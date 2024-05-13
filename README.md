# Wheat-BRIDGES

Wheat-BRIDGES is a new Wheat model simulating architectured growth and spatial nutrition by interacting different organ-scale models (blade, sheath, hidden zones, vessels, root segments).  

This model was the result of a coupling strategy, caried out under the OpenAlea platform, sharing the variables of 4 existing models :
- The CN-Wheat model (Barillot et al., 2016, https://doi.org/10.1093/aob/mcw143)
- The Rhizodep model (Rees et al., in prep)
- The Root-CyNAPS (Gerault et al., in prep)
- A python implementation of the RothC soil model

## Installation

Prerequisites to installation :
- miniconda (https://docs.anaconda.com/free/miniconda/miniconda-install/) 
- git (https://git-scm.com/downloads)

1) In a terminal, optionally install mamba for faster installation
```
conda install -y -c conda-forge mamba
```

2) Then, clone this repository and its unpackages dependancies in the desired location :
```
git clone --recurse-submodules https://github.com/GeraultTr/Wheat-BRIDGES.git
git clone https://github.com/GeraultTr/metafspm.git
git clone --recurse-submodules https://github.com/GeraultTr/data_utility.git
cd wheat-bridges
```

2bis. (OPTIONAL) Only for Windows users, caribu needs to be installed manually :
- in the requirements_minimal, uncomment "openalea.sconsx", "m2w64-toolchain" and comment "alinea.caribu"
- then clone https://github.com/openalea-incubator/caribu.git
- cd to folder and run "scons" to build it
- then run 
```
python -m setup.py install
```
Then continue bellow steps


3) Install packaged dependancies with : 
```
mamba create -n wheat-bridges -c conda-forge -c openalea3 --strict-channel-priority --file requirements_minimal.txt
mamba activate wheat-bridges
```

4) Finally, setup the locally unpackaged dependancies : 
```
cd .../wheat-bridges
python -m multisetup.py develop
cd .../metafspm
python -m setup.py develop
cd .../data_utility
python -m multisetup.py develop
```
