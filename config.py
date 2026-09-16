# ======================================================================
# BEGIN DO NOT EDIT
# ======================================================================
import logging
from pathlib import Path

# running path
BASE_DIR = Path(__file__).resolve().parent
COLOR_RESET = "\033[0m"

# ======================================================================
# END
# ======================================================================


# log config
LOG_FILE = BASE_DIR / "logs" / "YZ-Spider.log"
FILE_LOG_LEVEL = "DEBUG"
CONSOLE_LOG_LEVEL = "INFO"
LOG_BACKUP_DAYS = 7
COLOR_MAP = {
    logging.DEBUG: "\033[36m",
    logging.INFO: "\033[32m",
    logging.WARNING: "\033[33m",
    logging.ERROR: "\033[31m",
    logging.CRITICAL: "\033[1;31m"
}


