import csv
import pandas as pd
import itertools

folders = ['13-1-MW', '13-1-TF', '13-2-MW', '13-2-TF', \
            '14-1-MW', '14-1-TF', '14-2-MW', '14-2-TF',\
            '15-1-MW', '15-1-TF', '15-2-MW', '15-2-TF', \
            '16-1-MW', '16-1-TF']

def open_files(class_file, enrollment_file):
    # open files
    class_df = pd.read_csv(class_file, dtype=str)
    enroll_df = pd.read_csv(enrollment_file, dtype=str)
    return class_df, enroll_df

def time_convert(class_df):
    # make time_conversion dictionary
    weekday = ["M", "T", "W", "Th", "F", "S"]
    num_courses_per_day = 12
    offset = 0

    time_conversion = {}
    for day in weekday:
        for i in range(num_courses_per_day):
            key = day + str(i+1)
            value = offset*num_courses_per_day + i+1
            time_conversion[key] = value
        offset += 1
    class_df["time_conv"] = class_df["time"]
    #create a list of integers corresponding to the time_conversion
    for idx in range(len(class_df)):
        class_df.set_value(idx, "time_conv", [time_conversion[val] for val in class_df["time"][idx].split(',')])
    return class_df

def inner_join(class_df, enroll_df):
    # inner join two datasets on course
    joined_df = pd.merge(class_df, enroll_df, on=["course", "semester", "year", "subjectCode"], how="inner")
    joined_df.to_csv("data/"+folder+"/merged.csv", index = False)
    return joined_df

def cal_movement(joined_df):
    output_dict = dict()
    uniqueID = joined_df["random.ID"].unique()

    for id in uniqueID:
        id_df = joined_df[joined_df["random.ID"] == id].reset_index(drop=True)
        len_courses = len(id_df)

        for row_i in range(len_courses-1):
            for row_j in range(row_i+1, len_courses):
                for time1 in id_df["time_conv"][row_i]:
                    for time2 in id_df["time_conv"][row_j]:
                        if(time1 - time2) == -1:
                            course1 = id_df["course"][row_i]
                            course2 = id_df["course"][row_j]
                        elif(time1 - time2) == 1:
                            course1 = id_df["course"][row_j]
                            course2 = id_df["course"][row_i]
                            if course1 in output_dict:
                                if course2 in output_dict[course1]:
                                    output_dict[course1][course2] += 1
                                else:
                                    output_dict[course1][course2] = 1
                            else:
                                output_dict[course1] = dict()
                                output_dict[course1][course2] = 1
    return output_dict

folder = folders[0]
class_file = 'data/' + folder + '/class_randassign4.csv'
enrollment_file = 'enrollment_deidentified.csv'
class_df, enroll_df = open_files(class_file, enrollment_file)
class_df = time_convert(class_df)

enroll_df["course"] = enroll_df["subjectCode"] + "." + enroll_df["num"]
class_df["course"] = class_df["subjectCode"] + "." + class_df["num"]


joined_df = inner_join(class_df, enroll_df)
output_dict = cal_movement(joined_df)

# write transition file
with open('data/'+folder+'/transition.csv', 'wb') as transfile:
    writer = csv.writer(transfile)
    writer.writerow(["Source course", "Dest course", "Count"])
    for src in output_dict.keys():
        for dest in output_dict[src].keys():
            writer.writerow([src, dest, output_dict[src][dest]])

# write assigmnent.csv file
assignment_df = joined_df.loc[:,["course", "classroom"]]
assignment_df = assignment_df.drop_duplicates()
assignment_df.to_csv("data/"+folder+"/assignment.csv", index=False, index_col=False)
class_df.to_csv("data/"+folder+"/class_modified.csv", index=False, index_col=False)
