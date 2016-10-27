import datetime
import json
import os
import create_events as ce
import data_import as di

# Define our global variables
headerFile = os.path.abspath(os.getcwd()) + '/python/data/header.csv'
detailFile = os.path.abspath(os.getcwd()) + '/python/data/detail.csv'

patientHeadIDColName = 'GECaseID'
patientDetailIDColName = 'SNACaseID'


# Create fact object
def createFactObj(headerPatientData):
    fact = dict()
    procedures = {'D' : None, 'S' : None, 'R' : None, 'C' : None, 'H' : None}
    for item in procedures.keys():
        if item in ce.processProcedures(headerPatientData): procedures[item] = True
    fact['Gender'] = 1 # 1 female, 2 male
    fact['ProcedureSumm'] = procedures
    return fact


# Write to JSON
def writeJSON(patientID, patient):
    date_handler = lambda obj: (
        obj.isoformat()
        if isinstance(obj, datetime.datetime)
        or isinstance(obj, datetime.date)
        else None
    )

    # with open('test.json', 'w') as outfile:
    #     json.dump(patient, outfile)

    return json.dumps(patient, default=date_handler, indent=4, skipkeys=True, sort_keys=True)


# Create patient object
def createPatient(patientID, headerPatientData, detailPatientData, detail_data):
    eventGroup = ce.createEventGroup(patientID, headerPatientData, detailPatientData, detail_data)
    fact = createFactObj(headerPatientData)
    person = dict()
    person['EventGroup'] = eventGroup
    person['Fact'] = fact
    return person


def get_patient(patient_id):
    import_object \
        = di.importPatientData(
            patient_id, headerFile, detailFile, patientHeadIDColName, patientDetailIDColName)

    patient_head_data = import_object[1]
    patient_detail_data = import_object[2]
    detail_data = import_object[3]

    return writeJSON(patient_id, createPatient(patient_id, patient_head_data, patient_detail_data, detail_data))

# print get_patient('02EB5A0B-53D2-496D-A52F-E687BD3AC71C')
