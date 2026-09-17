import time
import config
import random

def delay() -> None:
    time.sleep(random.uniform(config.MIN_DELAY, config.MAX_DELAY))
    return