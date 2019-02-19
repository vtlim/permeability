
# Merging ABF windows to generate full PMF profile
Last updated: Dec 5 2018

1. Prep merge. Tip: use symbolic links instead of copying files or dealing with long path names.
    * Normal ABF analysis needs [1] `.count` and [2] `.grad` files.
    * Meta-eABF analysis needs four files for CZAR estimator: [1] `.czar.count`, [2] `.czar.zcount`, [3] `.czar.grad`, [4] `.czar.zgrad`
    * Meta-eABF analysis without CZAR estimator still needs those four file types (just non-czar version of them). 
But, would need to edit `colvars` configuration file to masquerade as plain ABF simulation. 
Else it looks for `zcount` and `zgrad` files. (There might be a better way to do this that I am not aware of.)
    * Ex 1: `for k in {01..06}; do echo $k; ln -s /path/housing/windows/win$k/runXX/abf.win$k.runXX.count .; done`
    * Ex 2: Edit and run bash script `prep.sh`

2. Merge using NAMD.
    * Ex: `namd2 merge_.inp > merge.out`

3. Symmetrize profile.
    * Ex: `python symmetrize_profile.py -i merged.grad -c merged.count --anti > x`

