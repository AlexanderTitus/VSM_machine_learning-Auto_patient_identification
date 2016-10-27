# Imports and setting up the workspace
from pprint import pprint
import data_import as di
import vsm_data_manipulation as vdm
import clustering as cluster


########################
# Running the code
########################
# Initialize logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


# Define our global variables
headerFile = '/Users/alexandertitus/pinnacles/summaryAPI/python/data/header.csv'
detailFile = '/Users/alexandertitus/pinnacles/summaryAPI/python/data/detail.csv'
patientHeadIDColName = 'GECaseID'
patientDetailIDColName = 'SNACaseID'


# Import data
data = di.import_data(headerFile, detailFile)
header_data = data[0]
detail_data = data[1]

k = 8
# Run the VSM and extract results
# new_data = vdm.prepare_date_vsm(detail_data)
# new_data = vdm.prepare_patient_vsm(detail_data)

new_data = vdm.prepare_vsm(detail_data, 'date', 'CPT')
clusters = cluster.create_clusters(new_data, k=k, model='LSI')

for i in range(k): print "Set " + str(i) + ': ', len(clusters[1][i]), len(set(clusters[0][i]))
for i in range(k): pprint(set(clusters[0][i]))

# # Plot the clusters
# cluster.plot_clusters(k, clusters[2], clusters[3], clusters[4])
# cluster.plot_kmeans_error(1, 20, clusters[2])

# # Test the cluster reporting
# string_test = '19303 19357'
# results = check_in_cluster(string_test, clusters[0])
# print set(results)
# print len(results)