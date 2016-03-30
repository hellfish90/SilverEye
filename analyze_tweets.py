# -*- coding: utf-8 -*-
from silver_eye_core import SilverEye

if __name__ == "__main__":
    silverEye = SilverEye('0.0.0.0', 27017)
    silverEye.political_analysis_for_all_user_by_political_party()
    silverEye.global_result_by_political_group()
