import string
import pandas as pd
import createSummary as cs
import helper_fxns as hf
import clustering as cluster
import pickle
import os

# Parse comorbidities
def countComorbidities(headerPatientData):
    coMorbidList = ['Comorbidity1', 'Comorbidity2', 'Comorbidity3',
                    'Comorbidity4', 'Comorbidity5', 'Comorbidity6',
                    'Comorbidity7', 'Comorbidity8', 'Comorbidity9',
                    'Comorbidity10']
    comorbidities = dict()
    for item in coMorbidList:
        if pd.notnull(headerPatientData[item].values[0]):
            code = str(headerPatientData[item].values[0])
            code = code[0:3] + '.' + code[3:5]
            #
            # Code '0.' really means 'nothing'!
            comorbidities[item] = None if code == '0.' else code
        else:
            comorbidities[item] = None

    return comorbidities


# Convert hormone status
def convert_hormone_status(headerPatientData):
    status_code = str(headerPatientData['CS_SSFactor16'].values[0])
    if len(status_code) == 1:
        status_code = '00' + status_code
    elif len(status_code) == 2:
        status_code = '0' + status_code
    else:
        status_code = status_code

    if status_code == '000':
        status = 'triple negative'
    elif status_code == '001' or status_code == '011' or status_code == '101' or status_code == '111':
        status = 'HER positive'
    elif status_code == '100' or status_code == '010' or status_code == '110':
        status = 'HR positive'
    else:
        status = status_code

    return status


# Process the procedure summary
def processProcedures(headerPatientData):
    procedureSumm = headerPatientData['TxSummFirst'].values[0].split()
    procedureSumm = ([word.translate(None, string.punctuation) for word in procedureSumm])
    return procedureSumm


# Create comorbidity event
def createComorbidEvent(comorb, event, headerPatientData, detailPatientData):
    tempEvent = dict()
    tempEvent['topCode'] = event['Comorbidities'][comorb]
    if pd.notnull(tempEvent['topCode']):
        base = tempEvent['topCode'][0:3]
        tempData = detailPatientData[detailPatientData.code.str[0:3].values == base]
        countEvents = len(tempData.index)
        tempEvent['reDiagCount'] = countEvents
        tempEvent['Summary'] = 'When the patient was diagnosed with her tumor on ' + str(headerPatientData.XDateDX.values[0]) + ' she ' \
                                + 'was also diagnosed with ' + tempEvent['topCode'] + ', and similar diagnoses were recorded ' \
                                + 'an additional ' + str(countEvents) + ' time(s) throughout her treatment history.'
    return tempEvent


# Create header event object
def createHeaderEvent(patientID, headerPatientData, detailPatientData):
    event = dict()
    event['Type'] = 'EventGroup'
    event['EventType'] = 'Diagnosis'
    event['patientID'] = headerPatientData['GECaseID'].values[0]
    event['DiagDate'] = str(headerPatientData['XDateDX'].values[0])
    event['PrimarySite'] = headerPatientData['PrimarySite'].values[0]
    event['SiteText'] = headerPatientData['siteText'].values[0]
    event['Laterality'] = headerPatientData['Laterality'].values[0]
    event['LatDescript'] = headerPatientData['lateralDescript'].values[0]
    event['Grade'] = headerPatientData['Grade'].values[0]
    event['Histology'] = headerPatientData['Histology'].values[0]
    event['TumorSeq'] = headerPatientData['TumSeq'].values[0]
    event['Stage'] = headerPatientData['BestStage'].values[0]
    event['HormoneStatus'] = convert_hormone_status(headerPatientData)
    event['TumorSize'] = headerPatientData['CS_TumSize'].values[0]
    event['DateFirstSurg'] = (headerPatientData['XDateFirstSurg'].values[0] - headerPatientData['XDateDX'].values[0]).days
    event['lymphInvasion'] = headerPatientData['LymphVascularInvasion'].values[0]
    event['AgeAtDX'] = headerPatientData['AgeAtDX'].values[0]
    event['ProcedureSumm'] = processProcedures(headerPatientData)
    event['NumRecords'] = len(detailPatientData.index)
    event['TreatDuration'] = (detailPatientData.XCodeDate.max() - detailPatientData.XCodeDate.min()).days
    event['FirstEncountAfterDiag'] = (detailPatientData.XCodeDate[detailPatientData.XCodeDate.values > headerPatientData.XDateDX.values].min() - headerPatientData.XDateDX.values[0]).days

    comorbs = countComorbidities(headerPatientData)

    event['Comorbidities'] = comorbs

    for comorb in comorbs.keys():
        event['Comorbidities'][comorb] = createComorbidEvent(comorb, event, headerPatientData, detailPatientData)

    event['Summary'] = cs.createPatientSummary(patientID, event)

    return event


def create_date_events(date_detail_data, header_patient_data):
    events = []

    file_object = open(os.path.abspath(os.getcwd()) + '/python/data/clusters.txt', 'r')
    clusters = pickle.load(file_object)

    for date in set(date_detail_data.XCodeDate.values):
        date_event = dict()
        date_detail_data_subset = date_detail_data[date_detail_data.XCodeDate == date]

        string_codes = hf.build_string(date_detail_data_subset)
        string_cpt = hf.build_string(date_detail_data_subset[date_detail_data_subset.CodeType == 'CPT'])

        results = cluster.check_in_cluster(string_cpt, clusters[0])

        date_event['Code'] = results[1][0]
        date_event['Day_summary'] = results[1][1]
        date_event['Day_summary_codes'] = string_codes
        date_event['Day_CPT_summary_codes'] = string_cpt
        date_event['Date'] = str(date)
        date_event['Events'] = ([createDetailEvent(row[1], header_patient_data) for row in date_detail_data_subset.iterrows()])
        events.append(date_event)
    return events


# Create detail event object
def createDetailEvent(date_detail_data, header_patient_data):
    headerPatientData = header_patient_data
    eventRow = date_detail_data
    event = dict()
    event['Type'] = 'Event'
    event['EventType'] = 'Subsequent'
    event['patientID'] = eventRow['SNACaseID']
    event['relDate'] = (eventRow.XCodeDate - headerPatientData['XDateDX'].values[0]).days
    event['EventType'] = eventRow['CodeType']
    event['DataSource'] = eventRow['datasource']
    event['Code'] = eventRow['code']
    event['CodeDescript'] = '' if hf.is_nan(eventRow['CodeDescript']) else eventRow['CodeDescript']
    event['Provider'] = eventRow['XSNACodeProvider']
    event['Department'] = eventRow['XSNACodeDepartment']
    event['DeptName'] = eventRow['XSNACodeDepartmentName']
    event['ProviderSpec'] = eventRow['XSNACodeProviderSpecialty']
    event['Summary'] = cs.createEventSummary(event)
    return event


# Create event group
def createEventGroup(patientID, headerPatientData, detailPatientData, detail_data):
    headerEvent = createHeaderEvent(patientID, headerPatientData, detailPatientData)
    events = create_date_events(detailPatientData, headerPatientData)
    events.insert(0,headerEvent)
    # events.append(headerEvent)
    return events
