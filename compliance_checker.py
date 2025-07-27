import argparse
import json
import os
import re
import time

from datetime import datetime

def load_config():
    with open('config/config.json', 'r') as config_file:
        return json.load(config_file)

def parse_log_file(log_file_path, violation_patterns, log_levels):
    timestamp_regex = re.compile(r'^[A-Z][a-z]{2} +\d{1,2} +\d{2}:\d{2}:\d{2}')
    violations = []

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
    return violations

def generate_summary(violations):
    summary = {}
    for v in violations:
        v_type = v["violation_type"]
        summary[v_type] = summary.get(v_type, 0) + 1
    return summary

def save_json_report(violations, output_dir='output/json'):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    json_path = os.path.join(output_dir,f'violations_{timestamp}.json')

    with open(json_path, 'w') as json_file:
        json.dump(violations, json_file, indent=2)

        print(f"Report saved to {json_path}")
        return json_path

def auto_delete_old_reports(folder_path, days_old=30):
    now = time.time()
    cutoff = now - (days_old * 86400)

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and os.path.getmtime(file_path) < cutoff:
            os.remove(file_path)
            print(f"Deleted old report: {file_path}")

def main():
    config = load_config()

    parser = argparse.ArgumentParser(description='Compliance Log Checker')
    parser.add_argument('--logfile',type=str, help='Path to the log file')
    args = parser.parse_args()

    log_file_path = args.logfile if args.logfile else config['log_file_path']
    violations = parse_log_file(log_file_path, config['violation_patterns'], config['log_levels'])

    summary = generate_summary(violations)

    #Console display
    for v in violations:
        print(f'Line {v['line_number']} [{v['timestamp']}] [{v['log_level']}] [{v['violation_type']}]: {v['description']}')
        print("n\Summary of Violations:")
        for v_type, count in summary.items():
            print(f"{v_type}: {count}")

    #Save JSON report
    save_json_report(violations)

    #Auto delete old reports
    auto_delete_old_reports('output/json')

    #Output JSON to stdout for Node to capture
    print("\n---Begin JSON Output---")
    print(json.dumps(violations, indent=2))
    print("---End JSON Output---")

if __name__ == "__main__":
    main()