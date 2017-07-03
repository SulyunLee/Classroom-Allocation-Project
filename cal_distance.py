import csv
import pandas as pd
folders = ['13-1-MW', '13-1-TF', '13-2-MW', '13-2-TF', \
            '14-1-MW', '14-1-TF', '14-2-MW', '14-2-TF',\
            '15-1-MW', '15-1-TF', '15-2-MW', '15-2-TF', \
            '16-1-MW', '16-1-TF']
folder = folders[0]
distance_file = "distance.csv"
assignment_file = "data/"+folder+"/assignment.csv"
transition_file = "data/"+folder+"/transition.csv"

distance_df = pd.read_csv(distance_file, dtype=str, index_col=[0])
assignment_df = pd.read_csv(assignment_file, dtype=str)
transition_df = pd.read_csv(transition_file, dtype=str)
transition_df["Count"] = transition_df["Count"].astype(int)

total_dist = 0
for i in range(len(transition_df)):
    src_course = transition_df["Source course"][i]
    src_class = assignment_df[assignment_df["course"]==src_course]["classroom"].iloc[0]
    dest_course = transition_df["Dest course"][i]
    dest_class = assignment_df[assignment_df["course"]==dest_course]["classroom"].iloc[0]
    count = transition_df["Count"][i]
    dist = int(distance_df[src_class][dest_class])
    total_dist += dist*count

print "Total distance:", total_dist
