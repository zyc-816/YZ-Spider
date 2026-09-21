import random
import time

import config


def delay() -> None:
    time.sleep(random.uniform(config.MIN_DELAY, config.MAX_DELAY))
    return