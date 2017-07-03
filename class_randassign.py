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
class_file = "data/" + folder + "/class_modified.csv"

classroom_df = pd.read_csv(classroom_file)
class_df = pd.read_csv(class_file)

def rand_select(p, class_df):
    # select p% of courses randomly
    courses = list(zip(class_df["course"], class_df["student_count"]))
    num_rand = int(len(courses) * p)
    random.shuffle(courses)
    randcourse = courses[:num_rand]
    return randcourse

def find_blankroom(class_df, classroom_df, course, time_sep):
    # list for putting full classrooms
    fullroom = []
    for i in range(len(class_df)):
        # find overlapping classrooms
        overlap = [e for e in time_sep if e in class_df["time"][i]]
        # if there is any overlapping classroom, put in list fullroom
        if overlap != []:
            fullroom.append(class_df["classroom"][i])
    # find available classrooms
    availRoom = list(set(list(classroom_df["classroom"])) - set(fullroom))
    return availRoom

def main(classroom_df, class_df, p):
    randcourse = rand_select(p, class_df)
    # sort randcourse by number of students in descending order
    sortedcourse = sorted(randcourse, key=lambda x:x[1], reverse=True)
    # make possible classroom set(classroom/time) for each selected courses
    for course, count in sortedcourse:
        time = class_df[class_df["course"]==course]["time"].values[0]
        time_sep = time.split(",")
        room = class_df[class_df["course"]==course]["classroom"].values[0]

        availRoom = find_blankroom(class_df, classroom_df, course, time_sep)
        # add current clasroom to availRT
        availRoom.append(room)
        # assign classrooms
        feasibleRoom = []
        for r in availRoom:
            if(int(classroom_df[classroom_df["classroom"]==r]["capacity"].values[0]) / 4 \
               <= count <= int(classroom_df[classroom_df["classroom"]==r]["capacity"].values[0])):
               feasibleRoom.append(r)
            # if there is no feasible classroom, select the original room
            if feasibleRoom==[]:
                selected = room
            # otherwise, randomly select a room from feasibleRoom
            else:
                selected = random.choice(feasibleRoom)
        # set the new classroom
        idx = class_df[class_df["course"]==course].index.values[0]
        class_df.set_value(idx, "classroom", selected)
