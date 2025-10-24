import multiprocessing as mp
import time
import os

# Model packages
import openalea.wheatbridges
from openalea.rhizosoil.model import RhizoSoil
from openalea.wheatbridges import WheatBRIDGES
from openalea.wheatbridges import LightModel

# Utility packages
from openalea.fspm.utility.scenario.initialize import MakeScenarios as ms
from openalea.fspm.utility.writer.logging import Logger
from openalea.metafspm.scene_wrapper import play_Orchestra
from openalea.fspm.utility.plot import analyze_data


if __name__ == "__main__":
    # scenarios = ms.from_table(file_path="inputs/Scenarios_25-08-05.xlsx", which=["WB_ref"])
    # custom_suffix = "r12_ref_unbal"
    # scenarios = ms.from_table(file_path="inputs/Scenarios_25-08-05.xlsx", which=["WB_debug"])
    scenarios = ms.from_table(file_path="inputs/Scenarios_25-08-05.xlsx", which=["WB_debug2"])
    # custom_suffix = "r19_debug_inter"
    custom_suffix = "r71_debug"
    output_folder = "outputs/parametrization"
    # densities = [50, 200, 400]
    # densities = [50, 400]
    densities = [250]
    
    scene_xrange = 0.15
    scene_yrange = 0.15
    row_spacing = 0.15
    environment_models_number = 2
    subprocesses_number = [int(max(scene_xrange * scene_yrange * density, 1)) + environment_models_number for density in densities]
    parallel_development = 1 # To keep room in CPUs if launching dev simulations in parallel on the machine
    max_processes = mp.cpu_count() - max(subprocesses_number) - parallel_development - 1 # -1 for the main process

    parallel = False
    processes = []

    if parallel:
        finished_process = 0
        for target_density in densities:
            requiered_subprocesses = int(max(scene_xrange * scene_yrange * target_density, 1)) + environment_models_number
            for scenario_name, scenario in scenarios.items():
                # Main process creation part
                while True:
                    # Remove any finished processes and join them to release resources
                    alive_processes = []
                    for proc in processes:
                        if proc.is_alive():
                            alive_processes.append(proc)
                        else:
                            proc.join()
                    processes = alive_processes

                    if len(processes) < max_processes:
                        break
                    time.sleep(1)
                full_scenario_name = f"{scenario_name}_{target_density}_{custom_suffix}"
                print(f"Launching {full_scenario_name}...")

                p = mp.Process(target=play_Orchestra, kwargs=dict(scene_name=full_scenario_name, output_folder=output_folder, plant_models=[WheatBRIDGES], plant_scenarios=[scenario], 
                                    soil_model=RhizoSoil, soil_scenario=scenario, light_model=LightModel,
                                    translator_path=openalea.wheatbridges.__path__[0],
                                    logger_class=Logger, log_settings=Logger.light_log, heavy_log_period=24,
                                    scene_xrange=scene_xrange, scene_yrange=scene_yrange, sowing_density=target_density, row_spacing=row_spacing,
                                    time_step=3600, n_iterations=50*24))

                p.start()
                processes.append(p)
                
    else:
        for target_density in densities:
            for scenario_name, scenario in scenarios.items():

                full_scenario_name = f"{scenario_name}_{target_density}_{custom_suffix}"

                clean_exit = play_Orchestra(scene_name=full_scenario_name, output_folder=output_folder, plant_models=[WheatBRIDGES], plant_scenarios=[scenario], 
                                    soil_model=RhizoSoil, soil_scenario=scenario, light_model=LightModel,
                                    translator_path=openalea.wheatbridges.__path__[0],
                                    logger_class=Logger, log_settings=Logger.heavy_log, heavy_log_period=1000,
                                    scene_xrange=scene_xrange, scene_yrange=scene_yrange, sowing_density=target_density, row_spacing=row_spacing,
                                    # time_step=3600, n_iterations=500, record_performance=True)
                                    time_step=3600, n_iterations=2500, record_performance=True)

                if clean_exit:
                    subscenarios = [subsc for subsc in os.listdir(os.path.join(output_folder, full_scenario_name)) if subsc not in ["Soil", "Delete_to_Stop"]]
                    for subscenario in subscenarios:
                        print("analysing", subscenario)
                        analyze_data(scenarios=[full_scenario_name], outputs_dirpath=output_folder, target_folder_key=subscenario,
                                        inputs_dirpath="inputs",
                                        on_sums=True,
                                        on_performance=True,
                                        animate_raw_logs=False,
                                        target_properties=None,
                                        on_shoot_logs=True)
                    
                    target_folder_key = "Soil"
                    
                    analyze_data(scenarios=[full_scenario_name], outputs_dirpath=output_folder, target_folder_key=target_folder_key,
                                    inputs_dirpath="inputs",
                                    on_soil_logs=True)

    # After all tasks started, join any remaining processes
    for proc in processes:
        proc.join()

