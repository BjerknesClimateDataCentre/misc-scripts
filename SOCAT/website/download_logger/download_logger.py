'''
Download logger main script

- Import the SOCAT log file(s)
- Identifies new and relevant download requests
- Share the download information with CP

Camilla S. Landa 2022-03-09
'''

import os
import logging
import json
import gzip
from datetime import datetime

if not os.path.isdir('script_log'): os.mkdir('script_log')
logging.basicConfig(filename = 'script_log/debug.log',
	format = '%(asctime)s %(levelname)-8s %(message)s',
	level = logging.DEBUG)

SOCAT_LOG_DIR = './socat_log_files'
SOCAT_LOG_TIME_FORMAT = "%d/%b/%Y:%H:%M:%S"

TEST_MODE = True # If False, info is sent to CP and the cutoff string is updated

def extract_timestamp(line, as_datetime = True):
	''' Extract the timestamp from a log line
	Return the timestamp as datetime or string type
	'''
	request_split = line.split(' - - [')[1]
	first_timestamp_full = request_split.split('] ')[0]
	first_timestamp = first_timestamp_full.split(' ')[0]
	if (as_datetime is True):
		first_timestamp = datetime.strptime(first_timestamp,
			SOCAT_LOG_TIME_FORMAT)
	return(first_timestamp)

def main():
	logging.info('***** Starting download logger script *****')

	with open ('./stored_info.json', 'r') as stored_info_file:
		all_stored_info = json.load(stored_info_file)
	cutoff_string = all_stored_info['cutoff_string']
	cutoff_timestamp = datetime.strptime(cutoff_string, SOCAT_LOG_TIME_FORMAT)

	''' List all socat log files and sort them from newest to oldest
	The file names contain timestamp yyyymmdd of the last log, and so reversed
	alphabetic sorting orders the files from newest to oldest. Exception: the
	newest log file does not contain timestamp and has to be moved to the front
	'''
	log_files = os.listdir(SOCAT_LOG_DIR)
	log_files_sorted = sorted(log_files, reverse = True)
	log_files_sorted.insert(0, log_files_sorted.pop())

	# Import all relevant log files and store their content in 'lines'
	lines = []
	for file in log_files_sorted:
		if '.gz' in file:
			with gzip.open(os.path.join(SOCAT_LOG_DIR, file), 'rt') as log_file:
				new_lines = log_file.readlines()
		else:
			with open(os.path.join(SOCAT_LOG_DIR, file)) as log_file:
				new_lines = log_file.readlines()

		# Append new log lines to 'lines' in chronological order
		for new_line in reversed(new_lines):
			lines.insert(0, new_line)

		# Stop loop if get to logs older than the cutoff timestamp
		first_timestamp = extract_timestamp(new_lines[0])
		if cutoff_timestamp >= first_timestamp:
			break

	for line in lines:

		# Identify download requests (v2021 and onwards) after cutoff timestamp
		match_words = ['GET', '/socat_files/', 'zip']
		ignore_versions = ['v6', 'v2019', 'v2020']
		current_timestamp = extract_timestamp(line)
		if (all(word in line for word in match_words) and
			all(version not in line for version in ignore_versions) and
			current_timestamp > cutoff_timestamp ):

			IP_adress = line.split(' - - ')[0]
			request_string = line.split('"')[1]
			request_list = request_string.split("/")
			version = request_list[2]
			filename = request_list[3].split('.zip')[0]

			if (TEST_MODE is True):
				print(IP_adress, version, filename)

			#if (TEST_MODE is False):
				# !!! Share IP_adress, version and filename with CP

	# Update the cutoff timestamp
	if (TEST_MODE is False):
		all_stored_info['cutoff_string'] = extract_timestamp(lines[-1],
			as_datetime = False)
		with open ('./stored_info.json', 'w') as stored_info_file:
			 json.dump(all_stored_info, stored_info_file)

if __name__ == '__main__':
	main()