# Carbon-balance debug log

Goal: `check_balance` in `Root_BRIDGES/.../root_CN.py` must hold to machine precision
(no carbon appearing/disappearing). Any residual is a real bug, never "numerical noise".
Test entry point: `Wheat-BRIDGES/simulations/scene/simulation_bal.py` (1 plant, easiest to read).

## Status: stable for 50+ simulated hours, residual small and bounded, not yet machine-precision

## Fixed so far

1. **`Root_BRIDGES/.../root_growth.py`, `ADDING_A_CHILD`** (earlier session) — new primordia
   (`nil_properties=True` branch) were never given a `living_struct_mass` entry. Fixed by adding
   `living_struct_mass=0.` to that `add_child(...)` call. Since extended to also default
   `C_sucrose_root`, `C_hexose_reserve`, `phloem_AA`, `xylem_AA`, `storage_protein` (and to copy
   them from the mother element in the `identical_properties=True` branch) — every eager CN
   property needs an entry for every vertex for fix #4's `indices_of(focus_vids)` to resolve
   correctly.

2. **`Root-CyNAPS/.../root_water.py`, `water_transport_munch_arrays`** (earlier session) —
   `Cv_solutes_xylem`/`Cv_solutes_phloem` combined raw `.values_array()` calls before slicing to
   the focus set. Fixed by slicing each source array first, combining after.

3. **`Root-CyNAPS/.../root_nitrogen.py`, `axial_transport_N_arrays`** — double-counting bug.
   The post-solve block (lines ~1525-1539, added in an earlier session) was adding the *full*
   `R_diffusion_actual` directly onto `C_hexose_root`/`AA`, on top of what `_C_hexose_root`/`_AA`
   (`@state`, in root_CN.py) *also* add via their own explicit inflow term. Confirmed via the real
   Choregrapher schedule (`rate -> axial -> state -> totalstate`) that axial runs *before* state,
   so the post-solve write and the `@state` computation both apply the same flux. Fix: deleted the
   redundant block; `@state` now picks up the axial-corrected `diffusive_flux_name` property as its
   sole inflow, exactly like the (already-correct) `xylem_Nm`/`xylem_AA` case. This alone dropped
   the residual from a large, fast-growing value to ~1e-7 mol C.

4. **`Root-CyNAPS/.../root_nitrogen.py` (`axial_transport_N_arrays`) and `root_water.py`
   (`water_transport_munch_arrays`) — eager/lazy property index mismatch.** Both functions compute
   one shared `focus_glob_idx = vertex_index.indices_of(focus_elements)` and use it to slice every
   property they touch. But properties fall into two registration classes:
   - **eager**: explicitly initialized for *every* vertex at creation, in `ADDING_A_CHILD`'s
     `add_child(...)` call (`living_struct_mass`, `length`, `radius`, `soil_temperature`, `label`,
     `struct_mass`, `type`, `C_hexose_root`, `AA`, `C_sucrose_root`, `phloem_AA`, `xylem_AA`,
     `C_hexose_reserve`, `storage_protein`).
   - **lazy**: only ever registered for a vertex once it enters `focus_elements` (`struct_mass>0`),
     via the `@state`/`@rate` Functor dispatch (`vertex_index`, `parent_id`, `K_xylem`, `xylem_volume`,
     `phloem_volume`, `symplasmic_volume`, exchange surfaces, `xylem_Nm`, `Nm`, diffusive flux props,
     etc.).

   `vertex_index` is itself lazy. As soon as any not-yet-focus vertex exists between two focus
   vertices in vid order, `vertex_index`'s array is *shorter* than the eager arrays', so
   `focus_glob_idx` (positions in vertex_index's space) silently picks the **wrong slot** in any
   eager array — corrupting that vertex's value (read) or overwriting a different vertex's value
   (write). This is what produced the `inf` values in `C_sucrose_root`/`phloem_AA`/`xylem_AA` for a
   newly-created, not-yet-emerged lateral root primordium (confirmed by cross-checking
   `keys_array()` across properties: `vertex_index`/anatomy props disagreed with the eager CN
   properties about which vid lived at global index 625).

   Tried first: making `vertex_index`/`parent_id` eager too (mirroring the CN properties). Wrong
   direction — broke alignment with the *other* lazy properties (`K_xylem`, `xylem_volume`, ...)
   instead, since those can't be sensibly eager-initialized (they depend on anatomy that doesn't
   exist yet for a struct_mass=0 primordium).

   Correct fix: stopped sharing one global `focus_glob_idx` for every property access. Each eager
   property now gets its own index via `props[name].indices_of(focus_vids)` before being sliced.
   Since `indices_of` preserves input order, slicing any property (eager or lazy) by
   `props[that_property].indices_of(focus_vids)` always yields a result aligned position-for-position
   with `focus_vids`, regardless of how that property is internally registered. Applied to:
   `length`/`radius`/`living_struct_mass`/`soil_temperature`/`label` (one shared `eager_idx`, since
   they're all set together in the same `add_child` call) and, in the per-solute loop,
   `solute_massic_concentration_prop`/`solute_massic_concentration_symplasm`/`diffusive_flux_name`
   (recomputed per solute config, since `xylem_Nm`/`Nm` are lazy while the other three solutes'
   props are eager).

## Result of fix #4

Re-ran `simulation_bal.py` after the fix: progressed cleanly past both prior crash points
(the nan/inf assertion at t=43200s and the `IndexError` at t=46800s that the half-finished
vertex_index-eager attempt introduced), and kept running stably to **50+ simulated hours**
with no errors and no `SOLVER NOT CONSERVING` warnings (which used to fire reliably by then).
Residual (`resid` in `[C-bal]` lines) stays in the ~1e-7 to 1e-6 mol C range, bounded, not
growing without limit — a large improvement over before, but **not yet machine precision**,
so per the project's standing rule this remaining residual is still a real bug, not noise.

## Removed: the lsm-drift / exact_lsm_impact diagnostic in `check_balance`

An earlier iteration of `check_balance` carried a second diagnostic (`lsm_drift`,
`exact_lsm_impact`, `lsm_C_impact`, and a "Per-pool lsm-growth contribution" print block) built
on the premise that `@state`'s formula `C_new = C_old + dt*flow/lsm_new` doesn't dilute
concentration when `lsm` grows, so growth itself would inject `C_old_i * delta_lsm_i` worth of
phantom mol-C per vertex.

That premise is false for this codebase. Traced the real per-step call order in
`WheatBRIDGES.run()` (`Wheat-BRIDGES/.../wheat_bridges.py:79-101`, the path `simulation_bal.py`
actually exercises — *not* the unused `Root_BRIDGES/.../root_bridges.py`): `self.root_growth(
modules_to_update=[...,root_cn,...])` runs structural growth and then, internally, calls
`self.post_growth_updating(modules_to_update=..., ...)` (`rhizodep/.../root_growth.py:3711`)
*before* `self.root_cn()` (rate→axial→state→totalstate) executes for that step. That
`post_growth_updating` rescales every property tagged `state_variable_type="massic_concentration"`
in its dataclass declaration — confirmed for all seven C-bearing pools (`C_hexose_root`,
`C_hexose_reserve`, `C_sucrose_root`, `AA`, `storage_protein`, `xylem_AA`, `phloem_AA`) — by the
exact ratio `old_struct_mass/new_struct_mass` for a segment that grew in place, or by an exact
mass-fraction split with the parent for a newly created vertex. Both paths preserve
`concentration * mass` exactly (zero net mol-C effect), by construction, *before* `check_balance`
ever runs. So growth dilution is already fully resolved upstream with zero residual; the
`exact_lsm_impact` apparatus was modeling a phantom effect. Removed it (and the `lsm_drift`/
`_new_n_seg` bookkeeping, the `[C-bal]` line's `lsm_impact(exact)`/`unexplained` fields, and the
"Per-pool lsm-growth contribution" print block) — none of it fed `residual`/`expected_C`/the
assert, so removal does not change check_balance's actual behavior, only its diagnostics.

## Next steps

- Let the run continue further (it was still healthy past t=226800s / ~63h when last checked)
  to see whether the residual stays bounded over the full `n_iterations=2500` (~104 days) run,
  or starts growing again at some later structural event.
- Worth auditing whether any *other* property in `axial_transport_N_arrays`/
  `water_transport_munch_arrays` is eager-but-still-sliced-via-the-shared `focus_glob_idx` (a
  search for `props['<eager-prop>'].values_array()[focus_glob_idx]` across both files came back
  clean as of this fix, but new eager properties added later could reintroduce this class of bug).
