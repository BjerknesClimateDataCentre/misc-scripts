#!/bin/bash

SOCAT_VERSION="SOCATv2019"

# URL Prefixes
SYTHESIS_PREFIX="https://www.ncei.noaa.gov/archive/archive-management-system/OAS/bin/prd/jquery/accession/0190072/data/0-data"
GRIDDED_PREFIX="https://accession.nodc.noaa.gov/0190072/data/0-data/SOCATv2019_Gridded_Dat"

# Filenames (exclude the SOCATvxxxx prefix -
# the script will use SOCAT_PREFIX defined above)
declare -a SYNTHESIS_FILES=(
  "Arctic.tsv"
  "Coastal.tsv"
  "Indian.tsv"
  "NorthAtlantic.tsv"
  "NorthPacific.tsv"
  "SouthernOceans.tsv"
  "TropicalAtlantic.tsv"
  "TropicalPacific.tsv"
  "FlagE.tsv"
  )

declare -a GRIDDED_FILES=(
  "tracks_gridded_monthly.nc"
  "tracks_gridded_yearly.nc"
  "tracks_gridded_decadal.nc"
  "qrtrdeg_gridded_coast_monthly.nc"
  )

# Other URLs to download
declare -a OTHER_URLS=(
  "http://store.pangaea.de/Publications/SOCATv2019/SOCATv2019All_SOCATFormatDoc.zip"
  )

echo "Processing synthesis files..."
for i in "${SYNTHESIS_FILES[@]}"
do
  filename="${SOCAT_VERSION}_${i}"
  wget -O "$filename" "${SYTHESIS_PREFIX}/${filename}"
  zip "${filename}.zip" "$filename"
  rm "$filename"
done

alldatafile="${SOCAT_VERSION}.tsv"
alldataurl="${SYTHESIS_PREFIX}/${alldatafile}"
zip "${alldatafile}.zip" "$alldatafile"
rm "$alldatafile"

echo "Processing gridded files..."
for i in "${GRIDDED_FILES[@]}"
do
  filename="${SOCAT_VERSION}_${i}"
  wget -O "$filename" "${GRIDDED_PREFIX}/${filename}"
  zip "${filename}.zip" "$filename"
  rm "$filename"
done

echo "Downloading other files..."
for i in "${OTHER_URLS[@]}"
do
  wget "$i"
done
