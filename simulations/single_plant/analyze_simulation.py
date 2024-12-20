import os
# Utility packages
from analyze.analyze import analyze_data


if __name__ == '__main__':

    scenarios = ["WB_lowS7"]

    #output_path = "outputs"
    #output_path = "C:/Users/tigerault/OneDrive - agroparistech.fr/Thesis/Sujet/Modelling/saved_scenarios/05-06_hairless_tests"
    output_path = "outputs"

    analyze_data(scenarios=scenarios, outputs_dirpath=output_path,
                     on_sums=True,
                     on_performance=True,
                     animate_raw_logs=False,
                     on_shoot_logs=True,
                     target_properties=None
                     )
    
    # In the end put the system to sleep, Windows only
    # os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    