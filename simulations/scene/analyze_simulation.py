import os
import numpy as np

# Utility packages
from openalea.fspm.utility.plot.analyze import analyze_data, test_output_range
from openalea.fspm.utility.writer.visualize import post_compress_gltf


if __name__ == '__main__':
    
    # output_path = os.path.join("outputs", "recoupling")
    output_path = os.path.join("outputs", "parametrization")

    # for scenario_name in ["WB_debug_250_r15_debug_unbal"]:
    # for scenario_name in ["WB_debug_250_r16_debug_unbal"]:
    # for scenario_name in ["WB_debug_250_r42_debug"]:
    for scenario_name in ["WB_debug2_250_r43_debug"]:
    # for scenario_name in ["WB_ref_250_r12_ref_unbal"]:
    # for scenario_name in ["WB_ref_250_r12_ref_unbal", "WB_debug_250_r15_debug_unbal"]:
    # for scenario_name in ["WB_ref_250_r3_heavy"]:
        # subscenarios = [subsc for subsc in os.listdir(os.path.join(output_path, scenario_name)) if subsc not in ["Soil", "Soil *", "Delete_to_Stop"]]
        subscenarios = ["WheatBRIDGES_0_" + scenario_name]
        for subscenario in subscenarios:
            print("analysing", subscenario)
            if True:
                analyze_data(scenarios=[scenario_name], outputs_dirpath=output_path, target_folder_key=subscenario,
                                inputs_dirpath="inputs",
                                on_sums=True,
                                on_performance=False,
                                animate_raw_logs=False,
                                target_properties=None,
                                on_shoot_logs=False,
                                on_images=False)
            if True:
                try:
                    analyze_data(scenarios=[scenario_name], outputs_dirpath=output_path, target_folder_key=subscenario,
                                    inputs_dirpath="inputs",
                                    on_sums=False,
                                    on_performance=False,
                                    animate_raw_logs=False,
                                    target_properties=None,
                                    on_shoot_logs=True,
                                    on_images=False)
                except:
                    print("Finished shoot")
            if True:
                analyze_data(scenarios=[scenario_name], outputs_dirpath=output_path, target_folder_key=subscenario,
                                inputs_dirpath="inputs",
                                on_sums=False,
                                on_performance=False,
                                animate_raw_logs=True,
                                target_properties=None,
                                on_shoot_logs=False,
                                on_images=False)
                

        do_soil=False
        if do_soil:
            analyze_data(scenarios=[scenario_name], outputs_dirpath=output_path, target_folder_key="Soil",
                                    inputs_dirpath="inputs",
                                    on_sums=True,
                                    on_soil_logs=False)