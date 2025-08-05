import os
import numpy as np

# Utility packages
from analyze.analyze import analyze_data, test_output_range
from log.visualize import post_compress_gltf


if __name__ == '__main__':

    # scenarios = ["Drew_1975_low", "Drew_1975_1"]
    #scenarios = ["Drew_1975_low"]
    # scenarios = ["RC_ref_30D_debug"]
    # target_days = [ 5, 7, 10, 20, 30, 40, 50, 60] #, 70, 80, 90, 100]
    # target_days = np.arange(10, 61, 1)
    # target_days = [10, 20, 30, 40, 50, 60]
    
    # scenarios = [f"RC_ref_high_{day}D" for day in target_days]
    # scenarios = [f"RC_ref_{day}D" + "_images" for day in target_days]
    # scenarios = [f"RC_no_hair_{day}D" for day in target_days]
    # scenarios = [f"RC_ref_{day}D" for day in target_days] + [f"RC_no_hair_{day}D" for day in target_days]

    # for n_scenario in ["RC_ref", "RC_ref_0.01",	"RC_ref_0.05", "RC_ref_0.5", "RC_ref_5", "RC_ref_50"]:
    # for n_scenario in ["RC_ref"]:
    # # for n_scenario in ["RC_ref_big_lats"]:
    #     # target_days = [10, 20, 30, 40, 50]
    #     target_days = [50]
    #     target_concentration = "5.00e-01"
    #     # target_smax = np.logspace(0, 4, 11) * 1e-9
    #     target_smax = [5e-6]

    #     scenarios = [f"{n_scenario}_{target_concentration}_{day}D" for day in target_days]
    #     # scenarios = [f"{n_scenario}_{target_concentration}_{target_days[0]}D_{smax:.2e}max" for smax in target_smax]

    #     # output_path = "outputs"
    #     output_path = os.path.join("outputs", "batch_fig7")
        
    #     #output_path = "C:/Users/tigerault/OneDrive - agroparistech.fr/Thesis/Sujet/Modelling/saved_scenarios/05-06_hairless_tests"
    #     # output_path = "C:/Users/tigerault/OneDrive - agroparistech.fr/Thesis/Sujet/Modelling/saved_scenarios/01-06_ISRR 2024"

    #     # test_output_range(scenarios=scenarios, outputs_dirpath="outputs", test_file_dirpath="inputs/outputs_validation_root_cynaps_V0.xlsx")

    #     # post_compress_gltf(os.path.join(output_path, scenarios[0], "root_images"))

    #     analyze_data(scenarios=scenarios, outputs_dirpath=output_path, inputs_dirpath="inputs",
    #                     on_sums=False,
    #                     on_performance=False,
    #                     animate_raw_logs=True,
    #                     target_properties=None
    #                     )
    output_path = os.path.join("outputs", "batch2")

    for scenario_name in ["WB_ref1_400"]:
        subscenarios = [subsc for subsc in os.listdir(os.path.join(output_path, scenario_name)) if subsc not in ["Soil", "Delete_to_Stop"]]
        for subscenario in subscenarios:

            analyze_data(scenarios=[scenario_name], outputs_dirpath=output_path, target_folder_key=subscenario,
                            inputs_dirpath="inputs",
                            on_sums=False,
                            on_performance=False,
                            animate_raw_logs=False,
                            target_properties=None,
                            on_shoot_logs=True
            )