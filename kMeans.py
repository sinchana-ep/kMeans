import numpy as np
import pandas as pd
import csv
import getopt, sys
import os
import path

iteration = 0
#for command line parameters
ip_filename = ""
directory_name = ""
fullCmdArguments = sys.argv
argumentList = fullCmdArguments[1:]
unix_options = "hd:o"
gnu_options = ["help", "data=", "output="]
try:
        arguments, values = getopt.getopt(argumentList, unix_options, gnu_options)
except getopt.error as err:
        print(str(err))
        print("kMeans.py --data <InputFileName> --output <DirectoryName>")
        sys.exit(2)

if len(arguments) < 1:
        print("Incorrect format \nPlease use this format for input parameters:")
        print("kMeans.py --data <InputFileName> --output <DirectoryName>")
        sys.exit(2)

for currentArgument, currentValue in arguments:
        if currentArgument in ("-h", "--help"):
            print("kMeans.py --data <InputFileName> --output <DirectoryName>")
            sys.exit()
        elif currentArgument in ("-d", "--data"):
            ip_filename = currentValue
        elif currentArgument in ("-o", "--output"):
            directory_name = currentValue


#read tsv file
ip = pd.read_csv(ip_filename, delimiter='\t', header=None)
ip = ip.drop(ip.columns[0], axis=1)
df = ip.dropna(axis=1, how='all')
df.columns=['x','y']

#write to directory
try:
        if not os.path.exists(str(os.getcwd()) + directory_name):
            os.makedirs(str(os.getcwd()) + directory_name)
            print("Directory ", directory_name, " Created ")
except FileExistsError:
    print("Directory ", directory_name, " already exists")

save_path=str(os.getcwd())+directory_name
op_filename=str(ip_filename.split('.')[0])
protoName = os.path.join(save_path, op_filename+"-Proto.tsv")
progrName = os.path.join(save_path, op_filename+"-Progr.tsv")
proto_file = open(protoName, "w")
progr_file = open(progrName, "w", newline='')

centroids = {1: [0, 5], 2: [0, 4], 3: [0, 3]}


def cluster_assignment(df, centroids):
    for i in centroids.keys():
        # euclidean distance
        df['distance_from_centroid{}'.format(i)] = (
            np.sqrt(
                (df['x'] - centroids[i][0]) ** 2
                + (df['y'] - centroids[i][1]) ** 2
            )
        )
    cluster_assignment_cols = ['distance_from_centroid{}'.format(i) for i in centroids.keys()]
    df['cluster'] = df.loc[:, cluster_assignment_cols].idxmin(axis=1)
    df['cluster'] = df['cluster'].map(lambda x: int(x.lstrip('distance_from_')))
    df['closest_value'] = df.loc[:, cluster_assignment_cols].min(axis=1)
    return df
df = cluster_assignment(df, centroids)


def recompute(k):
    if iteration != 0:
        proto_file.write('\n')
    for i in centroids:
        count = 0
        for value in centroids[i]:
            if count == 0:
                proto_file.write(str(value) + ',')
            else:
                proto_file.write(str(value))
            count = count + 1
        proto_file.write('\t')

    for i in centroids.keys():
        centroids[i][0] = np.mean(df[df['cluster'] == i]['x'])
        centroids[i][1] = np.mean(df[df['cluster'] == i]['y'])
    return k

while True:
    #optimization criteria
    sse = (df['closest_value'] ** 2).sum()
    progr_file.write(str(sse) + '\n')
    old_centroids = dict(centroids)
    dict1_values = []
    dict2_values = []
    for key, value in sorted(centroids.items()):
        for i in value:
            dict1_values.append(i)
    centroids = recompute(centroids)
    for key, value in sorted(old_centroids.items()):
        for i in value:
            dict2_values.append(i)

    iteration = iteration+1
    df = cluster_assignment(df, centroids)
    #if centroid values don't change anymore the program terminates
    if dict1_values == dict2_values:
        break

print('Program complete! Output stored in ' + save_path)
