
## Example workflow

1. Symmetrize PMF.
    * `python symmetrize_profile.py -i merge.grad -c merge.count --anti > pmf-sym.dat`

2. Shift PMF.
    * `python ../shift_pmf.py -i pmf-sym.dat -a 34.0 -b 36.0 -o pmf-sym-shift.dat`
    * VTL prefers the shift range of 40.0--42.0.

3. Prep final PMF/diffusivity files for permeability.

4. Process PMF to have same colvars grid as diffusivity.
    * `awk 'NR % 5 == 0' pre_final_pmf.dat`

5. Calculate permeability.
    * `python calc_perme.py -p final_pmf.dat -d final_dif.dat -t 308 > output.dat`

6. Plot components.
    `python plot_permeate.py -i final_pmf.dat --pmf`


