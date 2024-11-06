import wheat_bridges

# Edited models
from root_bridges.root_CN import RootCNUnified
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


class WheatBRIDGES(CompositeModel):
    """
    Root-BRIDGES model

    Use guideline :
    1. store in a variable Model(g, time_step) to initialize the model, g being an openalea.MTG() object and time_step a time interval in seconds.

    2. print Model.documentation for more information about editable model parameters (optional).

    3. Use Model.scenario(**dict) to pass a set of scenario-specific parameters to the model (optional).

    4. Use Model.run() in a for loop to perform the computations of a time step on the passed MTG File
    """

    def __init__(self, name="Plant", time_step: int=3600, coordinates: list=[0, 0, 0], **scenario):
        """
        DESCRIPTION
        ----------
        __init__ method of the model. Initializes the thematic modules and link them.

        :param g: the openalea.MTG() instance that will be worked on. It must be representative of a root architecture.
        :param time_step: the resolution time_step of the model in seconds.
        """
        # DECLARE GLOBAL SIMULATION TIME STEP, FOR THE CHOREGRAPHER TO KNOW IF IT HAS TO SUBDIVIDE TIME-STEPS
        self.name = name
        Choregrapher().add_simulation_time_step(time_step)
        self.time = 0

        parameters = scenario["parameters"]
        root_parameters = parameters["root_bridges"]["roots"]
        self.input_tables = scenario["input_tables"]

        # INIT INDIVIDUAL MODULES
        if len(scenario["input_mtg"]) > 0:
            self.root_growth = RootGrowthModelCoupled(g=scenario["input_mtg"]["root_mtg_file"], time_step=time_step, **parameters)
        else:
            self.root_growth = RootGrowthModelCoupled(g=None, time_step=time_step, **parameters)
        self.g_root = self.root_growth.g
        self.root_anatomy = RootAnatomy(self.g_root, time_step, **root_parameters)
        self.root_water = RootWaterModel(self.g_root, time_step/10, **root_parameters)
        self.root_cn = RootCNUnified(self.g_root, time_step/3, **root_parameters)
        self.soil = SoilModel(self.g_root, time_step, **root_parameters)
        self.soil_voxels = self.soil.voxels
        self.shoot = WheatFSPM(**scenario_utility(INPUTS_DIRPATH="inputs", stored_times="all", isolated_roots=True, cnwheat_roots=False, update_parameters_all_models=parameters))
        self.g_shoot = self.shoot.g

        # LINKING MODULES
        self.declare_and_couple_components(self.root_growth, self.root_anatomy, self.root_water, self.root_cn, self.soil, self.shoot,
                                           translator_path=wheat_bridges.__path__[0])

        self.declare_data_structures(root=self.g_root, shoot=self.g_shoot, soil=self.soil_voxels)
        
        # Specific here TODO remove later
        self.root_water.post_coupling_init()


    def run(self):
        self.apply_input_tables(tables=self.input_tables, to=self.components, when=self.time)

        # Update environment boundary conditions
        self.soil()

        # Compute shoot flows and state balance for CN-wheat
        self.shoot()

        # Compute root growth from resulting states
        self.root_growth()

        # Extend property dictionaries after growth
        self.root_anatomy.post_growth_updating()
        self.root_water.post_growth_updating()
        self.root_cn.post_growth_updating()
        self.soil.post_growth_updating()

        # Update topological surfaces and volumes based on other evolved structural properties
        self.root_anatomy()

        # Compute state variations for water and then carbon and nitrogen
        self.root_water()
        self.root_cn()

        self.time += 1

