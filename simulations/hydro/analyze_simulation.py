import os
import numpy as np

# Utility packages
from openalea.fspm.utility.plot.analyze import analyze_data, test_output_range
from openalea.fspm.utility.writer.visualize import post_compress_gltf


if __name__ == '__main__':
    
    output_path = "/home/torisuten/Documents/outputs/wbr_outputs/test"
    # output_path = os.path.join("outputs", "parametrization")

    # for scenario_name in ["WB_defense1_1_dbg_bal_1.1"]:
    for scenario_name in ["WB_publish1_250_vmaa_x100"]:
    # for scenario_name in ["WB_def_soil_1_250_3d_2.1"]:

        # subscenarios = [subsc for subsc in os.listdir(os.path.join(output_path, scenario_name)) if subsc not in ["Soil", "Soil *", "Delete_to_Stop"]]
        subscenarios = ["WheatBRIDGES_0_" + scenario_name]
        for subscenario in subscenarios:
            print("analysing", subscenario)
            if False:
                analyze_data(scenarios=[scenario_name], outputs_dirpath=output_path, target_folder_key=subscenario,
                                inputs_dirpath="inputs",
                                on_sums=True)
                
            if False:
                # try:
                analyze_data(scenarios=[scenario_name], outputs_dirpath=output_path, target_folder_key=subscenario,
                                inputs_dirpath="inputs",
                                on_shoot_logs=True)
                # except Exception as e:
                #     print("encountered:", e)
                # finally:    
                #     print("Finished shoot")

            if False:
                analyze_data(scenarios=[scenario_name], outputs_dirpath=output_path, target_folder_key=subscenario,
                                inputs_dirpath="inputs",
                                animate_raw_logs=True)
                
            if False:
                analyze_data(scenarios=[scenario_name], outputs_dirpath=output_path, target_folder_key=subscenario,
                                inputs_dirpath="inputs",
                                on_mtg=True)


            if True:
                analyze_data(scenarios=[scenario_name], outputs_dirpath=output_path, target_folder_key="Soil",
                                        inputs_dirpath="inputs",
                                        on_sums=True,
                                        on_soil_logs=True)
