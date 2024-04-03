# Description

## Installation

Prerequisites to installation :
- miniconda (https://docs.anaconda.com/free/miniconda/miniconda-install/) 
- git (https://git-scm.com/downloads)

In a terminal, optionally install mamba for faster installation
```
conda install -y -c conda-forge mamba
```

Then, clone this repository and its unpackages dependancies in the desired location :
```
git clone --recurse-submodules https://github.com/GeraultTr/Wheat-BRIDGES.git
git clone https://github.com/GeraultTr/metafspm.git
git clone --recurse-submodules https://github.com/GeraultTr/data_utility.git
cd wheat-bridges
```

Then, install packaged dependancies with : 
```
mamba create -n wheat-bridges -c conda-forge -c openalea3 --strict-channel-priority --file requirements_minimal.txt
mamba activate wheat-bridges
```

Finally, setup the locally unpackaged dependancies : 
```
cd .../wheat-bridges
python -m multisetup.py develop
cd .../metafspm
python -m setup.py develop
cd .../data_utility
python -m multisetup.py develop
```
