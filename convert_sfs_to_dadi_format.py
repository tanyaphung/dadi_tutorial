import argparse

# ---------------------
# Parse input arguments
# ---------------------
parser = argparse.ArgumentParser(description="Convert sfs (Tanya file format) to dadi file format for sfs")
parser.add_argument("--num_bin",required=True,help="Number of bin, which is equal to the number of unfolded sfs bins plus "
                                                 "one bin for the monomorphic bin. Ex: if there are 7 individuals, input "
                                                 "15 here because there are 7*2=14 unfolded sfs bins plus one bin for the monomorphic bin.")
parser.add_argument("--folded_or_unfolded",required=True,help="Input either folded or unfolded.")
parser.add_argument("--population_name",required=True,help="Input the name of the population.")
parser.add_argument("--sfs_filename",required=True,help="Input the path to the sfs file with Tanya file format.")
parser.add_argument("--num_individuals",required=True,help="Input the number of individuals in the sample.")
parser.add_argument("--out_filename",required=True,help="Input the path to the output file.")
parser.add_argument("--num_monomorphic",required=True,help="Input the number of monomorphic sites.")
parser.add_argument("--include_monomorphic",required=True,help="Input yes if wanting to include the monomorphic. No if wanting to mask out monomorphic.")


args = parser.parse_args()

outfile = open(args.out_filename, "w")

# Print first line
print (args.num_bin + " " + args.folded_or_unfolded + " " + '"' + args.population_name + '"', file=outfile)

# Print second line
sfs_bins = [args.num_monomorphic]
if args.include_monomorphic == "yes":
    mask = [str(0)]
    with open(args.sfs_filename, "r") as f:
        for line in f:
            sfs_bins.append(str(int(float(line.rstrip("\n").split("\t")[1]))))
            mask.append(str(0))

    # append the 0s to the rest of the bin
    for i in range(int(args.num_individuals)):
        sfs_bins.append(str(0))
        mask.append(str(1))

    print (" ".join(sfs_bins), file=outfile)
    print (" ".join(mask), file=outfile)

else:
    mask = [str(1)]
    with open(args.sfs_filename, "r") as f:
        for line in f:
            sfs_bins.append(str(int(float(line.rstrip("\n").split("\t")[1]))))
            mask.append(str(0))

    # append the 0s to the rest of the bin
    for i in range(int(args.num_individuals)):
        sfs_bins.append(str(0))
        mask.append(str(1))

    print(" ".join(sfs_bins), file=outfile)
    print(" ".join(mask), file=outfile)


