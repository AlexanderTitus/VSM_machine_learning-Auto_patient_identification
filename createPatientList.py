import datetime
import json
import os
import os.path
import pandas as pd

header = os.path.abspath(os.getcwd()) + '/../data/header.csv'

dataList = pd.read_csv(header)
patientList = dict()
patientList['PatientList'] = ([id for id in dataList.GECaseID.values])

# Write patient list to a JSON object
def writeJSON(patientList):
    date_handler = lambda obj: (
        obj.isoformat()
        if isinstance(obj, datetime.datetime)
        or isinstance(obj, datetime.date)
        else None
    )

    fileName = os.path.abspath(os.getcwd()) + '/../data/patientList.json'
    with open(fileName, "w") as outfile:
        jsonText = json.dumps(patientList, default=date_handler, indent=4, skipkeys=True, sort_keys=True)

    fd = open(fileName, 'w')
    fd.write(jsonText)
    fd.close()

writeJSON(patientList)
