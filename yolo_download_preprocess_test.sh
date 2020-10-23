sudo apt-get install p7zip-full

mkdir data
cd data

echo "Downloading Annotations"
wget https://zenodo.org/record/3723295/files/annotations.csv

for i in 7 8 9
do
  echo 'Downloading subset$i'
  wget https://zenodo.org/record/3723299/files/subset$i.zip
  7z x subset$i.zip
  rm subset$i.zip
  cd ..
  python preprocess_yolo.py --classes=./classes.names --data=./data --output=../luna_test --num_processes=4
  cd data
  rm -rf subset$i
done