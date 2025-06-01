import wheat_bridges

# Edited models
from root_bridges.root_CN import RootCNUnified
from root_bridges.root_growth import RootGrowthModelCoupled

# Untouched models
from rhizodep.root_anatomy import RootAnatomy
from root_cynaps.root_water import RootWaterModel

# Shoot Model
from fspmwheat.simulation import WheatFSPM, scenario_utility

# Utilities
from metafspm.composite_wrapper import CompositeModel
from metafspm.component_factory import Choregrapher
from log.visualize import plot_mtg


class WheatBRIDGES(CompositeModel):
    """
    Root-BRIDGES model

    Use guideline :
    1. store in a variable Model(g, time_step) to initialize the model, g being an openalea.MTG() object and time_step a time interval in seconds.

    2. print Model.documentation for more information about editable model parameters (optional).

    3. Use Model.scenario(**dict) to pass a set of scenario-specific parameters to the model (optional).

    4. Use Model.run() in a for loop to perform the computations of a time step on the passed MTG File
    """

    def __init__(self, shared_root_mtgs: dict={}, name: str="Plant", time_step: int=3600, coordinates: list=[0, 0, 0], rotation: float=0, **scenario):
        """
        DESCRIPTION
        ----------
        __init__ method of the model. Initializes the thematic modules and link them.

        :param g: the openalea.MTG() instance that will be worked on. It must be representative of a root architecture.
        :param time_step: the resolution time_step of the model in seconds.
        """
        # DECLARE GLOBAL SIMULATION TIME STEP, FOR THE CHOREGRAPHER TO KNOW IF IT HAS TO SUBDIVIDE TIME-STEPS
        self.name = name
        self.coordinates = coordinates
        self.rotation = rotation

        Choregrapher().add_simulation_time_step(time_step)
        self.time = 0

        parameters = scenario["parameters"]
        root_parameters = parameters["root_bridges"]["roots"]
        self.input_tables = scenario["input_tables"]

        # INIT INDIVIDUAL MODULES
        if len(scenario["input_mtg"]) > 0:
            self.root_growth = RootGrowthModelCoupled(g=scenario["input_mtg"]["root_mtg_file"], time_step=time_step, **root_parameters)
        else:
            self.root_growth = RootGrowthModelCoupled(g=None, time_step=time_step, **root_parameters)
        self.g_root = self.root_growth.g
        self.root_anatomy = RootAnatomy(self.g_root, time_step, **root_parameters)
        self.root_water = RootWaterModel(self.g_root, time_step, **root_parameters)
        self.root_cn = RootCNUnified(self.g_root, time_step, **root_parameters)
        self.shoot = WheatFSPM(root_mtg=self.g_root, **scenario_utility(INPUTS_DIRPATH="inputs", stored_times="all", isolated_roots=True, cnwheat_roots=False, update_parameters_all_models=parameters))
        self.g_shoot = self.shoot.g

        # LINKING MODULES
        self.declare_data_and_couple_components(root=self.g_root, shoot=self.g_shoot,
                                                translator_path=wheat_bridges.__path__[0],
                                                components=(self.root_growth, self.root_anatomy, self.root_water, self.root_cn, self.shoot))
        
        # Specific here TODO remove later
        self.root_water.collar_children = self.root_growth.collar_children
        self.root_water.collar_skip = self.root_growth.collar_skip
        self.root_cn.collar_children = self.root_growth.collar_children
        self.root_cn.collar_skip = self.root_growth.collar_skip

        # Provide signature for the MTG
        self.shared_root_mtgs = shared_root_mtgs
        self.props = self.g_root.properties()

        # Performed in initialization and run to update coordinates
        plot_mtg(self.g_root, position=self.coordinates, rotation=self.rotation)

        self.props["plant_id"] = name
        self.props["model_name"] = self.__class__.__name__
        self.props["carried_components"] = [component.__class__.__name__ for component in self.components]

        self.shared_root_mtgs[self.props["plant_id"]] = self.props


    def run(self):
        self.apply_input_tables(tables=self.input_tables, to=self.components, when=self.time)

        # Retrieve soil status for plant
        # NOTE : mandatory process pointer otherwise there is a huge access overhead since each plant does it in parallel
        local_pointer = self.shared_root_mtgs[self.props["plant_id"]]
        # print(local_pointer["microbial_N"])
        # print(local_pointer["microbial_C"])

        # NOTE : here you have to perform a per-variable update otherwise dynamic links are broken
        for variable_name in self.soil_outputs + ["voxel_neighbor"]:
            if variable_name not in self.props.keys():
                self.props[variable_name] = {}
            
            self.props[variable_name].update(local_pointer[variable_name])

        # Compute root growth from resulting states
        self.root_growth(modules_to_update=[c for c in self.components if c.__class__.__name__ != "RootGrowthModelCoupled" and c.__class__.__name__ != "WheatFSPM"],
                         soil_boundaries_to_infer=self.soil_outputs)
        
        # Update MTG coordinates accounting for position in the scene
        plot_mtg(self.g_root, position=self.coordinates, rotation=self.rotation)
        print(self.props["y1"][1], self.name)

        # Update topological surfaces and volumes based on other evolved structural properties
        self.root_anatomy()

        # Compute state variations for water and then carbon and nitrogen
        self.root_water()
        self.root_cn()

        # Compute shoot flows and state balance for CN-wheat
        self.shoot()

        # Send plant status to soil
        self.shared_root_mtgs[self.props["plant_id"]] = self.props

        self.time += 1
