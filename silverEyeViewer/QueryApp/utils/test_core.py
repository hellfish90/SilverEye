# -*- coding: utf-8 -*-
from core import SilverEye
import time

if __name__ == "__main__":
    silverEye = SilverEye('0.0.0.0', 27017)

    silverEye.start_extractor()

    time.sleep(7)
    silverEye.stop_extractor()

    time.sleep(7)
    silverEye.restart_extractor()

    time.sleep(7)
    silverEye.stop_extractor()
