log_file_path = 'logs/example_log.txt'

# Define violation patterns
violation_patterns = {
    "Failed Login": "Failed password",
    "invalid User": "Invalid user",
    "Privilege Escalation": "sudo",
    "Sensitive File Access": "/etc/shadow",
    "SSH Activity": "sshd"
}

violations = [] #List that stores violation records

with open(log_file_path, 'r') as file:
    for line_number, line in enumerate(file, start=1):
        cleaned_line = line.strip()

        for violation_type, pattern in violation_patterns.items():
            if pattern in cleaned_line:
                violations.append({
                    "line_number": line_number,
                    "violation_type": violation_type,
                    "description": cleaned_line
                })

for v in violations:
    print(f"Line {v['line_number']}: [{v['violation_type']}] {v['description']}")

print("\nSummary of Violations:") #Creates a summary of the violations
violation_counts = {}

for v in violations:
    violation_type = v["violation_type"]
    violation_counts[violation_type] = violation_counts.get(violation_type, 0) + 1

for v_type, count in violation_counts.items():
    print(f"{v_type}: {count}")
