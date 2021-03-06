sudo apt-get install p7zip-full

mkdir data
cd data

echo "Downloading Annotations"
wget https://zenodo.org/record/3723295/files/annotations.csv

for i in 0 1 2 3 4 5 6
do
  echo 'Downloading subset$i'
  wget https://zenodo.org/record/3723295/files/subset$i.zip
  7z x subset$i.zip
  rm subset$i.zip
  cd ..
  python preprocess_frcnn.py --data=./data --output=../luna_train --num_processes=4
  cd data
  rm -rf subset$i
done