# Pharmacy Claims Processing System

This Python-based system processes pharmacy claims, reverts, and generates reports and recommendations based on the data.

## Features

* Processes pharmacy information from CSV files (e.g., `pharmacies.csv`).
* Processes claim and revert information from JSON Lines files (e.g., `claims.json`, `reverts.json`).
* Handles multiple input files for each data type.
* Utilizes multiprocessing for efficient parallel processing.
* Calculates metrics such as:
    * Count of claims
    * Count of reverts
    * Average unit price
    * Total price
* Make a recommendation for the top 2 Chain to be displayed for each Drug
    * Active claims for each pharmacy
    * Total revenue for each pharmacy
    * Drug distribution for each pharmacy
* Recommends top 2 chains with the lowest average unit price per drug.
* Understand Most common quantity prescribed for a given Drug
* Outputs metrics and recommendations in JSON format.
* Includes comprehensive logging for tracking and debugging.

## Project Structure
    project/
    ├── data/               # Directory for input files
    │   ├── pharmacies/
    │   ├── claims/
    │   └── reverts/
    ├── logs/               # Directory for log files
    |── outputs/            # Directory for output files
    ├── schemas/
    │   ├── init.py
    │   ├── pharmacy.py
    │   ├── claim.py
    │   └── revert.py
    ├── parsers/
    │   ├── init.py
    │   └── data_parser.py
    ├── utils/
    │   ├── init.py
    │   ├── logger.py
    │   └── file_reader.py
    ├── pharmacy_system.py
    └── main.py

## Usage

1.  **Install dependencies:**
    * This project requires Python 3.7 or higher.
    * Install the necessary packages: `pip install -r requirements.txt` (You'll need to create this file with the required packages, e.g., `multiprocessing`, `logging`).
2.  **Prepare input files:**
    * Ensure your pharmacy, claims, and reverts data are in the correct format (see examples in `main.py`'s epilog).
    * Place the input files in the respective directories under `data/`.
3.  **Run the script:**
    ```bash
    python main.py \
        -p data/pharmacies/pharmacies1.csv,data/pharmacies/pharmacies2.csv \
        -c data/claims/claims1.json,data/claims/claims2.json \
        -r data/reverts/reverts1.json,data/reverts/reverts2.json \
        -l logs/ \
        -v
    ```
    * `-p`, `--pharmacy-file`: Comma-separated list of paths to pharmacy data files.
    * `-c`, `--claims-file`: Comma-separated list of paths to claims data files.
    * `-r`, `--reverts-file`: Comma-separated list of paths to reverts data files.
    * `-l`, `--log-dir`: Directory for log files (default: `logs`).
    * `-v`, `--verbose`: Enable verbose logging.

## Output

* `metrics.json`: Contains calculated metrics for NPIs and NDCs.
* `chain_recommendations.json`: Contains recommendations for top 2 chains per drug.
* Log files: Daily log files are created in the specified log directory.
