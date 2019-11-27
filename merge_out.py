import pandas as pd
import argparse
import os

parser = argparse.ArgumentParser(description="Merge output from all runs of dadi for a model.")
parser.add_argument("--directory",required=True,help="Input the directory where all the runs are stored.")
parser.add_argument("--filename",required=True,help="Input the name of the file.")
parser.add_argument("--out_filename",required=True,help="Input the name of the output file.")
parser.add_argument("--out_filename_sorted",required=True,help="Input the name of the output file that is sorted by LL.")

args = parser.parse_args()

all_reps = pd.read_csv(os.path.join(args.directory, "run_1", args.filename), sep="\t")

for i in range(2, 51):
    rep = pd.read_csv(os.path.join(args.directory, "run_" + str(i), args.filename), sep="\t")
    all_reps = all_reps.append(rep)

all_reps.to_csv(args.out_filename, sep=",", index=False)

all_reps_sort_by_LL = all_reps.sort_values("LL", ascending=False)
all_reps_sort_by_LL.to_csv(args.out_filename_sorted, sep=",", index=False)
