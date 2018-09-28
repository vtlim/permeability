package require tempoUserVMD

mol new /pub/limvt/pmf/00_reference/chipot_box.psf
dopbc -file /pub/limvt/pmf/06_abf/win05-noMin/02_run2/abf.win05.02.dcd -frames 0:100:4999
centering -mol top -ref "name C21 C31"

#set sel [atomselect top "oxygen and segname WTT"] 

mol addrep 0
mol modselect 1 0 segname WTT
mol modstyle 1 0 VDW 1.500000 12.000000
mol modcolor 1 0 ColorID 4

