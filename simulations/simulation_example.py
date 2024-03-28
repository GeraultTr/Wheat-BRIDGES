from wheat_bridges.coupled_simulation import run_coupled_simulation
from datetime import datetime
import os
import shutil


def previous_outputs_clearing():
    root_path = os.path.dirname(__file__)
    try:
        # We remove all files and subfolders:
        try:
            shutil.rmtree(root_path + '/outputs')
            print("Deleted the 'outputs' folder...")
            print("Creating a new 'outputs' folder...")
            os.mkdir(root_path + '/outputs')
        except OSError:
            print("Creating a new 'outputs' folder...")
            os.mkdir(root_path + '/outputs')
    except OSError as e:
        print("An error occured when trying to delete the output folder: %s - %s." % (e.filename, e.strerror))

if __name__ == '__main__':
    logging = True
    running = True
    if running:
        previous_outputs_clearing()
        start_time = datetime.now().strftime("%y.%m.%d_%H.%M")
        output_path = os.path.dirname(__file__) + f'/outputs/{start_time}.nc'
    else:
        outputs_folder = os.path.dirname(__file__) + '/outputs'
        all_subdirs = [d for d in os.listdir(outputs_folder) if os.path.isdir(outputs_folder + '/' + d)]
        if len(all_subdirs) > 1:
            latest_subdir = all_subdirs.sort(reverse=True)[0]
        else:
            latest_subdir = all_subdirs[0]
        output_path = os.path.dirname(__file__) + '/outputs/' + latest_subdir
    print(output_path)
    run_coupled_simulation(z_soil_Nm_max=0, output_path=output_path, logging=logging, running=running)
