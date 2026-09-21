# ======================================================================
# BEGIN DO NOT EDIT
# ======================================================================
import logging
import sys
from pathlib import Path

# running path
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent

# url
ROOT_URL = r"https://account.chsi.com.cn"
LOGIN_URL = r"https://account.chsi.com.cn/passport/login?entrytype=yzgr&service=https%3A%2F%2Fyz.chsi.com.cn%2Fj_spring_cas_security_check"
SIGN_URL = r"https://yz.chsi.com.cn/zsml/rs/zys.do"
MAIN_URL = r"https://yz.chsi.com.cn/zsml/a/zydetail.do"
SEARCH_URL = r"https://yz.chsi.com.cn/zsml/code/autozy.do"
SCHOOL_LIST_URL = r"https://yz.chsi.com.cn/zsml/rs/zydws.do"
SCHOOL_DETAIL_URL = r"https://yz.chsi.com.cn/zsml/rs/yjfxs.do"


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

# user data
ACCOUNT = ""
PASSWORD = ""

# UA
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"

# request config
MIN_DELAY = 3.0
MAX_DELAY = 4.0
MAX_RETRIES = 3
TIMEOUT = 10

# output path
OUTPUT_DIR = BASE_DIR / "outputs"