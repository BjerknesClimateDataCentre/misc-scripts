"""
Concert SOCAT enhanced format files for ingestion into Carbon Portal as OTC L2 datasets.

This takes files extracted from SOCAT synthesis files, NOT the enhanced TSV files.
It expects TSV values with a single header line.
"""
import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timezone


def main(in_file, out_file):
  # Create the destination dataframe
  output = pd.DataFrame(columns=[\
    'Date/Time',\
    'Expocode',\
    'Longitude',\
    'Latitude',\
    'Depth [m]',\
    'version',\
    'QC_Flag',\
    'P_sal [psu]',\
    'Temp [degC]',\
    'Temperature of Equilibration [degC]',\
    'Atmospheric Pressure [hPa]',\
    'Equilibrator Pressure (absolute) [hPa]',\
    'WOA_SSS',\
    'NCEP_SLP [hPa]',\
    'ETOPO2_depth [m]',\
    'dist_to_land [km]',\
    'GVCO2 [umol/mol]',\
    'CO2 Mole Fraction [umol mol-1]',\
    'xCO2water_SST_dry [umol/mol]',\
    'pCO2 In Water - Equilibrator Temperature [uatm]',\
    'pCO2 [uatm]',\
    'fCO2water_equ_wet [uatm]',\
    'fCO2water_SST_wet [uatm]',\
    'fCO2 [uatm]',\
    'fCO2rec_src',\
    'fCO2 [uatm] QC Flag',\
    'pCO2 [uatm] QC Flag',\
    'P_sal [psu] QC Flag',\
    'Temp [degC] QC Flag'])

  # Load the input data
  data = pd.read_csv(in_file, sep='\t')

  # Copy the columns that don't need any changes
  output['Expocode'] = data['Expocode']
  output['Longitude'] = data['longitude [dec.deg.E]']
  output['Latitude'] = data['latitude [dec.deg.N]']
  output['Depth [m]'] = data['sample_depth [m]']
  output['version'] = data['version']
  output['QC_Flag'] = data['fCO2rec_flag']
  output['P_sal [psu]'] = data['sal']
  output['Temp [degC]'] = data['SST [deg.C]']
  output['Temperature of Equilibration [degC]'] = data['Tequ [deg.C]']
  output['Atmospheric Pressure [hPa]'] = data['PPPP [hPa]']
  output['Equilibrator Pressure (absolute) [hPa]'] = data['Pequ [hPa]']
  output['WOA_SSS'] = data['WOA_SSS']
  output['NCEP_SLP [hPa]'] = data['NCEP_SLP [hPa]']
  output['ETOPO2_depth [m]'] = data['ETOPO2_depth [m]']
  output['dist_to_land [km]'] = data['dist_to_land [km]']
  output['GVCO2 [umol/mol]'] = data['GVCO2 [umol/mol]']
  output['CO2 Mole Fraction [umol mol-1]'] = data['xCO2water_equ_dry [umol/mol]']
  output['xCO2water_SST_dry [umol/mol]'] = data['xCO2water_SST_dry [umol/mol]']
  output['pCO2 In Water - Equilibrator Temperature [uatm]'] = data['pCO2water_equ_wet [uatm]']
  output['pCO2 [uatm]'] = data['pCO2water_SST_wet [uatm]']
  output['fCO2water_equ_wet [uatm]'] = data['fCO2water_equ_wet [uatm]']
  output['fCO2water_SST_wet [uatm]'] = data['fCO2water_SST_wet [uatm]']
  output['fCO2 [uatm]'] = data['fCO2rec [uatm]']
  output['fCO2rec_src'] = data['fCO2rec_src']
  output['fCO2 [uatm] QC Flag'] = data['fCO2rec_flag']

  # Fixed columns (basically the QC flags, all set to 9 for Not QCed)
  output['pCO2 [uatm] QC Flag'] = 9
  output['P_sal [psu] QC Flag'] = 9
  output['Temp [degC] QC Flag'] = 9

  # And finally the timestamp, one row at at time
  for index, row in data.iterrows():
    timestamp = datetime(
      year=int(row['yr']),
      month=int(row['mon']),
      day=int(row['day']),
      hour=int(row['hh']),
      minute=int(row['mm']),
      second=int(row['ss']),
      tzinfo=timezone.utc)

    output.at[index, 'Date/Time'] = timestamp

  # Enforce data type on date/time column
  output['Date/Time'] = pd.to_datetime(output['Date/Time'])

  # Set all float columns to 3 decimal places
  for col in output.columns:
    if output[col].dtype == np.float64:
      output[col] = output[col].round(3)


  output.to_csv(out_file, index=False, na_rep='NaN', date_format='%Y-%m-%dT%H:%M:%SZ')

if __name__ == '__main__':
  in_file = None

  if len(sys.argv) != 2:
    print("Usage: python socat2cp.py <file>")
    exit()

  in_file = sys.argv[1]
  root, ext = os.path.splitext(in_file)
  out_file = f'{root}.SOCAT.csv'

  main(in_file, out_file)