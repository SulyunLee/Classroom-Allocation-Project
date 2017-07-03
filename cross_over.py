import csv
import pandas as pd
import random

folders = ['13-1-MW', '13-1-TF', '13-2-MW', '13-2-TF', \
            '14-1-MW', '14-1-TF', '14-2-MW', '14-2-TF',\
            '15-1-MW', '15-1-TF', '15-2-MW', '15-2-TF', \
            '16-1-MW', '16-1-TF']

#########################################################
# modify variable here
folder = folders[0]
#########################################################
classroom_file = "classroom.csv"
class_file1 = "data/" + folder + "/class_randassign1.csv"
class_file2 = "data/" + folder + "/class_randassign2.csv"

classroom_df = pd.read_csv(classroom_file)
class_df1 = pd.read_csv(class_file1)
class_df2 = pd.read_csv(class_file2)

def rand_select(p, class_df):
    # select p% of courses randomly
    courses = list(zip(class_df["course"], class_df["student_count"]))
    num_rand = int(len(courses) * p)
    random.shuffle(courses)
    course_list = courses[:num_rand]
    return course_list

def find_blankroom(class_df, classroom_df, course, time_sep):
    # list for putting full classrooms
    fullroom = []
    for i in range(len(class_df)):
        overlap = [e for e in time_sep if e in class_df["time"][i]]
        if overlap != []:
            fullroom.append(class_df["classroom"][i])
    availRoom = list(set(list(classroom_df["classroom"])) - set(fullroom))
    return availRoom

def main(p, classroom_df, class_df1, class_df2):
    # select p% of course randomly
    course_list = rand_select(p, class_df1)
    # sort course list by number of students in descending order
    sortedcourse = sorted(course_list, key=lambda x:x[1], reverse=True)

    for course, count in sortedcourse:
        time = class_df1[class_df1["course"]==course]["time"].values[0]
        time_sep = time.split(",")
        room = class_df1[class_df1["course"]==course]["classroom"].values[0]
        new_room = class_df2[class_df2["course"]==course]["classroom"].values[0]
        availRoom = find_blankroom(class_df1, classroom_df, course, time_sep)
        # add current classroom to availRoom
        availRoom.append(room)


        feasibleRoom = []
        for r in availRoom:
            if(int(classroom_df[classroom_df["classroom"]==r]["capacity"])/4 \
                <= count <= int(classroom_df[classroom_df["classroom"]==r]["capacity"])):
                feasibleRoom.append(r)
        # if there is no feasible classroom, set the original room
        if feasibleRoom == []:
            continue
        else:
            assign_idx = class_df1[class_df1["course"]==course].index.values[0]
            if new_room in feasibleRoom:
                class_df1.set_value(assign_idx, "classroom", new_room)
            else:
                selected = random.choice(feasibleRoom)
                class_df1.set_value(assign_idx, "classroom", selected)
