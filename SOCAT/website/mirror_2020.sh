#!/bin/bash

SOCAT_VERSION="SOCATv2020"

# URL Prefixes
SYTHESIS_PREFIX="https://www.ncei.noaa.gov/data/oceans/ncei/ocads/data/0210711"
GRIDDED_PREFIX="https://www.ncei.noaa.gov/data/oceans/ncei/ocads/data/0210711/SOCATv2020_Gridded_Dat"

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
  "tracks_gridded_monthly.csv"
  "tracks_gridded_yearly.nc"
  "tracks_gridded_yearly.csv"
  "tracks_gridded_decadal.nc"
  "tracks_gridded_decadal.csv"
  "qrtrdeg_gridded_coast_monthly.nc"
  "qrtrdeg_gridded_coast_monthly.csv"
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

