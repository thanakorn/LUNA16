mkdir data
cd data

echo "Downloading Annotations"
wget https://zenodo.org/record/3723295/files/annotations.csv?download=1 -O annotations.csv

for i in {0..1}
do
  echo "Downloading subset$i"
  wget "https://zenodo.org/record/3723295/files/subset$i.zip?download=1 -O subset$i.zip"
  unzip "subset$i.zip"
  rm "subset$i.zip"
done
