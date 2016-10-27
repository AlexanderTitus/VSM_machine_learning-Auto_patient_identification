import pandas as pd
pd.options.mode.chained_assignment = None

def dateParse(date):
    return parse(date).date()


# Add code base classification for each CPT code
def change_cpt_code(data):

    def classify(classification):
        row[1]['codeBase'] = classification
        bagOfWords = str(row[1]['CodeDescript']) + ' ' + str(row[1]['XSNACodeDepartmentName']) + ' ' + str(row[1]['XSNACodeProviderSpecialty']) + ' ' + str(row[1]['codeBase'])
        data.set_value(index, 'bagOfWords', bagOfWords)
        data.set_value(index, 'codeBase', classification)

    for i, row in enumerate(data.iterrows()):
        index = data.index.values[i]

        if row[1]['CodeType'] == 'CPT' and not any(c.isalpha() for c in row[1]['code']):

            if int(row[1]['code']) > 10000:

                if int(row[1]['code']) < 10022:
                    classify('general')

                elif int(row[1]['code']) < 19499:
                    classify('integumentary')

                elif int(row[1]['code']) < 29999:
                    classify('musculoskeletal')

                elif int(row[1]['code']) < 32999:
                    classify('respiratory')

                elif int(row[1]['code']) < 37799:
                    classify('cardiovascular')

                elif int(row[1]['code']) < 38999:
                    classify('lymphatic')

                elif int(row[1]['code']) < 39599:
                    classify('diaphragm')

                elif int(row[1]['code']) < 49999:
                    classify('digestive')

                elif int(row[1]['code']) < 53899:
                    classify('urinary')

                elif int(row[1]['code']) < 55899:
                    classify('maleGenital')

                elif int(row[1]['code']) < 55980:
                    classify('reproductive')

                elif int(row[1]['code']) < 58999:
                    classify('femaleGenital')

                elif int(row[1]['code']) < 59899:
                    classify('maternityDelivery')

                elif int(row[1]['code']) < 60699:
                    classify('endocrine')

                elif int(row[1]['code']) < 64999:
                    classify('nervous')

                elif int(row[1]['code']) < 68899:
                    classify('eye')

                elif int(row[1]['code']) < 69979:
                    classify('auditory')

                else:
                    classify('other')
        else:
            classify('other')

    return data


# Create a combined summary for each patient
def patient_code_combination(headerData, detailData):
    headerData['bagOfWords'] = headerData.GECaseID

    for i, patient in enumerate(headerData.GECaseID):
        index = headerData.index.values[i]
        patient_data = detailData[detailData.SNACaseID == patient]

        bag_group = set(patient_data.bagOfWords)

        bagOfWords = {bag for bag in bag_group}
        headerData.set_value(index, 'bagOfWords', bagOfWords)

    return headerData


# Create a concatenated list of codes for a specific date - CPT
def build_string(data):
    string = ''
    for code in data.code.values:
        string = string + ' ' + code

    return string


# Create a concatenated list of codes for a specific date - EPICMedID
def build_string_med(data):
    full_string = ''
    for string in data.CodeDescript.values:
        full_string = full_string + ' ' + string.split(' ', 1)[0]

    return full_string


# Loop through all dates to build codes
def date_code_concat(data, big_string):

    for date in set(data.XCodeDate.values):
        patient_date_subset = data[data.XCodeDate == date]

        string = build_string(patient_date_subset)
        # string = build_string_med(patient_date_subset)
        big_string.append(string)
    return big_string


# Create patient bagOfWords from codes that occur on the same day
def bag_or_words(data, group='date', code='CPT'):
    big_string = []
    cpt_data = data[data.CodeType == code]

    for patient in set(cpt_data.SNACaseID.values):
        patient_data = cpt_data[cpt_data.SNACaseID == patient]
        if group == 'date':
            big_string = date_code_concat(patient_data, big_string)
        elif group == 'patient':
            big_string.append(build_string(patient_data))


    return big_string


##############################
# Prepare data
##############################
def prepare_data(detail_data):
    # Process data for further analysis
    detail_data['codeBase'] = detail_data['CodeDescript']
    detail_data['bagOfWords'] = detail_data['CodeDescript']
    detail_data = change_cpt_code(detail_data)
    return detail_data


##############################
# Prepare data and bagOfWords by date for VSM
##############################
def prepare_date_vsm(detail_data):
    # Process data for further analysis
    detail_data = prepare_data(detail_data)

    new_data = bag_or_words(detail_data)
    return new_data


##############################
# Prepare data and bagOfWords by patient for VSM
##############################
def prepare_patient_vsm(detail_data):
    # Process data for further analysis
    detail_data = prepare_data(detail_data)

    new_data = bag_or_words(detail_data, group='patient')
    return new_data


##############################
# Prepare data and bagOfWords by patient for VSM
##############################
def prepare_vsm(detail_data, grouping, code):
    # Process data for further analysis
    detail_data = prepare_data(detail_data)

    new_data = bag_or_words(detail_data, group=grouping, code=code)
    return new_data
