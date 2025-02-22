import json
from typing import List, Dict, Generator


class FileReader:
    @staticmethod
    def read_csv_file(file_path: str, skip_header=True) -> Generator[List[str], None, None]:
        """Read a CSV file line by line, optionally skipping the header."""
        try:
            with open(file_path, 'r') as file:
                if skip_header:
                    next(file)  # Skip the header line
                for line in file:
                    yield line.strip().split(',')
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            raise Exception(f"Error reading file {file_path}: {str(e)}")

    @staticmethod
    def read_json_lines_file(file_path: str) -> Generator[Dict, None, None]:
        """Read a JSON Lines file where each line is a JSON dictionary."""
        try:
            with open(file_path, 'r') as file:
                # Remove the square brackets and split into lines
                data = file.read().strip('').split(',\n')
                for line_number, line in enumerate(data, 1):
                    line = line.strip()
                    if not line:  # Skip empty lines
                        continue
                    try:
                        yield json.loads(line)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Invalid JSON on line {line_number}: {str(e)}\nLine content: {line}")
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            raise Exception(f"Error reading file {file_path}: {str(e)}")