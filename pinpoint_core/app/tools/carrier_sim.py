import random
import time
from typing import Dict

class MMISignalGenerator:
    """Simulates GSM MMI/USSD signals from a carrier network."""

    SIGNAL_TYPES = ["BALANCE_QUERY", "RECHARGE", "NETWORK_STATUS", "LOCATION_UPDATE"]
    CARRIERS = ["VODAFONE", "AIRTEL", "JIO", "T-MOBILE"]

    @staticmethod
    def generate_raw_signal() -> Dict[str, str]:
        """Generates a mock MMI signal."""
        signal_id = f"MMI_{random.randint(1000, 9999)}"
        signal_type = random.choice(MMISignalGenerator.SIGNAL_TYPES)
        carrier = random.choice(MMISignalGenerator.CARRIERS)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        return {
            "signal_id": signal_id,
            "type": signal_type,
            "carrier": carrier,
            "timestamp": timestamp,
            "raw_payload": f"*121#{random.randint(10, 99)}*"
        }

if __name__ == "__main__":
    # Test generation
    print(MMISignalGenerator.generate_raw_signal())
