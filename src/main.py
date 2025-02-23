import argparse
from pathlib import Path
import multiprocessing
from configs import config
from pharmacy_system import PharmacySystem
from utils.logger import setup_logger, with_logging


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Process pharmacy, claims, and reverts from directories of files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        Example usage:
          python main.py -p data/pharmacies data/claims -c data/claims -r data/reverts
        """,
    )

    parser.add_argument(
        "-p",
        "--pharmacy-dir",
        type=str,
        required=True,
        help="Path to the directory containing pharmacy data files",
    )

    parser.add_argument(
        "-c",
        "--claims-dir",
        type=str,
        required=True,
        help="Path to the directory containing claims data files",
    )

    parser.add_argument(
        "-r",
        "--reverts-dir",
        type=str,
        required=True,
        help="Path to the directory containing reverts data files",
    )

    parser.add_argument(
        "-l", "--log-dir", type=str, default="logs", help="Directory for log files (default: logs)"
    )

    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    # Validate directory paths
    for dir_path in [args.pharmacy_dir, args.claims_dir, args.reverts_dir]:
        if not Path(dir_path).is_dir():
            parser.error(f"Directory not found: {dir_path}")

    return args


@with_logging
def process_pharmacy_file(system, file_path):
    try:
        system.load_pharmacies_from_file(file_path)
    except Exception as e:
        system.logger.error(f"Error processing pharmacy file {file_path}: {e}")


@with_logging
def process_claims_file(system, file_path):
    try:
        system.process_claims_from_file(file_path)
    except Exception as e:
        logger.error(f"Error processing claims file {file_path}: {e}")


@with_logging
def process_reverts_file(system, file_path):
    try:
        system.process_reverts_from_file(file_path)
    except Exception as e:
        logger.error(f"Error processing reverts file {file_path}: {e}")


def main():
    args = parse_arguments()
    # Split comma-separated file paths into lists

    logger, log_file = setup_logger(log_dir=args.log_dir, verbose=args.verbose)
    logger.info("Starting pharmacy system processing")

    # Create a PharmacySystem object
    system = PharmacySystem()

    # Use a Manager to share the attributes of the system object
    with multiprocessing.Manager() as manager:
        # Create shared variables for the attributes
        shared_pharmacies = manager.dict()
        shared_claims = manager.dict()
        shared_active_claims = manager.dict()
        shared_reverts = manager.dict()

        # Assign the shared variables to the system object's attributes
        system.pharmacies = shared_pharmacies
        system.claims = shared_claims
        system.active_claims = shared_active_claims
        system.reverts = shared_reverts

        # Setting up the list of files to be processed
        pharmacy_files = [str(file) for file in Path(args.pharmacy_dir).glob("*") if file.is_file()]
        claims_files = [str(file) for file in Path(args.claims_dir).glob("*") if file.is_file()]
        reverts_files = [str(file) for file in Path(args.reverts_dir).glob("*") if file.is_file()]

        try:
            with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
                pool.starmap(
                    process_pharmacy_file,
                    [(system, file_path, log_file, args.verbose) for file_path in pharmacy_files],
                )
                pool.starmap(
                    process_claims_file,
                    [(system, file_path, log_file, args.verbose) for file_path in claims_files],
                )
                pool.starmap(
                    process_reverts_file,
                    [(system, file_path, log_file, args.verbose) for file_path in reverts_files],
                )

            # Generate reports (this part needs to be adjusted as well)
            logger.info("Generating pharmacy statistics...")

            # Calculate metrics and save to JSON
            metrics_output_file = config.METRICS_OUTPUT_FILE
            metrics = system.calculate_metrics()
            system.save_metrics_to_json(metrics, metrics_output_file)

            # Generate chain recommendations using calculated metrics and save to JSON
            recommendations_output_file = config.CHAIN_RECOMMENDATIONS_OUTPUT_FILE
            recommendations = system.recommend_top_chains_per_drug(metrics, config.TOP_N_CHAINS)
            system.save_metrics_to_json(recommendations, recommendations_output_file)

            # Generate most common quantities using calculated metrics and save to JSON
            quantities_output_file = config.MOST_COMMON_QUANTITIES_OUTPUT_FILE
            most_common_quantities = system.find_most_common_quantities(
                metrics, config.MOST_COMMON_QUANTITIES_LIMIT
            )
            system.save_metrics_to_json(most_common_quantities, quantities_output_file)

        except Exception as e:
            logger.error(f"An error occurred during processing: {str(e)}")
            raise

    logger.info("Processing completed successfully")


if __name__ == "__main__":
    main()
