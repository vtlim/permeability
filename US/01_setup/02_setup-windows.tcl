# Purpose: copy and edit configuration file and colvars input file
#    into each subdirectory for Umbrella Sampling.
# Adapted from setup-windows.tcl from NAMD tutorial.
# Usage: change num_wins, maxZ; then "tclsh file.tcl"



set num_wins 53        ;# number of windows, including zero
#set num_wins 89        ;# number of windows, including zero
set maxZ 44            ;# values for "centers", spaced every 1 A
set config "us.winbase.inp"
set min "us.winbase.min.inp"
set usconf "usConfig.winbase.inp"

cd /pub/limvt/pmf/07_us
#cd /home/victoria/Documents/pmf/07_us

for {set i 0} {$i < $num_wins} {incr i} {

## process numbers < 10 to add a zero

# sort out directories, "centers" value for usConfig
if {$i <= $maxZ && $i < 10} {
    set win 0$i
    set cent $i
} elseif {$i <= $maxZ && $i >= 10} {
    set win $i
    set cent $i
} else { 
    set win $i 
    set cent [expr $maxZ - $i]
}

  ## write the minimzation config files
  set in0 [open $min r]
  set out [open "windows/${win}/01_min/us.win${win}.min.inp" w]
  puts $out "set num $win"
  while { [gets $in0 line] >= 0} {
    puts $out $line
  } 
  close $out

  ## write the config files
  set in1 [open $config r]
  set out [open "windows/${win}/us.win${win}.inp" w]
  puts $out "set num $win"
  while { [gets $in1 line] >= 0} {
    puts $out $line
  } 
  close $out

  ## write the colvars input files      
  set in2 [open $usconf r]
  set out [open "windows/${win}/usConfig.win${win}.inp" w]
  while { [gets $in2 line] >= 0} {
    if { [string match "*CENTER*" $line]} {
      puts $out "    centers        $cent"
    } else {  
      puts $out $line
    }
  }
}
