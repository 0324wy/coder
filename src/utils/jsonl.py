import json
import os

# Read an jsonl file and convert it into a python list of dictionaries.
def read_jsonl(filename):
    """Reads a jsonl file and yields each line as a dictionary"""
    lines = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            lines.append(json.loads(line))
    return lines

# Write a python list of dictionaries into a jsonl file
def write_jsonl(filename, lines):
    """Writes a python list of dictionaries into a jsonl file"""
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Write data to the file
    with open(filename, "w", encoding="utf-8") as file:
        for line in lines:
            file.write(json.dumps(line) + "\n")
