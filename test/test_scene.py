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


class RhizosphericSoil:
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


### metafspm zone

class SceneWrapper:

    planting_pattern = dict(
        pattern_name = "rows",
        inter_rows = 0.2,
        density = 100,
        pattern_model_alternance=1,
        sowing_depth=[0.]
    )

    def __init__(self, scenario_name, scenario, planting_pattern = planting_pattern, simulation_length=500,
                 dt=3600, dx=0.3, dy=0.3, dz=1,
                 voxel_widht=0.01, voxel_height=0.01):

        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.time_step = dt

        manager = mp.Manager()
        self.plant_instances_dict = manager.dict()
        self.environment_instances_dict = manager.dict()

        self.plant_models = (Wheat,)
        self.environment_models = {"Soil": Soil, "Atmosphere": None}

        planting_sequence = self.planting_initialization(pattern=planting_pattern, plant_models=self.plant_models)
        self.plant_ids = [plant["plant_ID"] for plant in planting_sequence]

        # to define from inputs, and then pass on to the models, including soil
        shared_soil = manager.dict()
        shared_atmosphere = ()

        scenario["input_soil"] = shared_soil
        scenario["input_atmosphese"] = shared_atmosphere

        # Initialize model instances for each plant
        processes = []
        for plant in planting_sequence:
            p = mp.Process(target=self.initialize_model, args=(self.model_instances_dict,
                                                          plant["model"], plant["plant_ID"], scenario, plant["coordinates"]))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

    def initialize_model(self, instance_dict, ModelClass, name, scenario, coordinates, shared_array, output_dirpath):
        instance_dict[name] = ModelClass(name=name, scenario=scenario, coordinates=coordinates)

    def planting_initialization(self, pattern, plant_models):
        unique_plant_ID = 0
        planting_sequence = []
        row_number = int(self.dx / pattern["inter_rows"])
        number_per_row = int(self.dy * pattern["density"] / row_number)
        intra_row_distance = 1. / number_per_row
        current_model_index = -1
        for x in range(row_number):
            alternance = x % pattern["pattern_model_alternance"]
            if alternance == 0:
                current_model_index = (current_model_index + 1) % len(plant_models)
            for y in range(number_per_row):
                planting_sequence += [dict(model=plant_models[current_model_index],
                                            plant_ID=unique_plant_ID,
                                            coordinates=[x*pattern["inter_rows"],
                                                        y*intra_row_distance,
                                                        pattern["sowing_depth"][current_model_index]])]

        return planting_sequence

    def run_model(self, name, instance_dict):
        model = instance_dict[name]
        model.run()

    def play(self):
        # DO the same thing but with environmental models

        # Run the models in separate processes
        processes = []
        for name in self.plant_ids:
            p = mp.Process(target=self.run_model, args=(name, self.model_instances_dict))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()


Scene().play()
