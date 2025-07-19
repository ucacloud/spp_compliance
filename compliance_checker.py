log_file_path = 'logs/example.log'

# Define violation patterns
violation_patterns = {
    "Failed Login": "Failed password",
    "invalid User": "Invalid user",
    "Privilege Escalation": "sudo",
    "Sensitive File Access": "/etc/shadow",
    "SSH Activity": "sshd"
}

with open(log_file_path, 'r') as file:
    for line in file:
        cleaned_line = line.strip()
        matched = False

        for violation_type, pattern in violation_patterns.items():
            if pattern in cleaned_line:
                print(f" [{violation_type}] {cleaned_line}")
                matched = True

        if not matched:
            print(f" [OK] {cleaned_line}")
