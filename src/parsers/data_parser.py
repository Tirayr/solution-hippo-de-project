from typing import List, Dict, Generator
import logging
from schemas.pharmacy import Pharmacy
from schemas.claim import Claim
from schemas.revert import Revert


class DataParser:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def parse_pharmacies(
        self, data: Generator[List[str], None, None]
    ) -> Generator[Pharmacy, None, None]:
        """Parse pharmacy data from a list of lists and yield Pharmacy objects."""
        for pharmacy_data in data:
            try:
                chain, npi = pharmacy_data
                yield Pharmacy(npi=npi, chain=chain)
            except (IndexError, ValueError) as e:
                self.logger.error(f"Error parsing pharmacy data: {e}. Data: {pharmacy_data}")

    def parse_claims(self, data: Generator[Dict, None, None]) -> Generator[Claim, None, None]:
        """Parse claim data and yield Claim objects."""
        for claim_data in data:
            try:
                yield Claim.from_dict(claim_data)
            except (KeyError, ValueError) as e:
                self.logger.error(f"Error parsing claim data: {e}. Data: {claim_data}")

    def parse_reverts(self, data: Generator[Dict, None, None]) -> Generator[Revert, None, None]:
        """Parse revert data and yield Revert objects."""
        for revert_data in data:
            try:
                yield Revert.from_dict(revert_data)
            except (KeyError, ValueError) as e:
                self.logger.error(f"Error parsing revert data: {e}. Data: {revert_data}")
