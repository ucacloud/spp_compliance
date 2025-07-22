import re
import os
import csv
from datetime import datetime

log_file_path = 'logs/example_log.txt'

# Define violation patterns
violation_patterns = {
    "Failed Login": "Failed password",
    "invalid User": "Invalid user",
    "Privilege Escalation": "sudo",
    "Sensitive File Access": "/etc/shadow",
    "SSH Activity": "sshd"
}

# Map violation types to log levels
log_levels = {
    "Failed Login": "ERROR",
    "Invalid User": "WARNING",
    "Privilege Escalation": "CRITICAL",
    "Sensitive File Access": "CRITICAL",
    "SSH Activity": "INFO"
}

violations = [] #List that stores violation records

# Regex to capture timestamp at start of line (e.g. 'Jul 30 10:02:11')
timestamp_regex = re.compile(r'^[A-Z][a-z]{2} +\d{1,2} +\d{2}:\d{2}:\d{2}')

with open(log_file_path, 'r') as file:
    for line_number, line in enumerate(file, start=1):
        cleaned_line = line.strip()

        timestamp_match = timestamp_regex.match(cleaned_line)
        timestamp = timestamp_match.group(0) if timestamp_match else "Unknown"

        for violation_type, pattern in violation_patterns.items():
            if pattern in cleaned_line:
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
txt_output_dir = 'output/txt'
os.makedirs(txt_output_dir, exist_ok=True)

#Generate timestamped txt filename
txt_filename = f"{txt_output_dir}/violation_report_{timestamp}.txt"

with open(txt_filename, 'w') as outfile:
    outfile.write("Detailed Violations:\n")
    for v in violations:
        outfile.write(f"Line {v['line_number']} [{v['timestamp']}] [{v['log_level']}] [{v['violation_type']}]: {v['description']}\n")

    outfile.write("\nSummary of Violations:\n")
    for v_type, count in violation_counts.items():
        outfile.write(f"{v_type}: {count}\n")

print(f"\nReport saved to {txt_filename}")

#Create csv subfolder if it doesn't exist
csv_output_dir = 'output/csv'
os.makedirs(csv_output_dir, exist_ok=True)

#Generate timestamped csv filename
csv_filename = f"{csv_output_dir}/violation_report_{timestamp}.csv"

#Write violations to csv
with open(csv_filename, mode='w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['line_number', 'timestamp', 'log_level', 'violation_type', 'description']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for violation in violations:
        writer.writerow(violation)

print(f"\nCSV report saved to: {csv_filename}")