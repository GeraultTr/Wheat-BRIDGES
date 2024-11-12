# Related to Root-BRIDGES
cd Root_BRIDGES
cd root_cynaps
git pull origin main
cd ..
cd rhizodep
git pull origin main
cd ..
git pull origin main
cd ..
git pull origin main

# Related to WheatFspm
cd WheatFspm
cd adel
git pull origin master
cd ..
cd cn-wheat
git pull origin main
cd ..
cd elong-wheat
git pull origin master
cd ..
cd farquhar-wheat
git pull origin main
cd ..
cd fspm-wheat
git pull origin main
cd ..
cd growth-wheat
git pull origin master
cd ..
cd respi-wheat
git pull origin master
cd ..
cd senesc-wheat
git pull origin master
cd ..
git pull origin master
cd ..

# Optionnal, only if data_utility is in the same folder as Wheat-BRIDGES
cd ..
cd data_utility
cd initialize
git pull origin main
cd ..
cd log
git pull origin main
cd ..
cd analyze
git pull origin main
cd ..
git pull origin main