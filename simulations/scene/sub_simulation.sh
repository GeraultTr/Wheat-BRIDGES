#!/bin/bash

### Les commentaires qui commencent par �#$� sont interpr�t�s par SGE comme des options en ligne ###
### ce script est un exemple, il est n�cessaire de le modifier pour l'adapter � vos besoins ###

# Shell � utiliser pour l'ex�cution du job
#$ -S /bin/bash

# Nom du job
#$ -N wb_krfvx6_2

# Nom de la queue
#$ -q short.q
# -q long.q
# -q highmem.q

# Sélection d'un noeud particulier (commented)
# -l hostname=n12

# Sortie standard (already handled by python)
#$ -o /home/tigerault/work/Wheat-BRIDGES_framework/Wheat-BRIDGES/simulations/scene/outputs/output.out

# Sortie d�erreur (already handled by python)
#$ -e /home/tigerault/work/Wheat-BRIDGES_framework/Wheat-BRIDGES/simulations/scene/outputs/errors.err

# Mail
#$ -m ea
#$ -M tristan.gerault@inrae.fr

# Lance la commande depuis le r�pertoire o� est lanc� le script
#$ -cwd

# Utiliser n CPUs
#$ -pe thread 10

# Python

conda activate wheat-bridges
python -m simulation_density
conda deactivate