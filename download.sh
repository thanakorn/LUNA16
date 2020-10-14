mkdir data
cd data

echo "Downloading Annotations"
wget https://zenodo.org/record/3723295/files/annotations.csv?download=1 -O annotations.csv

echo "Downloading subset0"
wget https://zenodo.org/record/3723295/files/subset0.zip?download=1 -O subset0.zip
unzip subset0.zip
rm subset0.zip
