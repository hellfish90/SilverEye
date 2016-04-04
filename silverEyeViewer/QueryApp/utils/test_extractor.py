from core import SilverEye
from pymongo import MongoClient

if __name__ == "__main__":

    client = MongoClient('0.0.0.0', 27017, connect=True)

    silverEye = SilverEye('0.0.0.0', 27017)

    silverEye.start_extractor()