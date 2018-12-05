
# Merging ABF windows to generate full PMF profile
Last updated: Dec 5 2018

1. Prep merge. Tip: use symbolic links instead of copying files or dealing with long path names.
    * Normal ABF calculations need [1] `.count` and [2] `.grad` files.
    * Meta-eABF calculations need four files: [1] `.czar.count`, [2] `.czar.zcount`, [3] `.czar.grad`, [4] `.czar.zgrad`
    * Ex 1: `for k in {01..06}; do echo $k; ln -s /path/housing/windows/win$k/runXX/abf.win$k.runXX.count .; done`
    * Ex 2: Edit and run bash script `prep.sh`

2. Merge using NAMD.
    * Ex: `namd2 merge_.inp > merge.out`

3. Symmetrize profile.
    * Ex: `python symmetrize_profile.py -i merged.grad -c merged.count --anti > x`

