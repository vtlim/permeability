# "tclsh file.tcl"

# ======================================================================

set winstart 0
set winend 52
set maxZ 44.0

set ns_per_job 13.0
set eqtime 0   ;# ns for equilibration
set startns 0
set stopns 4

set wfile "INPUT_0-13ns"
set pmffile "wtt_us_0-13ns.pmf"

# ======================================================================


cd /pub/limvt/pmf/07_us/02_analysis/trajfiles

### split original traj file to discard equil time
### assuming traj output freq so that 13 ns = 13,001 lines
### .traj file should have # lines already removed with sed in bash script
set FINDEX [expr {$eqtime * 1000} + 1]
set TIME1 [expr {$startns * 1000}]
set TIME2 [expr {$stopns * 1000}]

foreach tfile [glob win*traj] {
#    exec tail -n+$FINDEX $tfile > eq$eqtime-$tfile

    ### open and read data file, separate by lines
    set fp [open $tfile r]
    set data [read $fp]
    close $fp
    set data [split $data "\n"]

    puts [llength $data]

    ### open output file and put relevant lines
    if {![file exists "zz-$tfile"]} {
        set outf [open "zz-$tfile" "w"]
    }
    puts $outf [lrange $data $TIME1 $TIME2]
    close $outf
}

exit

### open and write wham metadata file
set INPUT [open ../03_wham/$wfile w]

### wham hist_min hist_max num_bins tol temperature numpad metadatafile freefile
puts $INPUT "\#\# wham -8 44 180 0.0001 308.0 0 $wfile $pmffile"
puts $INPUT "\#\#/path/to/timeseries/file loc_win_min spring \[correl time\] \[temp\]"
puts $INPUT "\#\#"

for {set i $winstart} {$i <= $winend} {incr i} {

    ### set values for window number and wtt center
    if {$i <= $maxZ && $i < 10} {
        set win 0$i
        set cent $i
    } elseif {$i <= $maxZ && $i > 10} {
        set win $i
        set cent $i
    } else {
        set win $i
        set cent [expr $maxZ - $i]
    }

    if ![file exists ./eq$eqtime-win$win.traj] {
        continue
    }
    puts $INPUT "../trajfiles/eq$eqtime-win$win.traj $cent 1.5"
}

close $INPUT
