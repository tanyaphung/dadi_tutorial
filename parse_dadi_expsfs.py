# In this script, we will parse the output of expected sfs from dadi
import argparse

parser = argparse.ArgumentParser(description="Parse dadi expected SFS output file.")
parser.add_argument("--dadi_expsfs",required=True,help="Input the path to the dadi expected sfs file.")
parser.add_argument("--num_individuals",required=True,help="Input how many individuals there are in your sample.")
parser.add_argument("--theta",required=True,help="Input the value of theta from dadi.")
parser.add_argument("--out_filename",required=True,help="Input the output filename")

args = parser.parse_args()

file = open(args.dadi_expsfs)

folded_exp_sfs = []
for i, line in enumerate(file):
    if i == 1: #the values are in the second line of the file
        bins = line.rstrip("\n").split(" ")
        for m in range(1, int(args.num_individuals) + 1):
            n = len(bins) - 1 - m
            if m != n:
                folded_exp_sfs.append(float(bins[m]) + float(bins[n]))
            else:
                folded_exp_sfs.append((float(bins[m]) + float(bins[n]))/2)

# print (len(folded_exp_sfs))

folded_exp_sfs_scaled_by_theta = [i*float(args.theta) for i in folded_exp_sfs]

outfile = open(args.out_filename, "w")

for i in range(1, len(folded_exp_sfs) + 1):
    out = [str(i), str(folded_exp_sfs_scaled_by_theta[i-1])]
    print ("\t".join(out), file=outfile)