import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# QUERY_BQ_CLOSED_TRADE_COUNT_ROOT_RELATIVE_PATH = os.path.join(
#     BASE_DIR, "data", "query", "query_get_closed_trade_count.sql"
# )
# QUERY_BQ_DAILY_FACT_FEATURES_ROOT_RELATIVE_PATH = os.path.join(
#     BASE_DIR, "data", "query", "query_get_daily_fact_features.sql"
# )
# QUERY_BQ_NAV_BALANCE_RELATIVE_PATH = os.path.join(
#     BASE_DIR, "data", "query", "query_get_nav_balance.sql"
# )
# QUERY_BQ_OPEN_TRADE_COUNT_RELATIVE_PATH = os.path.join(
#     BASE_DIR, "data", "query", "query_get_open_trade_count.sql"
# )
# QUERY_BQ_REVENUE_INCOME_RELATIVE_PATH = os.path.join(
#     BASE_DIR, "data", "query", "query_get_revenue_income.sql"
# )
# QUERY_SF_USERS_RELATIVE_PATH = os.path.join(BASE_DIR, "data", "query", "query_get_sf_users.soql")
# QUERY_BQ_VOLUME_RELATIVE_PATH = os.path.join(BASE_DIR, "data", "query", "query_get_volume.sql")
# QUERY_BQ_USER_CHANNEL_PATH = os.path.join(BASE_DIR, "data", "query", "query_get_channel.sql")
# QUERY_BQ_MERGE_TEMP_RESULT_TO_FINAL_TABLE_PATH = os.path.join(
#     BASE_DIR, "data", "query", "query_merge_temp_result_to_final_table.sql"
# )
# QUERY_BQ_MERGE_INPUT_SAMPLES_TO_SAMPLES_TABLE_PATH = os.path.join(
#     BASE_DIR, "data", "query", "query_merge_new_input_samples_to_samples_table.sql"
# )
# QUERY_BQ_MERGE_TRAINING_DATA_TO_TRAINING_DATA_TABLE_PATH = os.path.join(
#     BASE_DIR, "data", "query", "query_merge_training_data_to_training_data_table.sql"
# )
#
# RESULT_TABLE_SCHEMA_PATH = os.path.join(
#     BASE_DIR, "data", "schema", "pltv_model_results_table_schema.json"
# )
# TRAINING_DATA_TABLE_SCHEMA_PATH = os.path.join(
#     BASE_DIR, "data", "schema", "pltv_model_training_data_table_schema.json"
# )
# INPUT_VECTORS_TABLE_SCHEMA_PATH = os.path.join(
#     BASE_DIR, "data", "schema", "pltv_model_prediction_inputs_table_schema.json"
# )
#
#
# def load_query(query_absolute_path):
#     """Loads query template file as string based on sent path.
#     :param query_absolute_path: str - absolute path to query template file
#     :return:
#     """
#     with open(query_absolute_path, "r") as file_io:
#         return file_io.read()
