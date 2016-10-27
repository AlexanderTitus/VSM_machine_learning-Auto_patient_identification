import pickle
import clustering as cluster
import vsm_data_manipulation as vdm
import data_import as di
import os


# Define our global variables
headerFile = os.path.abspath(os.getcwd()) + '/../data/header.csv'
detailFile = os.path.abspath(os.getcwd()) + '/../data/detail.csv'

patientHeadIDColName = 'GECaseID'
patientDetailIDColName = 'SNACaseID'
patient_id = 'F60657BD-1482-4DED-8E23-756E459F56A4'

import_object = di.importPatientData(patient_id, headerFile, detailFile, patientHeadIDColName, patientDetailIDColName)

# patient_head_data = import_object[1]
# patient_detail_data = import_object[2]
detail_data = import_object[3]

k = 8
new_data = vdm.prepare_vsm(detail_data, 'date', 'CPT')
clusters = cluster.create_clusters(new_data, k=k, model='LSI')

file_name = 'clusters.txt'
file_object = open(os.path.abspath(os.getcwd()) + '/../data/' + file_name, 'wb')
pickle.dump(clusters, file_object)
file_object.close()
