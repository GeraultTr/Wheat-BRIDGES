# Public packages


# Model packages
from wheat_bridges.rhizospheric_soil import RhizosphericSoil
from wheat_bridges.wheat_bridges import WheatBRIDGES

# Utility packages
from initialize.initialize import MakeScenarios as ms
from metafspm.scene_wrapper import play_Orchestra
#from log.logging import Logger
#from analyze.analyze import analyze_data


if __name__ == "__main__":
    scenarios = ms.from_table(file_path="inputs/Scenarios_24_11_10.xlsx", which=["RC_ref"])
    play_Orchestra(scene_name="Test_scene", output_folder="outputs", plant_models=[WheatBRIDGES], plant_scenarios=[scenarios["RC_ref"]], 
                           soil_model=RhizosphericSoil, soil_scenario=scenarios["RC_ref"], 
                           n_iterations=2500)
