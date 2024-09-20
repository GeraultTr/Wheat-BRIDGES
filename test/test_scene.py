# Public packages


# Model packages
from wheat_bridges.rhizospheric_soil import RhizosphericSoil
from wheat_bridges.wheat_bridges import WheatBRIDGES

# Utility packages
from initialize.initialize import MakeScenarios as ms
from metafspm.scene_wrapper import SceneWrapper
#from log.logging import Logger
#from analyze.analyze import analyze_data


if __name__ == "__main__":
    scenarios = ms.from_table(file_path="inputs/Scenarios_24-09-13.xlsx", which=["WB6"])
    scene = SceneWrapper(scene_name="Test_scene", planting_pattern=SceneWrapper.planting_pattern, plant_models=[WheatBRIDGES], plant_scenarios=[scenarios["WB6"]], soil_model=RhizosphericSoil)

    for _ in range(2):
        scene.play()

    scene.close()
