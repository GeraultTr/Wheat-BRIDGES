import wheat_bridges

# Edited models
from root_bridges.root_carbon import RootCarbonModelCoupled
from root_bridges.root_nitrogen import RootNitrogenModelCoupled
from root_bridges.root_growth import RootGrowthModelCoupled
from root_bridges.soil_model import SoilModel

# Untouched models
from rhizodep.root_anatomy import RootAnatomy
from root_cynaps.root_water import RootWaterModel

# Shoot Model
from fspmwheat.simulation import WheatFSPM, scenario_utility
import wheat_bridges.cn_wheat_collar

# Utilities
from metafspm.composite_wrapper import CompositeModel
from metafspm.component_factory import Choregrapher


class Model(CompositeModel):
    """
    Root-BRIDGES model

    Use guideline :
    1. store in a variable Model(g, time_step) to initialize the model, g being an openalea.MTG() object and time_step a time interval in seconds.

    2. print Model.documentation for more information about editable model parameters (optional).

    3. Use Model.scenario(**dict) to pass a set of scenario-specific parameters to the model (optional).

    4. Use Model.run() in a for loop to perform the computations of a time step on the passed MTG File
    """

    def __init__(self, time_step: int, **scenario):
        """
        DESCRIPTION
        ----------
        __init__ method of the model. Initializes the thematic modules and link them.

        :param g: the openalea.MTG() instance that will be worked on. It must be representative of a root architecture.
        :param time_step: the resolution time_step of the model in seconds.
        """
        # DECLARE GLOBAL SIMULATION TIME STEP

        Choregrapher().add_simulation_time_step(time_step)
        self.time = 0
        parameters = scenario["parameters"]
        root_parameters = parameters["root_bridges"]
        self.input_tables = scenario["input_tables"]

        # INIT INDIVIDUAL MODULES
        self.root_growth = RootGrowthModelCoupled(scenario["input_mtg"]["root_mtg_file"], time_step, **root_parameters)
        self.g_root = self.root_growth.g
        self.root_anatomy = RootAnatomy(self.g_root, time_step, **root_parameters)
        self.root_water = RootWaterModel(self.g_root, time_step/5, **root_parameters)
        self.root_carbon = RootCarbonModelCoupled(self.g_root, time_step/4, **root_parameters)
        self.root_nitrogen = RootNitrogenModelCoupled(self.g_root, time_step/2, **root_parameters)
        self.soil = SoilModel(self.g_root, time_step, **root_parameters)
        self.soil_voxels = self.soil.voxels
        self.shoot = WheatFSPM(**scenario_utility(INPUTS_DIRPATH="inputs", stored_times="all", isolated_roots=True, cnwheat_roots=False, update_parameters_all_models=parameters))
        self.g_shoot = self.shoot.g

        # EXPECTED !
        self.models = (self.root_growth, self.root_anatomy, self.root_water, self.root_carbon, self.root_nitrogen, self.soil, self.shoot)
        self.data_structures = {"root": self.g_root, "shoot": self.g_shoot, "soil": self.soil_voxels}

        # LINKING MODULES
        self.link_around_mtg(translator_path=wheat_bridges.__path__[0])

        # Specific here TODO remove later
        self.root_water.post_coupling_init()

    def run(self):
        self.apply_input_tables(tables=self.input_tables, to=self.models, when=self.time)

        # Update environment boundary conditions
        self.soil()

        # Compute shoot flows and state balance for CN-wheat
        self.shoot()

        # Compute root growth from resulting states
        self.root_growth()

        # Extend property dictionaries after growth
        self.root_anatomy.post_growth_updating()
        self.root_water.post_growth_updating()
        self.root_carbon.post_growth_updating()
        self.root_nitrogen.post_growth_updating()
        self.soil.post_growth_updating()

        # Update topological surfaces and volumes based on other evolved structural properties
        self.root_anatomy()

        # Compute rate -> state variations for water and then carbon and nitrogen
        self.root_water()
        self.root_carbon()
        self.root_nitrogen()

        self.time += 1

