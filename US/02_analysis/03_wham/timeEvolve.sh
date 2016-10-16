python input-wham-cmdline.py --portion True --begin 0 --end 13
python input-wham-cmdline.py --portion True --begin 13 --end 26
python input-wham-cmdline.py --portion True --begin 26 --end 39 --prefix 13-26ns
python input-wham-cmdline.py --portion True --begin 39 --end 52 --prefix 13-26ns
python input-wham-cmdline.py --portion True --begin 52 --end 104 --prefix 39-52ns

#exit
# now manually fix the WHAM 52-104 file for windows 30-44

wham=/data/users/limvt/local/wham/wham/wham
$wham -8.000000 44.000000 180 0.000100 308.000000 0.000000 WHAM-INPUT_0-13ns US_0-13ns.pmf      > wham_0-13ns.out
$wham -8.000000 44.000000 180 0.000100 308.000000 0.000000 WHAM-INPUT_13-26ns US_13-26ns.pmf    > wham_13-26ns.out 
$wham -8.000000 44.000000 180 0.000100 308.000000 0.000000 WHAM-INPUT_26-39ns US_26-39ns.pmf    > wham_26-39ns.out 
$wham -8.000000 44.000000 180 0.000100 308.000000 0.000000 WHAM-INPUT_39-52ns US_39-52ns.pmf    > wham_39-52ns.out 
$wham -8.000000 44.000000 180 0.000100 308.000000 0.000000 WHAM-INPUT_52-104ns US_52-104ns.pmf  > wham_52-104ns.out  

