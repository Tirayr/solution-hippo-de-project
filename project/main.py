import argparse
from pathlib import Path
from pharmacy_system import PharmacySystem
from utils.logger import setup_logger, with_logging
import multiprocessing


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Process pharmacy, claims, and reverts from text files.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
        Example usage:
          python main.py -p pharmacies1.txt pharmacies2.txt -c claims1.txt,claims2.txt -r reverts1.txt,reverts2.txt
          python main.py --pharmacy-file data/pharmacies1.txt,data/pharmacies2.txt 
                         --claims-file data/claims1.txt,data/claims2.txt
                         --reverts-file data/reverts1.txt,data/reverts2.txt
        '''
    )

    parser.add_argument(
        '-p', '--pharmacy-files',
        nargs='+',  # Accept one or more file paths
        type=str,
        required=True,
        help='Path(s) to the pharmacy data file(s)'
    )

    parser.add_argument(
        '-c', '--claims-files',
        nargs='+',  # Accept one or more file paths
        type=str,
        required=True,
        help='Path(s) to the claims data file(s)'
    )

    parser.add_argument(
        '-r', '--reverts-files',
        nargs='+',  # Accept one or more file paths
        type=str,
        required=True,
        help='Path(s) to the reverts data file(s)'
    )

    parser.add_argument(
        '-l', '--log-dir',
        type=str,
        default='logs',
        help='Directory for log files (default: logs)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()
    args.pharmacy_files = args.pharmacy_files[0].split(',')
    args.claims_files = args.claims_files[0].split(',')
    args.reverts_files = args.reverts_files[0].split(',')

    # Validate file paths
    for file_paths in [args.pharmacy_files, args.claims_files, args.reverts_files]:
        for file_path in file_paths:
            if not Path(file_path).is_file():
                parser.error(f"File not found: {file_path}")

    # Validate/create log directory
    log_dir = Path(args.log_dir)
    try:
        log_dir.mkdir(exist_ok=True)
    except Exception as e:
        parser.error(f"Cannot create log directory {args.log_dir}: {str(e)}")

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
        try:
            with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
                pool.starmap(process_pharmacy_file,
                             [(system, file_path, log_file, args.verbose) for file_path in args.pharmacy_files])
                pool.starmap(process_claims_file,
                             [(system, file_path, log_file, args.verbose) for file_path in args.claims_files])
                pool.starmap(process_reverts_file,
                             [(system, file_path, log_file, args.verbose) for file_path in args.reverts_files])

            # Generate reports (this part needs to be adjusted as well)
            logger.info("Generating pharmacy statistics...")

            # Calculate metrics and save to JSON
            metrics_output_file = "outputs/metrics.json"
            metrics = system.calculate_metrics()
            system.save_metrics_to_json(metrics, metrics_output_file)

            # Generate chain recommendations using calculated metrics and save to JSON
            recommendations_output_file = "outputs/chain_recommendations.json"
            recommendations = system.recommend_top_chains_per_drug(metrics, 2)
            system.save_metrics_to_json(recommendations, recommendations_output_file)

            # Generate most common quantities using calculated metrics and save to JSON
            quantities_output_file = "outputs/most_common_quantities.json"
            most_common_quantities = system.find_most_common_quantities(metrics)
            system.save_metrics_to_json(most_common_quantities, quantities_output_file)

        except Exception as e:
            logger.error(f"An error occurred during processing: {str(e)}")
            raise

    logger.info("Processing completed successfully")


if __name__ == "__main__":
    main()
