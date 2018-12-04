head -n 2 *.state | tail -n 1 | awk '{print $2}'
tail -n 1 *traj | awk '{print $1}'
tail -n 1 *xsc | awk '{print $1}' 

#find -type f -name '*.count' ! -iname '*hist.count' -path '*noMin*'
#find -type f -name '*.count' ! -iname '*hist.count' -path '*noMin*' -exec tail -f "$file" {} +

