# Public packages
import os, sys
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
                    logging_period_in_hours=24,
                    recording_images=True, plotted_property="C_hexose_root", show_soil=True,
                    recording_mtg=False,
                    recording_raw=False,
                    recording_sums=True,
                    recording_performance=True,
                    echo=True)

    try:
        for _ in range(200):
            # Placed here also to capture mtg initialization
            logger()
            whole_plant.run()

    except (ZeroDivisionError, ):
        logger.exceptions.append(sys.exc_info())

    finally:
        logger.stop()
        analyze_data(outputs_dirpath=outputs_dirpath,
                     on_sums=True,
                     on_performance=True,
                     animate_raw_logs=False,
                     target_properties=[]
                     )


def test_apply_scenarios():
    scenarios = ms.from_table(file_path="inputs/Scenarios.xlsx", which=["WB1"])
    for scenario_name, scenario in scenarios.items():
        single_run(scenario=scenario, outputs_dirpath=os.path.join("outputs", str(scenario_name)))


test_apply_scenarios()
