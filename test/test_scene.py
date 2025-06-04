# Model packages
from wheat_bridges.rhizospheric_soil import RhizosphericSoil
from wheat_bridges.wheat_bridges_no_soil import WheatBRIDGES
from wheat_bridges.caribu_component import LightModel

# Utility packages
from initialize.initialize import MakeScenarios as ms
from log.logging import Logger
from metafspm.scene_wrapper import play_Orchestra


if __name__ == "__main__":
    scenarios = ms.from_table(file_path="inputs/Scenarios_24-11-06.xlsx", which=["WB_ref1"])
    play_Orchestra(scene_name="Test_scene", output_folder="outputs", plant_models=[WheatBRIDGES], plant_scenarios=[scenarios["WB_ref1"]], 
                           soil_model=RhizosphericSoil, soil_scenario=scenarios["WB_ref1"], light_model=LightModel,
                           logger_class=Logger, log_settings=Logger.light_log,
                           scene_xrange=0.15, scene_yrange=0.15, sowing_density=50, # Test with only one plant
                           n_iterations=1000)
