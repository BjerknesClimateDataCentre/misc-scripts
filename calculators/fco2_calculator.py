# Take in a csv file, and add an fco2 column
# calculated from the data in that file.
#
# Asks which columns to use
import sys
import math
import os
import pandas as pd

def main(infile):
  df = pd.read_csv(infile)

  # Get the calculation columns
  temp_col = get_param_column('Temperature', df.columns)
  press_col = get_param_column('Pressure', df.columns)
  xco2_col = get_param_column('xCO2', df.columns)
  pco2_col = get_param_column('pCO2', df.columns)

  # Add fco2 column
  df['fco2'] = -1.0

  # Loop through each row and calculate
  for i, row in df.iterrows():
    temperature = row[temp_col]
    pressure = row[press_col]
    xco2 = row[xco2_col]
    pco2 = row[pco2_col]

    df.at[i, 'fco2'] = calc_fco2(temperature, pressure, xco2, pco2)

  root, extension = os.path.splitext(infile)
  outfile = f'{root}.fco2{extension}'
  df.to_csv(outfile, index=False)

def calc_fco2(temperature, pressure, xco2, pco2):
  kelvin = temperature + 273.15
  b = -1636.75 + 12.0408 * kelvin - 0.0327957 * pow(kelvin, 2) \
    + (3.16528 * 1e-5) * pow(kelvin, 3);
  delta = 57.7 - 0.118 * kelvin;

  return pco2 * math.exp(((b + 2 * pow(1 - xco2 * 1e-6, 2) * delta)
      * hPaToAtmospheres(pressure)) / (82.0575 * kelvin));

  return delta

def hPaToAtmospheres(hPa):
  return hPa * 100 * 0.00000986923266716013;

def get_param_column(parameter, columns):
  col = -1

  while col < 0:
    print()
    for i in range(0, len(columns)):
      print(f'  {i:>2d}: {columns[i]}')

    print(f'Enter {parameter} column number: ', end='')
    selection = input()
    if selection.isnumeric():
      if int(selection) > 0 and int(selection) < len(columns):
        col = int(selection)

  return col


def usage():
  print('Usage: python fco2_calculator.py <input_file>')
  exit()

if __name__ == '__main__':
  if len(sys.argv) != 2:
    usage()

  main(sys.argv[1])
