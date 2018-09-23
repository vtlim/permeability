rm diffuse_26ns.out
for k in {52..45}; do echo $k; ./corr_vtl1 /pub/limvt/pmf/07_us/02_analysis/trajfiles-26ns/win$k.traj 1 >> diffuse_26ns.out; done
for k in {00..44}; do echo $k; ./corr_vtl1 /pub/limvt/pmf/07_us/02_analysis/trajfiles-26ns/win$k.traj 1 >> diffuse_26ns.out; done
