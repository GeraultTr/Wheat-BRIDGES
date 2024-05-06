# Public packages
import os, sys
import multiprocessing as mp
import numpy as np
# Model packages
from wheat_bridges.wheat_bridges import Model
# Utility packages
from initialize.initialize import MakeScenarios as ms
from log.logging import Logger
from analyze.analyze import analyze_data


class SharedArray:
    def __init__(self, shape, model_number):
        self.array = mp.Array('d', shape[0] * shape[1] * shape[2])
        self.shape = shape
        self.np_array = np.frombuffer(self.array.get_obj(), dtype=np.float64).reshape(shape)
        self.barrier = mp.Barrier(model_number)  # Number of processes
        self.lock = mp.Lock()

    def wait(self):
        self.barrier.wait()

    def acquire_lock(self):
        self.lock.acquire()

    def release_lock(self):
        self.lock.release()


class Wheat:
    def __init__(self, name, scenario, shared_array, outputs_dirpath="outputs"):
        self.name = name
        self.shared_array = shared_array
        self.soil_grid = shared_array.np_array
        # TODO: Pass on the soil grid to the model so that it can execute get_from_voxel and apply_to_voxel,
        # methods to add in the Composite Model
        self.plant = Model(time_step=3600, **scenario)

        self.outputs_dirpath = outputs_dirpath

        self.logger = Logger(model_instance=self.plant, outputs_dirpath=os.path.join(self.outputs_dirpath, name),
                        time_step_in_hours=1,
                        logging_period_in_hours=24,
                        recording_images=False, plotted_property="C_hexose_root", show_soil=True,
                        recording_mtg=False,
                        recording_raw=False,
                        recording_sums=True,
                        recording_performance=True,
                        echo=True)

    def run(self):
        for _ in range(500):
            # Placed here also to capture mtg initialization
            self.logger()
            self.plant.run()

            self.shared_array.wait()

            self.shared_array.acquire_lock()
            # TODO
            self.plant.sync_with_voxels()
            self.shared_array.release_lock()


        self.logger.stop()
        analyze_data(outputs_dirpath=self.outputs_dirpath,
                     on_sums=True,
                     on_performance=True,
                     animate_raw_logs=False,
                     target_properties=[]
                     )


class Soil:
    def __init__(self, name, scenario, shared_array, outputs_dirpath="outputs"):
        self.name = name
        self.shared_array = shared_array
        self.soil_grid = shared_array.np_array

        # self.soil =

        self.outputs_dirpath = outputs_dirpath

        self.logger = Logger(model_instance=self.soil, outputs_dirpath=os.path.join(self.outputs_dirpath, name),
                             time_step_in_hours=1,
                             logging_period_in_hours=24,
                             recording_images=False, plotted_property="C_hexose_root", show_soil=True,
                             recording_mtg=False,
                             recording_raw=False,
                             recording_sums=True,
                             recording_performance=True,
                             echo=True)

    def run(self):
        for _ in range(500):
            # Placed here also to capture mtg initialization
            self.logger()
            self.soil.run()
            self.shared_array.wait()

        self.logger.stop()
        analyze_data(outputs_dirpath=self.outputs_dirpath,
                     on_sums=True,
                     on_performance=True,
                     animate_raw_logs=False,
                     target_properties=[]
                     )


class Scene:

    def __init__(self, simulation_length=500, dt=3600, dx=0.3, dy=0.3, dz=1, voxel_widht=0.01, voxel_height=0.01):
        scenarios = ms.from_table(file_path="inputs/Scenarios.xlsx", which=["WB1"])
        for scenario_name, scenario in scenarios.items():
            manager = mp.Manager()
            self.model_instances_dict = manager.dict()

            self.models = {"Soil": Soil, "Plant1": Wheat, "Plant2": Wheat}

            # to define from inputs, and then pass on to the models, including soil
            shared_array = SharedArray((3, 3, 3), len(self.models))

            # Initialize model instances for each process
            processes = []
            for name, ModelClass in self.models:
                p = mp.Process(target=self.initialize_model, args=(self.model_instances_dict,
                                                              ModelClass, name, scenario, shared_array, os.path.join("outputs", str(scenario_name))))
                p.start()
                processes.append(p)

            for p in processes:
                p.join()

    def initialize_model(self, instance_dict, ModelClass, name, scenario, shared_array, output_dirpath):
        instance_dict[name] = ModelClass(name=name, scenario=scenario, shared_array=shared_array,
                                         outputs_dirpath=output_dirpath)

    def run_model(self, name, instance_dict):
        model = instance_dict[name]
        model.run()

    def play(self):
        # Run the models in separate processes
        processes = []
        for name in self.models.keys():
            p = mp.Process(target=self.run_model, args=(name, self.model_instances_dict))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()


Scene().play()
