# Public packages
import os, traceback, time
import multiprocessing as mp
# Model packages
from wheat_bridges.wheat_bridges import WheatBRIDGES
# Utility packages
from log.logging import Logger
from initialize.initialize import MakeScenarios as ms
from analyze.analyze import analyze_data, test_output_range


def single_run(scenario, outputs_dirpath="outputs", simulation_length=2500, echo=True, log_settings={}):

    whole_plant = WheatBRIDGES(time_step=3600, **scenario)
    
    logger = Logger(model_instance=whole_plant, components=whole_plant.components,
                    outputs_dirpath=outputs_dirpath,
                    time_step_in_hours=1, logging_period_in_hours=24,
                    recording_shoot=True,
                    echo=echo, **log_settings)
    
    stop_file = os.path.join(outputs_dirpath + " *", "Delete_to_Stop")
    open(stop_file, "w").close()
    try:
        for _ in range(simulation_length):
            # Placed here also to capture mtg initialization
            
            # logger.run_and_monitor_model_step()
            logger()
            whole_plant.run()

            if not os.path.exists(stop_file):
                raise KeyboardInterrupt

    except Exception as e:
        logger.exceptions.append(traceback.format_exc())

    finally:
        logger.stop()
        analyze_data(scenarios=[os.path.basename(outputs_dirpath)], inputs_dirpath="inputs", outputs_dirpath="outputs", target_properties=None, on_sums=True, on_shoot_logs=True)
        inspect = False
        leaf_elements = {vid: [whole_plant.g_shoot.get_vertex_property(vid) for vid in whole_plant.g_shoot.components_at_scale(vid, 5)] for vid in whole_plant.g_shoot.components_at_scale(1, 2)}
        print(leaf_elements)
        if inspect:
            while True:
                command = input("Command? ")
                try:
                    eval(command)
                except:
                    print("Invalid command")
        #test_output_range(outputs_dirpath=outputs_dirpath, scenarios=[scenario], test_file_dirpath="inputs")


def simulate_scenarios(scenarios, simulation_length=24, echo=True, custom_prefix=None, log_settings={}):
    processes = []
    max_processes = mp.cpu_count()
    for scenario_name, scenario in scenarios.items():

        # Enable quick parallel testing with exact same parameters
        if custom_prefix:
            scenario_name = f"{scenario_name}_{custom_prefix}"

        while len(processes) == max_processes:
            for proc in processes:
                if not proc.is_alive():
                    processes.remove(proc)
            time.sleep(1)

        p = mp.Process(target=single_run, kwargs=dict(scenario=scenario,
                                                      outputs_dirpath=os.path.join("outputs", str(scenario_name)),
                                                      simulation_length=simulation_length,
                                                      echo=echo,
                                                      log_settings=log_settings))
        p.start()
        processes.append(p)


if __name__ == '__main__':

    #scenarios = ms.from_table(file_path="inputs/Scenarios_24-11-06.xlsx", which=["WB_R13", "WB_R14", "WB_R15", "WB_R16", "WB_R17", "WB_R18", "WB_R19"])
    # scenarios = ms.from_table(file_path="inputs/Scenarios_24-11-06.xlsx", which=["WB_R21", "WB_R22", "WB_R23", "WB_R24"])
    #scenarios = ms.from_table(file_path="inputs/Scenarios_24-11-06.xlsx", which=["WB_Reference", "WB_Reference_V1"])
    scenarios = ms.from_table(file_path="inputs/Scenarios_24-11-06.xlsx", which=["WB_long"])
    # scenarios = ms.from_table(file_path="inputs/Scenarios_24-11-06.xlsx", which=["WB_lowS7"])
    for name, scenario in scenarios.items():
        single_run(scenario=scenario,
                                                        outputs_dirpath=os.path.join("outputs", str(name)),
                                                        simulation_length=120,
                                                        echo=True,
                                                        log_settings=Logger.medium_log_focus_images)
    # simulate_scenarios(scenarios, simulation_length=2500, log_settings=Logger.medium_log_focus_images)
