# Wheat-BRIDGES: Biogeochemical Rhizospherous Integration by Development and Growth of Environmental Signals applied to a whole plant of wheat

A whole plant FSPM vs heterogeneous environment models to study the plastic response of the plant arising from the variability of local organs functioning

## Software

### Authors
Tristan Gérault, Christophe Pradal, Romain Barillot, Marion Gauthier, Alexandra Jullien, Frédéric Rees

### Institutes

INRAE / AgroParisTech / CIRAD / INRIA

### License

CecILL-C

Python package

**URL** (Not available yet): <https://wheat-bridges.rtfd.io>

## About



### *Wheat-BRIDGES* presentation

Wheat-BRIDGES is a new *Triticum aestivum* Functional-Structural Plant Model (FSPM) simulating C, N, water, anatomy and growth in each vegetative tissue of the plant architecture. It simulates the heterogeneity of organs' transport and metabolism along plant architecture in response to local plant growth processes and complex environmental gradients, enabling to estimate and decompose plant C&N balance from local activities. 

This model was the result of a coupling strategy, to build on the complementary processes already represented in 3 existing models:
- The *CN-Wheat* model ([Barillot et al. 2016](https://doi.org/10.1093/aob/mcw143) and [Gauthier et al. 2020](https://doi.org/doi.org/10.1093/jxb/eraa276))
- The *RhizoDep* model ([Rees et al. 2025](https://doi.org/10.1007/s11104-025-07766-z))
- The *Root-CyNAPS* model (Gerault et al., submited, model available at https://github.com/openalea/Root-CyNAPS)

Additionally, to explore the capabilities of the *Wheat-BRIDGES* model to study the plasticity of the plant under heterogeneous environmental conditions, it was coupled with 3D light and soil models. 
- *Wheat-BRIDGES* reuses the *Caribu* model ([Chelle and Andrieu 1998](https://doi.org/10.1016/S0304-3800(98)00100-8)) to compute heterogeneous light interception between individual photosynthetic organs. An alternative, VirtualPlantLab's Raytrace ([Morales et al. 2025](https://doi.org/10.1093/insilicoplants/diaf005)) was also coupled to the model to enable the simulation phytotronic chambers of greenhouse light environments.
- For the soil compartment, two existing models were coupled to yield a 3D model of CN biochemistry and water-solute transport: the *MIMICS-CN* v1.0 model ([Kyker-Snowman et al. 2020](https://doi.org/10.5194/gmd-13-4413-2020)) and the *CMF* model ([Kraft et al. 2011](https://doi.org/10.1016/j.envsoft.2010.12.009)). This coupling enables to study the multiscale C-N-W interactions between plant and soil. Coupling with soil temperature models are also considered, since the Wheat-BRIDGES include regulations of local organ's activities by local temperature (See https://github.com/openalea-incubator/soiltemp).


This coupling of plant and environment models was performed in the Openalea Platform using the *MetaFSPM* toolkit (https://github.com/openalea/metafspm), a generic FSPM coupling and execution package which provided utilities to modularize existing models, expose their input data for coupling, manage the execution of the network of coupled models and 

### Example outputs

First Wheat-BRIDGES simulation evidenced the existence of active root zones in the root system near root tips and during the emergence of lateral roots. The contribution of these active zones to plant balance was shown to cause complex variations of total rhizodeposition and N uptake, advocating to further study the regulations between the emergence of these active zones. The variation of these root-soil exchanges along root system architecture and over time can be visualized here: https://geraulttr.github.io/AR_glb_viewer/index.html

## Usage

After installation, begin by familiarising with an example execution of the model under simulations/examples/scene/simulation.py

Simply run this example by 
1) activating your environment with ```mamba activate wheat-bridges```
2) ```cd ./simulations/examples/scene``` into the example folder of this repo
3) run the model with the python interpreter installed in this environment ```python -m simulation```

To design a simulation scenario, simply edit the configuration of the simulation with the PlayOrchestra function. For example, after importing models, the Logger and the scenario:
```python
play_Orchestra(scene_name="scenario_name_here", output_folder="outputs", plant_models=[WheatBRIDGES], plant_scenarios=[scenario], soil_model=RhizoSoil, soil_scenario=scenario, 
light_model=LightModel, translator_path=openalea.wheatbridges.__path__[0], logger_class=Logger, log_settings=Logger.heavy_log, scene_xrange=0.15, scene_yrange=0.15, sowing_density=250, row_spacing=0.15, time_step=3600, n_iterations=2500)
```

To change model parameters, simply modify the parametrization file "scenario_***.xlsx" in the input simulations/example/scene/inputs/folder, 


### Installation options

#### User Docker Installation (Eazy and Smaller on disk)

*Available soon*


#### User Conda Installation (Available Soon)

*Available soon*


#### Developer Installation 
**Prerequisites to installation:**
- miniconda (https://docs.anaconda.com/free/miniconda/miniconda-install/) 
- git (https://git-scm.com/downloads)

On all systems, a script has been written to automate the installation which still remains complex while the model is not packaged in conda or provided as a container image. Just open a terminal, cd into the desired installation directory, and run the following commands:
```
mkdir Wheat-BRIDGES_framework
cd Wheat-BRIDGES_framework

git clone -b debug_advection git@github.com:openalea/Root-CyNAPS.git
git clone -b release2025 git@github.com:openalea/metafspm.git
git clone -b release2025 git@github.com:openalea/fspm-utility.git
git clone -b develop_tristan git@github.com:openalea/rhizodep.git
git clone -b main git@github.com:GeraultTr/RhizoSoil.git
git clone -b munch git@github.com:GeraultTr/Root_BRIDGES.git
git clone --recurse-submodules -b main git@github.com:GeraultTr/Wheat-BRIDGES.git

cd Wheat-BRIDGES
mamba create -n wheat-bridges -f ./conda/environment.yaml -y
mamba activate wheat-bridges
pip install -e .
cd WheatFspm
git checkout master
python -m multisetup develop
cd ..
cd ..

cd Root-CyNAPS
pip install -e .
cd ..

cd metafspm
pip install -e .
cd ..

cd fspm-utility
pip install -e .
cd ..

cd rhizodep
pip install -e .
cd ..

cd RhizoSoil
pip install -e .
cd ..

cd Root_BRIDGES
pip install -e .
cd ..

echo Installation finished
```

For linux users only, an additional installation is necessary to render 3D outputs off-screen. It is installed with:
```
sudo apt install -y libgl1-mesa-glx xvfb
```


#### Requirements installed by Root-CyNAPS

> -   openalea.mtg
> -   openalea.plantgl
> -   openalea.metafspm
> -   openalea.fspmutility
> -   openalea.rootcynaps
> -   pandas
> -   numpy
> -   scipy
> -   pyyaml
> -   xarray
> -   pyvista
> -   matplotlib
> -   pint
> -   trimesh
> -   salib


## Documentation

Link not available yet

## Citations


## Contributors

<a href="https://github.com/geraulttr/wheat-bridges/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=geraulttr/wheat-bridges" />
</a>