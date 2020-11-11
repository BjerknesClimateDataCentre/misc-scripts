# Convert a TSG file into a CSV file.
# Strips off all the headers, creates an ISO standard Timestamp column,
# and leaves all other columns as they are.
#
# TSG files have two ways of specifying the time:
# 1. Hours from the start of the file (with start_time specified in the header)
# 2. UNIX timestamp
#
# Both types are handled.
#
# Usage: python tsg2csv <filename> <hours|unix>
# Creates a file named <filename>.csv in the current directory.
#
# Output CSV files do not have headers
#
import sys
import os.path
import re
from datetime import datetime, timedelta
import math

HOURS_MODE = 0
UNIX_MODE = 1

HEADER_END = "*END*"

def main(filename, mode):

  start_time = None
  in_header = True

  with open(f'{filename}.csv', 'w') as out:
    with open(filename, 'r') as f:
      line = f.readline().strip()

      while line:
        if 'start_time' in line:
          start_time = extract_start_time(line)
        if in_header:
          if line == HEADER_END:
            in_header = False
            if mode == HOURS_MODE and start_time is None:
              print('Did not find start_time in header')
              exit()
        else:
          # Split into fields
          fields = re.sub('  *', ' ', line).split()

          # Calculate the line's timestamp
          line_time = None

          if mode == HOURS_MODE:
            line_time = calc_time(start_time, float(fields[3]))
          elif mode == UNIX_MODE:
            line_time = datetime.fromtimestamp(int(fields[1]))

          fields.insert(0, line_time.strftime('%Y-%m-%dT%H:%M:%SZ'))
          out.write(','.join(fields))
          out.write('\n')

        line = f.readline().strip()


def extract_start_time(line):
  pattern = re.compile(r'.*start_time = (.*) \[')
  match = pattern.match(line)
  timestring = match.group(1)
  return datetime.strptime(timestring, '%b %d %Y %H:%M:%S')

def calc_time(start_time, hours):
  wholehours = math.trunc(hours)
  seconds = math.trunc((hours - wholehours) * 3600) + wholehours * 3600
  return start_time + timedelta(seconds=seconds)

def usage():
  print('Usage: python tsg2csv <filename> <hours|unix>')
  exit()

if __name__ == '__main__':
  filename = None
  mode = None

  if len(sys.argv) != 3:
    usage()

  filename = sys.argv[1]
  modestring = sys.argv[2]
  if modestring == 'hours':
    mode = HOURS_MODE
  elif modestring == 'unix':
    mode = UNIX_MODE
  else:
    usage()

  main(filename, mode)