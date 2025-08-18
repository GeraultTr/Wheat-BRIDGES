# Model packages
import wheat_bridges
from wheat_bridges.rhizospheric_soil import RhizosphericSoil
from wheat_bridges.wheat_bridges_no_soil import WheatBRIDGES
from wheat_bridges.caribu_component import LightModel

# Utility packages
from initialize.initialize import MakeScenarios as ms
from log.logging import Logger
from openalea.metafspm.scene_wrapper import play_Orchestra


if __name__ == "__main__":
    scenarios = ms.from_table(file_path="inputs/Scenarios_25-06-05.xlsx", which=["WB_ref1"])
    for scenario_name, scenario in scenarios.items():
        play_Orchestra(scene_name=scenario_name, output_folder="outputs/long_run", plant_models=[WheatBRIDGES], plant_scenarios=[scenario], 
                            soil_model=RhizosphericSoil, soil_scenario=scenario, light_model=LightModel,
                            translator_path=wheat_bridges.__path__[0],
                            logger_class=Logger, log_settings=Logger.light_log, heavy_log_period=24,
                            scene_xrange=0.15, scene_yrange=0.15, sowing_density=1,
                            n_iterations=100*24)
