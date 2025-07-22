import re

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

# Output information to txt file in output folder

output_file_path = 'output/violation_report.txt'

with open(output_file_path, 'w') as outfile:
    outfile.write("Detailed Violations:\n")
    for v in violations:
        outfile.write(f"Line {v['line_number']} [{v['timestamp']}] [{v['log_level']}] [{v['violation_type']}]: {v['description']}\n")

    outfile.write("\nSummary of Violations:\n")
    for v_type, count in violation_counts.items():
        outfile.write(f"{v_type}: {count}\n")

print(f"\nReport saved to {output_file_path}")
