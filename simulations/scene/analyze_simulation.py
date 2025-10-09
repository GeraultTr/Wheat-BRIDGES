import os
import numpy as np

# Utility packages
from openalea.fspm.utility.plot.analyze import analyze_data, test_output_range
from openalea.fspm.utility.writer.visualize import post_compress_gltf


if __name__ == '__main__':
    
    # output_path = os.path.join("outputs", "recoupling")
    output_path = os.path.join("outputs", "parametrization")

    for scenario_name in ["WB_ref_250_p4.2_heavy_short"]:
        # subscenarios = [subsc for subsc in os.listdir(os.path.join(output_path, scenario_name)) if subsc not in ["Soil", "Soil *", "Delete_to_Stop"]]
        subscenarios = ["WheatBRIDGES_4_" + scenario_name]
        for subscenario in subscenarios:
            print("analysing", subscenario)
            analyze_data(scenarios=[scenario_name], outputs_dirpath=output_path, target_folder_key=subscenario,
                            inputs_dirpath="inputs",
                            on_sums=False,
                            on_performance=False,
                            animate_raw_logs=True,
                            target_properties=None,
                            on_shoot_logs=False)

        do_soil=False
        if do_soil:
            analyze_data(scenarios=[scenario_name], outputs_dirpath=output_path, target_folder_key="Soil",
                                    inputs_dirpath="inputs",
                                    on_sums=True,
                                    on_soil_logs=False)