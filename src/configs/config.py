import os

OUTPUT_DIR = "outputs"

LOG_DIR = "logs"
METRICS_OUTPUT_FILE = os.path.join(OUTPUT_DIR, "metrics.json")
CHAIN_RECOMMENDATIONS_OUTPUT_FILE = os.path.join(OUTPUT_DIR, "chain_recommendations.json")
MOST_COMMON_QUANTITIES_OUTPUT_FILE = os.path.join(OUTPUT_DIR, "most_common_quantities.json")
TOP_N_CHAINS = 2
MOST_COMMON_QUANTITIES_LIMIT = 5
