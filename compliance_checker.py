import argparse
import csv
import json
import os
import re
import time

from datetime import datetime

#Load config.json
with open('config/config.json', 'r') as config_file:
    config = json.load(config_file)

#CLI Argument parser to check different log files
parser = argparse.ArgumentParser(description='Compliane Log Checker')
parser.add_argument('--logfile', type=str, help='Path to the log file')
args = parser.parse_args()

#Use command line log file if provided, otherwise fall back to config
log_file_path = args.logfile if args.logfile else config['log_file_path']

violation_patterns = config['violation_patterns']
log_levels = config['log_levels']
txt_output_dir = config['txt_output_dir']
csv_output_dir = config['csv_output_dir']

violations = [] #List that stores violation records

# Regex to capture timestamp at start of line (e.g. 'Jul 30 10:02:11')
timestamp_regex = re.compile(r'^[A-Z][a-z]{2} +\d{1,2} +\d{2}:\d{2}:\d{2}')

with open(log_file_path, 'r') as file:
    for line_number, line in enumerate(file, start=1):
        cleaned_line = line.strip()

        timestamp_match = timestamp_regex.match(cleaned_line)
        timestamp = timestamp_match.group(0) if timestamp_match else "Unknown"

        for violation_type, pattern in violation_patterns.items():
            if re.search(pattern, cleaned_line):
                violations.append({
                    "line_number": line_number,
                    "timestamp": timestamp,
                    "violation_type": violation_type,
                    "log_level": log_levels[violation_type],
                    "description": cleaned_line
                })

for v in violations: #Prints detailed violations
    print(f"Line {v['line_number']} [{v['timestamp']}] [{v['log_level']}] [{v['violation_type']}]: {v['description']}")

print("\nSummary of Violations:") #Creates a summary of the violations
violation_counts = {}

for v in violations:
    violation_type = v["violation_type"]
    violation_counts[violation_type] = violation_counts.get(violation_type, 0) + 1

for v_type, count in violation_counts.items():
    print(f"{v_type}: {count}")

# Output to CSV and TXT

#Create safe timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")

#Create a txt subfolder if it doesn't exist
os.makedirs(txt_output_dir, exist_ok=True)

#Generate timestamped txt filename
txt_filename = os.path.join(txt_output_dir, f"violation_report_{timestamp}.txt")

with open(txt_filename, 'w') as outfile:
    outfile.write("Detailed Violations:\n")
    for v in violations:
        outfile.write(f"Line {v['line_number']} [{v['timestamp']}] [{v['log_level']}] [{v['violation_type']}]: {v['description']}\n")

    outfile.write("\nSummary of Violations:\n")
    for v_type, count in violation_counts.items():
        outfile.write(f"{v_type}: {count}\n")

print(f"\nReport saved to {txt_filename}")

#json output for Angular
json_output_path = os.path.join('output', 'json', f'violations_{timestamp}.json')
with open(json_output_path, 'w') as json_file:
    json.dump(violations, json_file, indent=2)

print(f"Report saved to {json_output_path}")

#Create csv subfolder if it doesn't exist
os.makedirs(csv_output_dir, exist_ok=True)

#Generate timestamped csv filename
csv_filename = os.path.join(csv_output_dir, f"violation_report_{timestamp}.txt")
#Write violations to csv
with open(csv_filename, mode='w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['line_number', 'timestamp', 'log_level', 'violation_type', 'description']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for violation in violations:
        writer.writerow(violation)

print(f"\nCSV report saved to: {csv_filename}")

#Auto delete reports older than 30 days
def auto_delete_old_reports(folder_path, days_old=30):
    now = time.time()
    cutoff = now - (days_old * 86400)

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            file_mtime = os.path.getmtime(file_path)
            if file_mtime < cutoff:
                os.remove(file_path)
                print(f"Deleted old report: {file_path}")

#Call the function for both subfolders
auto_delete_old_reports('output/csv')
auto_delete_old_reports('output/json')
auto_delete_old_reports('output/txt')