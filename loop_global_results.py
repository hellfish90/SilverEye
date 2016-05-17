import time

from pymongo import MongoClient

from silverEyeViewer.QueryApp.Core.AnalysisController import AnalysisController

client = MongoClient("127.0.0.1", 27017, connect=True)

database_name = "Test"

analysis_controller = AnalysisController(client, database_name)
while True:
    analysis_controller.overall_analysis()
    time.sleep(60)