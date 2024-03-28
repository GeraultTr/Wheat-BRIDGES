import os
import pickle

import wheat_bridges

# Edited models
from root_bridges.root_carbon import RootCarbonModelCoupled
from root_bridges.root_nitrogen import RootNitrogenModelCoupled

# Untouched models
from rhizodep.root_growth import RootGrowthModel
from rhizodep.root_anatomy import RootAnatomy
from rhizodep.rhizo_soil import SoilModel

from root_cynaps.root_water import RootWaterModel

# from Data_enforcer.shoot import ShootModel
from fspmwheat.simulation import WheatFSPM, scenario_utility

# Utilities
from metafspm.composite_wrapper import CompositeModel


class Model(CompositeModel):
    """
    Root-BRIDGES model

    Use guideline :
    1. store in a variable Model(g, time_step) to initialize the model, g being an openalea.MTG() object and time_step an time interval in seconds.

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

        # INIT INDIVIDUAL MODULES
        self.root_growth = RootGrowthModel(time_step, **scenario)
        self.g_root = self.root_growth.g
        self.root_anatomy = RootAnatomy(self.g_root, time_step, **scenario)
        self.root_water = RootWaterModel(self.g_root, time_step, **scenario)
        self.root_carbon = RootCarbonModelCoupled(self.g_root, time_step, **scenario)
        self.root_nitrogen = RootNitrogenModelCoupled(self.g_root, time_step, **scenario)
        self.soil = SoilModel(self.g_root, time_step, **scenario)
        self.shoot = WheatFSPM(**scenario_utility(INPUTS_DIRPATH="test/inputs", isolated_roots = True, cnwheat_roots = False))
        self.g_shoot = self.shoot.g

        # EXPECTED !
        self.models = (self.root_growth, self.root_anatomy, self.root_water, self.root_carbon, self.root_nitrogen, self.soil, self.shoot)
        self.mtgs = {"root": self.g_root, "shoot": self.g_shoot} # TODO May be optionnal, see later

        # LINKING MODULES
        self.link_around_mtg(translator_path=wheat_bridges.__path__[0])

        self.root_water.post_coupling_init()

    def run(self):
        # Update environment boundary conditions
        self.soil()

        # Compute shoot flows and state balance for CN-wheat
        self.shoot()

        # Compute root growth from resulting states
        self.root_growth()
        
        # Extend property dictionnaries after growth
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
