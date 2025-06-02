# Public packages


# Model packages
from wheat_bridges.rhizospheric_soil import RhizosphericSoil
from wheat_bridges.wheat_bridges_no_soil import WheatBRIDGES
from wheat_bridges.caribu_component import LightModel

# Utility packages
from initialize.initialize import MakeScenarios as ms
from metafspm.scene_wrapper import play_Orchestra
#from log.logging import Logger
#from analyze.analyze import analyze_data


if __name__ == "__main__":
    # scenarios = ms.from_table(file_path="inputs/Scenarios_24-11-06.xlsx", which=["WB_ref1"])
    scenarios = ms.from_table(file_path="inputs/Scenarios_24-11-06.xlsx", which=["WB_ref1"])
    play_Orchestra(scene_name="Test_scene", output_folder="outputs", plant_models=[WheatBRIDGES], plant_scenarios=[scenarios["WB_ref1"]], 
                           soil_model=RhizosphericSoil, soil_scenario=scenarios["WB_ref1"], light_model=LightModel,
                           scene_xrange=0.15, scene_yrange=0.15,
                           n_iterations=24)
