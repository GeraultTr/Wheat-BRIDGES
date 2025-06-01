import wheat_bridges

# Soil model
from root_bridges.soil_model import SoilModel

# Utilities
from metafspm.composite_wrapper import CompositeModel
from metafspm.component_factory import Choregrapher


class RhizosphericSoil(CompositeModel):
    """
    Root-BRIDGES model

    Use guideline :
    1. store in a variable Model(g, time_step) to initialize the model, g being an openalea.MTG() object and time_step a time interval in seconds.

    2. print Model.documentation for more information about editable model parameters (optional).

    3. Use Model.scenario(**dict) to pass a set of scenario-specific parameters to the model (optional).

    4. Use Model.run() in a for loop to perform the computations of a time step on the passed MTG File
    """

    def __init__(self, shared_root_mtgs: dict, shared_soil: dict, time_step: int,  **scenario):
        """
        DESCRIPTION
        ----------
        __init__ method of the model. Initializes the thematic modules and link them.

        :param g: the openalea.MTG() instance that will be worked on. It must be representative of a root architecture.
        :param time_step: the resolution time_step of the model in seconds.
        """
        # DECLARE GLOBAL SIMULATION TIME STEP, FOR THE CHOREGRAPHER TO KNOW IF IT HAS TO SUBDIVIDE TIME-STEPS
        Choregrapher().add_simulation_time_step(time_step)
        self.time = 0
        parameters = scenario["parameters"]
        self.input_tables = scenario["input_tables"]

        # INIT INDIVIDUAL MODULES
        if shared_soil is not None:
            self.soil = SoilModel(time_step_in_seconds=time_step, shared_soil=shared_soil, **parameters)
        else:
            self.soil = SoilModel(time_step_in_seconds=time_step, **parameters)

        self.soil_voxels = self.soil.voxels

        # Manually assigning data structure for logger retreive
        self.declare_data(soil=self.soil_voxels)
        self.components = [self.soil]

        # LINKING MODULES
        # NOTE only plant to soil is necessary since plants retreive all soil states
        for id, props in shared_root_mtgs.items():
            vertices = props["vertex_index"].keys()

            # Performed for every mtg in case we use different models
            self.couple_current_with_components_list(receiver=self.soil, components=props["carried_components"], 
                                                    translator=self.open_or_create_translator(wheat_bridges.__path__[0]), 
                                                    subcategory=props["model_name"])
            
            # Step to ensure every neighbor gets computed at first
            props["voxel_neighbor"] = {vid: None for vid in vertices}

            # Requiered because soil states need to be written in the MTGs by soil, but hadn't been initialized by plants
            for variable_name in self.soil.state_variables:
                if variable_name not in props.keys() and variable_name != "voxel_neighbor":
                    props[variable_name] = {}

            shared_root_mtgs[id] = props
            


    def run(self, shared_root_mtgs):
        self.apply_input_tables(tables=self.input_tables, to=self.components, when=self.time)
        # Update environment boundary conditions
        self.soil(shared_root_mtgs=shared_root_mtgs)

        self.time += 1

