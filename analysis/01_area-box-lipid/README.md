
# Scripts for evaluating box size in MD simulation
Last updated: Dec 3 2018

## Contents
* `area_box_lipid.py`

## Example instructions

* Plot just one file:
    * `python area_box_lipid.py -i npt01.xst -n 144`
* Plot one file compared to another:
    * `python area_box_lipid.py -i /loc/of/sim1/npt01.xst -j /loc/of/sim2/npt01.xst -n 144`
* Plot one file compared to another, with multiple simulations each:
    * `python area_box_lipid.py -i /loc/of/sim1/npt01.xst /loc/of/sim1/npt02.xst -j /loc/of/sim2/npt01.xst /loc/of/sim2/npt02.xst -n 144`

