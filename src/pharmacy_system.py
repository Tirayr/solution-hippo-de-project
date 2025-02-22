import json
import multiprocessing
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from collections import defaultdict, Counter

from schemas.pharmacy import Pharmacy
from schemas.claim import Claim
from schemas.revert import Revert
from parsers.data_parser import DataParser
from utils.file_reader import FileReader


class PharmacySystem:
    def __init__(self):
        self.pharmacies: Dict[str, Pharmacy] = {}
        self.claims: Dict[str, Claim] = {}
        self.active_claims: Dict[str, Claim] = {}
        self.reverts: Dict[str, Revert] = {}
        self.logger = multiprocessing.get_logger()
        self.parser = DataParser(self.logger)
        self.file_reader = FileReader()

    def load_pharmacies_from_file(self, file_path: str) -> None:
        """Load pharmacy data from file into the system."""
        try:
            data = self.file_reader.read_csv_file(file_path)  # Use read_csv_file
            self.logger.info(f"Loading pharmacy data from {file_path}")
            for pharmacy in self.parser.parse_pharmacies(data):
                self.pharmacies[pharmacy.npi] = pharmacy  # Use npi as key
            self.logger.info(f"Successfully loaded {len(self.pharmacies)} pharmacies")
        except Exception as e:
            self.logger.error(f"Failed to load pharmacy data: {str(e)}")
            raise

    def process_claims_from_file(self, file_path: str) -> None:
        """Process claims from file."""
        try:
            # Get the generator
            data_generator = self.file_reader.read_json_lines_file(file_path)
            self.logger.info(f"Processing claims from {file_path}")

            processed_count = 0
            skipped_count = 0

            # Extract the list of claims from the generator
            for claim_list in data_generator:
                # Iterate through the list of claims
                for claim_data in claim_list:
                    try:
                        claim = Claim.from_dict(claim_data)
                    except (KeyError, ValueError) as e:
                        self.logger.error(f"Error parsing claim data: {e}. Data: {claim_data}")
                        continue
                    if claim.npi not in self.pharmacies.keys():
                        self.logger.warning(f"Pharmacy with NPI {claim.npi} not found. Skipping claim {claim.id}")
                        skipped_count += 1
                        continue

                    self.claims[claim.id] = claim
                    self.active_claims[claim.id] = claim
                    processed_count += 1
            self.logger.info(f"Processed {processed_count} claims, skipped {skipped_count} claims")

        except Exception as e:
            self.logger.error(f"Failed to process claims: {str(e)}")
            raise

    def process_reverts_from_file(self, file_path: str) -> None:
        """Process reverts from file"""
        try:
            data_generator = self.file_reader.read_json_lines_file(file_path)
            self.logger.info(f"Processing reverts from {file_path}")
            processed_count = 0
            skipped_count = 0

            for revert_list in data_generator:
                for revert_data in revert_list:
                    try:
                        revert = Revert.from_dict(revert_data)
                    except (KeyError, ValueError) as e:
                        self.logger.error(f"Error parsing claim data: {e}. Data: {revert_data}")
                        continue

                    self.reverts[revert.id] = revert
                    self.active_claims.pop(revert.claim_id, None)
                    processed_count += 1

            self.logger.info(f"Processed {processed_count} reverts, skipped {skipped_count} reverts")
        except Exception as e:
            self.logger.error(f"Failed to process reverts: {str(e)}")
            raise

    def get_active_claims_for_pharmacy(self, npi: str) -> List[Claim]:
        """Get all active claims for a specific pharmacy"""
        return [claim for claim in self.active_claims.values() if claim.npi == npi]

    def get_total_revenue_for_pharmacy(self, npi: str) -> float:
        """Calculate total revenue for a pharmacy based on active claims"""
        active_claims = self.get_active_claims_for_pharmacy(npi)
        return sum(claim.price for claim in active_claims)

    def get_drug_distribution(self, npi: str) -> Dict[str, int]:
        """Get distribution of drugs (NDCs) for a pharmacy"""
        active_claims = self.get_active_claims_for_pharmacy(npi)
        distribution = {}
        for claim in active_claims:
            distribution[claim.ndc] = distribution.get(claim.ndc, 0) + claim.quantity
        return distribution

    def calculate_metrics(self) -> List[Dict]:
        """Calculate metrics for all NPI-NDC combinations."""
        metrics = []
        for npi in self.pharmacies:
            for ndc in set(claim.ndc for claim in self.claims.values() if claim.npi == npi):
                claims_for_npi_ndc = [claim for claim in self.claims.values() if claim.npi == npi and claim.ndc == ndc]
                reverts_for_npi_ndc = [
                    revert for revert in self.reverts.values()
                    if self.claims.get(revert.claim_id) and self.claims[revert.claim_id].npi == npi and self.claims[revert.claim_id].ndc == ndc
                ]
                # Calculate the average unit price for the current (npi, ndc) pair
                avg_unit_price = sum(claim.price / claim.quantity for claim in claims_for_npi_ndc) / len(
                    claims_for_npi_ndc) if claims_for_npi_ndc else 0

                metrics.append({
                    "npi": npi,
                    "ndc": ndc,
                    "fills": len(claims_for_npi_ndc),
                    "reverted": len(reverts_for_npi_ndc),
                    "avg_price": avg_unit_price,
                    "total_price": sum(claim.price for claim in claims_for_npi_ndc),
                    "total_quantity": sum(claim.quantity for claim in claims_for_npi_ndc)
                })

        return metrics

    def save_metrics_to_json(self, json_data, output_file: str) -> None:
        """Save the calculated metrics to a JSON file."""
        try:
            with open(output_file, 'w') as f:
                json.dump(json_data, f, indent=4)  # Directly dump the list of metrics
            self.logger.info(f"Metrics saved to {output_file}")
        except Exception as e:
            self.logger.error(f"Failed to save metrics to JSON: {e}")
            raise

    def recommend_top_chains_per_drug(self, metrics, top_num) -> List[dict]:
        """Recommends the top 2 chains with the lowest average unit price for each drug."""

        # Calculate metrics first
        metrics = self.calculate_metrics()

        # Aggregate metrics by NDC and chain
        ndc_chain_avg_prices = defaultdict(list)
        for metric in metrics:
            ndc = metric['ndc']
            npi = metric['npi']
            chain = self.pharmacies[npi].chain
            ndc_chain_avg_prices[ndc].append({"name": chain, "avg_price": metric['avg_price']})

        # Create recommendations
        recommendations = []
        for ndc, avg_prices in ndc_chain_avg_prices.items():
            top_chains = sorted(avg_prices, key=lambda x: x["avg_price"])[:top_num]
            recommendations.append({"ndc": ndc, "chain": top_chains})

        return recommendations

    def find_most_common_quantities(self, metrics: list[dict], most_common_quantity_limit: int) -> list[dict]:
        """
        Finds the most common quantities for each drug (NDC)
        using pre-calculated metrics with total_quantity.
        """

        ndc_quantities = defaultdict(list)
        for metric in metrics:
            ndc = metric['ndc']
            total_quantity = metric['total_quantity']
            ndc_quantities[ndc].append(total_quantity)

        result = []
        for ndc, quantities in ndc_quantities.items():
            most_common_quantities = [q for q, c in Counter(quantities).most_common(most_common_quantity_limit)]
            result.append({"ndc": ndc, "most_prescribed_quantity": most_common_quantities})
        return result
