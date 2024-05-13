# Public packages
import os, sys
import multiprocessing as mp
# Model packages
from wheat_bridges.wheat_bridges import Model
# Utility packages
from initialize.initialize import MakeScenarios as ms
from log.logging import Logger
from analyze.analyze import analyze_data


def single_run(scenario, outputs_dirpath="outputs"):
    whole_plant = Model(time_step=3600, **scenario)
    
    logger = Logger(model_instance=whole_plant, outputs_dirpath=outputs_dirpath, 
                    time_step_in_hours=1,
                    logging_period_in_hours=6,
                    recording_images=False, plotted_property="C_hexose_root", show_soil=True,
                    recording_mtg=False,
                    recording_raw=False,
                    recording_sums=True,
                    recording_shoot=True,
                    recording_performance=True,
                    echo=True)

    try:
        for _ in range(200):
            # Placed here also to capture mtg initialization
            logger()
            logger.run_and_monitor_model_step()
            #whole_plant.run()

    except (ZeroDivisionError, KeyboardInterrupt):
        logger.exceptions.append(sys.exc_info())

    finally:
        logger.stop()
        analyze_data(outputs_dirpath=outputs_dirpath,
                     on_sums=True,
                     on_performance=True,
                     animate_raw_logs=False,
                     on_shoot_logs=True,
                     target_properties=None
                     )


def test_apply_scenarios():
    scenarios = ms.from_table(file_path="inputs/Scenarios.xlsx", which=["WB2", "WB3"])
    processes = []
    for scenario_name, scenario in scenarios.items():
        print(f"[INFO] Launching scenario {scenario_name}...")
        p = mp.Process(target=single_run, kwargs=dict(scenario=scenario, outputs_dirpath=os.path.join("outputs", str(scenario_name))))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()


if __name__ == '__main__':
    test_apply_scenarios()
    # In the end put the system to sleep, windows only
    #os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
