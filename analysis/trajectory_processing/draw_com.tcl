#https://www.ks.uiuc.edu/Research/vmd/mailing_list/vmd-l/22204.html

# =======================================================
#set outfile [open com.dat w]
set ref [atomselect 0 "resname GBIN"]
set dummy [atomselect 0 "index 50863"]

# Loop over frames
set numframes [molinfo 0 get numframes]
for {set frame 0} {${frame} < ${numframes}} {incr frame} {

  # Change the frame inside the loop
  $ref frame $frame
  $dummy frame $frame
  set com_ref [measure center ${ref} weight mass]
  #puts $outfile "Frame $frame com $com_ref"

  # Move dummy atom to COM location
  $dummy set {x y z} [list $com_ref]
}
#close $outfile
# =======================================================
