# Load the modules and setup our workspace
import pandas as pd
import helper_fxns as hf


# A function to import and subset data to a unique patient ID
# headerFile and detailFile should be strings containing full paths to the data files
def importPatientData(patientID, headerFile, detailFile, patientHeadIDColName, patientDetailIDColName):
    """
    This function takes in a patient ID and information about where data files are stored and returns the
    two data files (header & detail) and subsetted to the specific patient ID. The function then returns
    the patient ID, the subset header data, and the subset detail data.
    parameters:
        workingDir - The string directory where the data is stored (two .csv files)
        patientID - The unique string patient ID
        headerFile - The string file name for the file (.csv) containing header data about the patients initial diagnosis.
        detailFile - The string file name for the file (.csv) containing detail data about the patients treatment history.
        patientHeadIDColName - The string column name for the unique patient ID in the header file.
        patientDetailIDColName - The string column name for the unique patient ID in the header file.
    """

    # Import the data
    headerData = pd.read_csv(headerFile)
    detailData = pd.read_csv(detailFile)

    # Subset the data
    patientHeaderData = headerData[headerData[patientHeadIDColName] == patientID]
    patientDetailData = detailData[detailData[patientDetailIDColName] == patientID]

    # Remove all data rows where the provider specialty if not provieded (indicating machine billing).
    pd.options.mode.chained_assignment = None  # Turn off the warning that doesn't apply in this case; default='warn'
    patDetailData = patientDetailData[pd.notnull(patientDetailData['XSNACodeProviderSpecialty'])]
    patDetailData.loc[:,'XCodeDate'] = patDetailData['XCodeDate'].apply(hf.dateParse)
    patDetailData.sort_values('XCodeDate', axis=0, ascending=True, inplace=True)
    patientHeaderData.loc[:,'XDateDX'] = patientHeaderData['XDateDX'].apply(hf.dateParse)
    patientHeaderData.loc[:,'XDateFirstSurg'] = patientHeaderData['XDateFirstSurg'].apply(hf.dateParse)

    return patientID, patientHeaderData, patDetailData, detailData


# Import data
def import_data(headerFile, detailFile, rmDuplicates = True):
    header_data = pd.read_csv(headerFile)
    detail_data = pd.read_csv(detailFile)

    if rmDuplicates:
        # Remove rows where the provider specialty is NULL, indicating a billing code from a machine
        detail_data = detail_data[pd.notnull(detail_data['XSNACodeProviderSpecialty'])]

    return header_data, detail_data