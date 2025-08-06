import os
import pickle

# Utility packages
from analyze.analyze import analyze_data


if __name__ == '__main__':
        
    scenarios = ["WB_ref1_50"]
    for scenario_name in scenarios:
        target_folder_key = "WheatBRIDGES_0"
        output_path = "outputs" 
        # output_path = "simulations/scene/outputs" # When debugging

        mtg_path = os.path.join(output_path, scenario_name, target_folder_key, "MTG_files")
        # mtg_path = os.path.join("/home/torisuten/package/Wheat-BRIDGES/Root_BRIDGES/simulations/scene/outputs/RB_ref/RootBRIDGES_0", "MTG_files")

        for mtg_name in os.listdir(mtg_path):
            mtg_filepath = os.path.join(mtg_path, mtg_name)
            with open(mtg_filepath, "rb") as f:
                g = pickle.load(f)
                g =g["root"]
                collar = g.node(1)
                coordinates = [collar.x1, collar.y1, collar.z1]
                print(coordinates)
                
                angle_node = g.node(116)
                vector = [angle_node.x2 - angle_node.x1, angle_node.y2 - angle_node.y1]
                print(vector)
                ref_vector = [1, 0]
                # # Compute dot product
                # dot = x1 * x2 + y1 * y2
                
                # # Compute norms (magnitudes)
                # norm1 = math.hypot(x1, y1)
                # norm2 = math.hypot(x2, y2)


        # analyze_data(scenarios=[scenario_name], outputs_dirpath=output_path, target_folder_key=target_folder_key,
        #                 inputs_dirpath="inputs",
        #                 on_sums=True,
        #                 on_performance=False,
        #                 animate_raw_logs=True,
        #                 target_properties=None)
