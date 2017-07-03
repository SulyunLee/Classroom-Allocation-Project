from cross_over import *

####################################
# modify variables here
crossover_num = 100
firstgen_num = 100
p = 0.2
####################################

for i in range(crossover_num):
    num_list = range(1, firstgen_num+1)
    file_choice = random.sample(num_list, 2)
    file1 = "data/"+folder+"/class_randassign"+str(file_choice[0])+".csv"
    file2 = "data/"+folder+"/class_randassign"+str(file_choice[1])+".csv"
    class_df1 = pd.read_csv(file1)
    class_df1 = pd.read_csv(file2)

    main(p, classroom_df, class_df1, class_df2)
    class_df1.to_csv("data/"+folder+"/crossover"+str(i+1)+".csv", index=False, index_col=False)
