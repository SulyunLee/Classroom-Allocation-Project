from class_randassign import *

#################################
# set the number of first generation
first_gen_num = 20
p = [0.1, 0.3, 0.5, 0.7, 1.0]
####################################

for i in range(len(p)):
    for j in range(first_gen_num):
        main(classroom_df, class_df, p[i])
        class_df.to_csv("data/" + folder + "/class_randassign"+str(j+1+20*i)+".csv", index=False, index_col=False)
