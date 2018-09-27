rm output_02_20ps.dat

trajfiles=( 
  "/dfs3/pub/limvt/pmf/07_us/windows/52/us.win52-rs04-z01.colvars.traj"
  "/dfs3/pub/limvt/pmf/07_us/windows/48/us.win48-rs05-z01.colvars.traj"
  "/dfs3/pub/limvt/pmf/07_us/windows/00/us.win00-rs03-z01.colvars.traj" 
  "/dfs3/pub/limvt/pmf/07_us/windows/05/us.win05-rs06-z01.colvars.traj"
  "/dfs3/pub/limvt/pmf/07_us/windows/10/us.win10-rs02-z01.colvars.traj"
  "/dfs3/pub/limvt/pmf/07_us/windows/15/us.win15-rs03-z01.colvars.traj"
  "/dfs3/pub/limvt/pmf/07_us/windows/20/us.win20-rs03-z01.colvars.traj"
  "/dfs3/pub/limvt/pmf/07_us/windows/25/us.win25-rs02-z01.colvars.traj"
  "/dfs3/pub/limvt/pmf/07_us/windows/29/us.win29-rs04-z01.colvars.traj"
  "/dfs3/pub/limvt/pmf/07_us/windows/34/us.win34-rs03-z01.colvars.traj"
  "/dfs3/pub/limvt/pmf/07_us/windows/40/us.win40-z01.colvars.traj" 
)

for i in "${trajfiles[@]}"; do echo $i; echo $k >> output_02_20ps.dat; ./corr_orig $i 1 >> output_02_20ps.dat; done
#echo "/dfs3/pub/limvt/pmf/07_us/windows/52/us.win52-rs02-z01.colvars.traj" >> output_02_20ps.dat; ./corr_orig /dfs3/pub/limvt/pmf/07_us/windows/52/us.win52-rs04-z01.colvars.traj 1 >> output_02_20ps.dat
#echo "/dfs3/pub/limvt/pmf/07_us/windows/00/us.win00-rs03-z01.colvars.traj" >> output_02_20ps.dat; ./corr_orig /dfs3/pub/limvt/pmf/07_us/windows/00/us.win00-rs03-z01.colvars.traj 1 >> output_02_20ps.dat
#echo "/dfs3/pub/limvt/pmf/07_us/windows/10/us.win10-rs02-z01.colvars.traj" >> output_02_20ps.dat; ./corr_orig /dfs3/pub/limvt/pmf/07_us/windows/10/us.win10-rs02-z01.colvars.traj 1 >> output_02_20ps.dat
#echo "/dfs3/pub/limvt/pmf/07_us/windows/20/us.win20-rs03-z01.colvars.traj" >> output_02_20ps.dat; ./corr_orig /dfs3/pub/limvt/pmf/07_us/windows/20/us.win20-rs03-z01.colvars.traj 1 >> output_02_20ps.dat
