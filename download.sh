sudo apt-get install p7zip-full

mkdir data
cd data

echo "Downloading Annotations"
wget https://zenodo.org/record/3723295/files/annotations.csv

for i in 1
do
  echo 'Downloading subset$i'
  wget https://zenodo.org/record/3723295/files/subset$i.zip
  7z subset$i.zip
  # rm subset$i.zip
done
