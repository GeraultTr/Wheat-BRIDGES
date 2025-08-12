import os
import numpy as np

# Utility packages
from openalea.fspm.utility.plot.analyze import analyze_data, test_output_range
from openalea.fspm.utility.writer.visualize import post_compress_gltf


if __name__ == '__main__':
    
    output_path = os.path.join("outputs", "recoupling")

    for scenario_name in ["WB_ref2_250_tests"]:
        subscenarios = [subsc for subsc in os.listdir(os.path.join(output_path, scenario_name)) if subsc not in ["Soil", "Delete_to_Stop"]]
        for subscenario in subscenarios:
            print("analysing", subscenario)
            analyze_data(scenarios=[scenario_name], outputs_dirpath=output_path, target_folder_key=subscenario,
                            inputs_dirpath="inputs",
                            on_sums=False,
                            on_performance=True,
                            animate_raw_logs=False,
                            target_properties=None,
                            on_shoot_logs=False)

        analyze_data(scenarios=[scenario_name], outputs_dirpath=output_path, target_folder_key="Soil",
                                inputs_dirpath="inputs",
                                on_sums=True,
                                on_soil_logs=True)