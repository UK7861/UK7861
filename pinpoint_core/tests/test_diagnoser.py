import os
import sys

# Setup path
sys.path.append(os.getcwd())

from pinpoint_core.app.agents.matrix import LogExceptionDiagnoser
import logging

def test_diagnoser():
    # Setup logging to the expected file
    log_dir = os.path.join(os.getcwd(), "pinpoint_core", "app", "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "system.log")

    # Clear existing log
    if os.path.exists(log_file):
        os.remove(log_file)

    logger = logging.getLogger("PinPointCore") # Must match main.py if we want to simulate properly, or just use FileHandler
    handler = logging.FileHandler(log_file)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    diagnoser = LogExceptionDiagnoser()

    # Test Healthy
    logger.info("Some normal log message")
    status = diagnoser.monitor_stack()
    print(f"Status (Healthy): {status}")
    assert status == "HEALTHY"

    # Test Critical
    logger.error("ERROR: Something went wrong!")
    # Flush log
    for h in logger.handlers:
        h.flush()
    status = diagnoser.monitor_stack()
    print(f"Status (Critical): {status}")
    assert "CRITICAL" in status

if __name__ == "__main__":
    test_diagnoser()
