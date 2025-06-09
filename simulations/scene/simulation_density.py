import multiprocessing as mp
import time

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
    densities = [50, 200, 400]

    parallel = True
    scene_xrange = 0.2
    scene_yrange = 0.2
    environment_models_number = 2
    subprocesses_number = [int(max(scene_xrange * scene_yrange * density, 1)) + environment_models_number for density in densities]
    parallel_development = 0 # To keep room in CPUs if launching dev simulations in parallel on the machine
    max_processes = mp.cpu_count() - 4 # to keep space for other processes to run normally

    if parallel:
        processes = []
        total_running_processes = 0
        finished_process = 0
        for target_density in densities:
            requiered_subprocesses = int(max(scene_xrange * scene_yrange * target_density, 1)) + environment_models_number
            for scenario_name, scenario in scenarios.items():
                # Main process creation part
                while total_running_processes >= max_processes:
                    for proc in processes:
                        if not proc.is_alive():
                            processes.remove(proc)
                            # Supposing they exit in the same order than the input list
                            total_running_processes -= subprocesses_number[finished_process] + 1
                            finished_processes += 1
                    time.sleep(1)
                
                # If going through, subprocesses are launched
                total_running_processes += requiered_subprocesses + 1
                print("Total running processes = ", total_running_processes)

                p = mp.Process(target=play_Orchestra, kwargs=dict(scene_name=f"{scenario_name}_{target_density}", output_folder="outputs", plant_models=[WheatBRIDGES], plant_scenarios=[scenario], 
                                    soil_model=RhizosphericSoil, soil_scenario=scenario, light_model=LightModel,
                                    translator_path=wheat_bridges.__path__[0],
                                    logger_class=Logger, log_settings=Logger.medium_log_focus_properties,
                                    scene_xrange=scene_xrange, scene_yrange=scene_yrange, sowing_density=target_density,
                                    n_iterations=50*24))

                p.start()
                processes.append(p)
                
    else:
        for target_density in densities:
            for scenario_name, scenario in scenarios.items():

                play_Orchestra(scene_name=scenario_name + "_" + target_density, output_folder="outputs", plant_models=[WheatBRIDGES], plant_scenarios=[scenario], 
                                    soil_model=RhizosphericSoil, soil_scenario=scenario, light_model=LightModel,
                                    translator_path=wheat_bridges.__path__[0],
                                    logger_class=Logger, log_settings=Logger.medium_log_focus_properties,
                                    scene_xrange=scene_xrange, scene_yrange=scene_yrange, sowing_density=target_density,
                                    n_iterations=60*24)
