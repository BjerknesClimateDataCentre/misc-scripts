# Take in a standard General Oceanics data file and add an ISO date
# column on the front, based on the PC Date/PC Time columns.
#
# Assumes one header line.
#
# Outputs a new file in the current directory where
# input.txt -> input.isodate.txt
#
import sys
import os.path
import re
from datetime import datetime
import math

def main(filename):

  start_time = None
  in_header = True

  with open(f'{os.path.splitext(filename)[0]}.isodate.txt', 'w') as out:
    with open(filename, 'r') as f:

      # Header line
      headerline = f.readline().strip()
      out.write(f'ISO Date\t{headerline}')

      fields = headerline.split('\t')
      date_index = fields.index('PC Date')
      time_index = fields.index('PC Time')

      line = f.readline().strip()

      while line:
        fields = line.split('\t')
        date = fields[date_index]
        time = fields[time_index]

        linetime = datetime.strptime(f'{date} {time}', '%d/%m/%y %H:%M:%S')
        isodate = linetime.strftime('%Y-%m-%dT%H:%M:%SZ')
        out.write(f'{isodate}\t{line}\n')

        line = f.readline().strip()

def usage():
  print('Usage: python go_add_iso_date.py <filename>')
  exit()

if __name__ == '__main__':
  filename = None
  mode = None

  if len(sys.argv) != 2:
    usage()

  filename = sys.argv[1]

  main(filename)