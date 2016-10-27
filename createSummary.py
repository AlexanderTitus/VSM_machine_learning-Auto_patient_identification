import pandas as pd


def laterality(latValue):
    if latValue == 1:
        return 'right'
    elif latValue == 2:
        return 'left'
    else:
        return '(missing)'


def lymphInvasion(lymphValue):
    if lymphValue == 9:
        return 'untested'
    elif lymphValue == 0:
        return 'not present'
    else: return 'present'


def treatmentBreakdown(treatList):
    if 'D' in treatList or 'D,' in treatList:
        print '     Diagnostic procedure'
    if 'S' in treatList or 'S,' in treatList:
        print '     Surgery'
    if 'R' in treatList or 'R,' in treatList:
        print '     Radiation therapy'
    if 'C' in treatList or 'C,' in treatList:
        print '     Chemotherapy'
    if 'H' in treatList or 'H,' in treatList:
        print '     Hormone therapy'


def countComorbidities(comorbidities):
    coMorbidList = ['Comorbidity1', 'Comorbidity2', 'Comorbidity3',
                    'Comorbidity4', 'Comorbidity5', 'Comorbidity6',
                    'Comorbidity7', 'Comorbidity8', 'Comorbidity9',
                    'Comorbidity10']
    count = 0
    for item in coMorbidList:
        if pd.isnull(comorbidities[item]) == False:
            count += 1

    if count == 0:
        return 0
    else:
        return count


# Create an overall patient and diagnosis event summary
def createPatientSummary(patientID, event):

    # Generate the biographical summary
    summary = 'On ' + str(event['DiagDate']) + ', patient ' + patientID[0:8] \
                + ', a ' + str(event['AgeAtDX']) + ' year old woman, was diagnosed with breast cancer (lifetime tumor #' + str(event['TumorSeq'])  + '). ' \
                'She presented with ' + str(countComorbidities(event['Comorbidities'])) + ' comorbidities and a ' \
                + str(event['HormoneStatus']) + ' hormone receptor status. ' \
                'The patient presented with a ' + str(event['TumorSize']) + 'mm, (' \
                + event['Grade'] + ') stage ' + event['Stage'] + ' tumor. ' \
                'The tumor was found in the ' + laterality(event['Laterality']) + ' breast ' \
                + '(' + event['LatDescript'] + ') at the site: ' + event['SiteText'] + ' (' + event['PrimarySite'] + '). ' \
                'The status of lymph node invasion was determined to be ' + lymphInvasion(event['lymphInvasion']) + '. ' \
                'Over the course of the patient\'s treatment history (' + str(event['TreatDuration']) + ' days), she has ~' + str(event['NumRecords']) + ' encounter records on file. ' \
                'Her first visit after diagnosis was ~' + str(event['FirstEncountAfterDiag']) + ' days post-diagnosis and her first surgery was ~' + str(event['DateFirstSurg']) + ' days post-diagnosis. ' \
                'Throughout her treatment, she has undergone one or more of the following:'

    # treatmentBreakdown(event['ProcedureSumm'])


    return summary

# Create a summary specific to each event
def createEventSummary(event):
    summary = 'Patient ' + event['patientID'][0:8] + ' was seen for a "' + str(event['CodeDescript']) + '" (' \
                + event['Code'] + ') ' + str(event['relDate']) + ' days after initial diagnosis. She was seen by provider ' \
                + event['Provider'][0:8] + ' in the ' + event['ProviderSpec'] + ' department.'
    return summary
