## This document is a tutorial for inferring demography using the program dadi
**By:** Tanya Phung
**Acknowledgement:** much of the scripts used here is from Annabel Beichman and Bernard Kim

1. Installing dadi
  1. Current version (2.0.3): In the dadi manual, it is suggested that the easiest way to install dadi is via conda:
  ```
  conda install -c bioconda dadi
  ```
    - However, this newer version is not compatible with the scripts from Annabel. Therefore, in this tutorial, we will use the older version, which is version 1.6.3.
  2. Version 1.6.3:
    1. First I created a conda environment called py2 including Python version 2.7.16. The other packages that are required in order to install and run dadi are: numpy, scipy, and matplotlib. The file `environment.yml` includes all the packages in my environment py2
    2. Clone dadi github:
    ```
    git clone https://github.com/paulirish/dadi.git
    ```
    3. Install dadi:
    ```
    cd dadi/
    python setup.py install
    ```
2. Generate the allele frequency spectrum in dadi file format
  1. Allele frequency spectrum in dadi file format:
    - First line: `15 folded "AK"` where 15 denotes the number of bins of the unfolded allele frequency spectrum plus 1 bin for the monomorphic bin. In this example here, there are 7 individuals so there are 14 bins of the unfolded allele frequency spectrum plus 1 bin for the monomorphic bin, which is equal to 15. **Folded** indicates that the allele frequency spectrum is folded. **"AK"** denotes the population.
    - Second line: `6332509.42379213 737.707233765847 492.625507259976 420.892860357512 373.527206069309 304.691740700859 243.478848656167 113.652811055772 0 0 0 0 0 0 0` where each value denotes the number of variants in that bin. For example, there are 6332509.42379213 sites in the monomorphic bin, 737.707233765847 in the singleton bin, 492.625507259976 in the doubleton bin, and so on (the number here is not interger because the example is a projected SFS).
    - Third line: `1 0 0 0 0 0 0 0 1 1 1 1 1 1 1`. This line is to apply a mask, where 1 means to mask out. For example here, we are asking dadi to mask out the monomorphic bin, and bin 8 to 14 (because this is a folded allele frequency spectrum).

3. An example of how to perform demographic inference using the 2Epoch model.
  1. See the python script `1D.2Epoch.dadi.py`. This script was written originally by Annabel Beichman and modified by Tanya Phung
  2. Below I'm going through step by step of what this script does
    1. Load the sfs from file
    ```
    fs=dadi.Spectrum.from_file(sfs) (line 48)
    ```
    2. Set up general dadi parameters
      1. **ns**: sample size (in haploids)
      ```
      ns = fs.sample_sizes (line 58)
      >>> ns
      array([14])
      ```
      2. **pts**: the number of grid points used in the calculation. this should be slightly larger (+5) than sample size and increase by 10
      ```
      pts_l = [ns[0]+5,ns[0]+15,ns[0]+25]
      ```
    3. Set up specific model
      1. In this example, we are using the 2Epoch model. The two parameters for this model are **nu** and **T**. **nu** specifies the ratio of the contemporary population size to the ancient population size. **T** is the time in the past at which size change happened (in units of 2*Na generations)
      ```
      func = Demographics1D.two_epoch
      param_names= ("nu","T")
      ```
    4. Set up initial parameters:
    ```
    upper_bound = [10, 1]
    lower_bound = [1e-4, 1e-5]
    p0 = [0.01,0.001]
    ```

    5. Carry out optimization
      1. Make extrapolation function:
      ```
      func_ex = dadi.Numerics.make_extrap_log_func(func)
      ```
      2. Perturb parameters:
      ```
      p0 = dadi.Misc.perturb_params(p0, fold=1, upper_bound=upper_bound, lower_bound=lower_bound)
      >>> p0
      array([0.00558669, 0.00073791])
      ```
      3. Optimize:
      ```
      popt = dadi.Inference.optimize_log(p0, fs, func_ex, pts_l,
                                 lower_bound=lower_bound,
                                 upper_bound=upper_bound,
                                 verbose=len(p0), maxiter=maxiter)
      ```
      4. Calculate best fit model:
      ```
      model = func_ex(popt, ns, pts_l)
      ```
      5. Compute likelihood of the data given the model allele frequency spectrum:
      ```
      ll_model = dadi.Inference.ll_multinom(model, fs)
      ```
      6. Compute the likelihood of the data to itself (best possible LL):
      ```
      ll_data=dadi.Inference.ll_multinom(fs, fs)
      ```
      7. Calculate the best fit theta:
      ```
      theta = dadi.Inference.optimal_sfs_scaling(model, fs)
      ```
      8. Model specific scaling of parameters (will depend on mu and L that you supply):
      ```
      Nanc=theta / (4*mu*L)
      nu_scaled_dip=popt[0]*Nanc
      T_scaled_gen=popt[1]*2*Nanc
      scaled_param_names=("Nanc_FromTheta_scaled_dip","nu_scaled_dip","T_scaled_gen")
      scaled_popt=(Nanc,nu_scaled_dip,T_scaled_gen)
      ```
4. Best practices:
  1. For each model (for example, the 2Epoch model), we want to run the Python script (`1D.2Epoch.dadi.py`) multiple times (for example, 50 times). Then, we concat the output (use script `merge_out.py`) and sort by likelihood. We want to see that the top 3 likelihoods do not differ too much.
    1. How to use `merge.py` script:

    ```
    python merge_out.py -h
    usage: merge_out.py [-h] --directory DIRECTORY --filename FILENAME
                        --out_filename OUT_FILENAME --out_filename_sorted
                        OUT_FILENAME_SORTED

    Merge output from all runs of dadi for a model.

    optional arguments:
      -h, --help            show this help message and exit
      --directory DIRECTORY
                            Input the directory where all the runs are stored.
      --filename FILENAME   Input the name of the file.
      --out_filename OUT_FILENAME
                            Input the name of the output file.
      --out_filename_sorted OUT_FILENAME_SORTED
                            Input the name of the output file that is sorted by
                            LL.
    ```

    Example:
    ```
    python merge_out.py --directory ~/scratch/Tutorial/dadi_1.6.3/ --filename AK.dadi.inference.1D.2Epoch.runNum.1.output --out_filename test.csv --out_filename_sorted test_sorted.tsv
    ```
