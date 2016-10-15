package require tempoUserVMD

mol new /pub/limvt/pmf/00_reference/chipot_box.psf
dopbc -file /pub/limvt/pmf/06_abf/win05-noMin/01_run1/abf.win05.01.dcd -frames 0:10:14999
centering -mol top -ref "name C21 C31"
set sel [atomselect top "oxygen and segname WTT"] 
set idf [open wtt_win05_01a.dat w]

# loop over 1500 since skipping every 10 frames
for {set i 0} {$i < 1500} {incr i} {
    $sel frame $i
    puts $idf "$i [$sel get z]"
}

