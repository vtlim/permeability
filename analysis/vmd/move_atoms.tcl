
# http://www.ks.uiuc.edu/Research/vmd/vmd-1.8.4/ug/node181.html#14132
proc moveby {sel offset} {
  set newcoords {}
  foreach coord [$sel get {x y z}] {
    lappend newcoords [vecadd $coord $offset]
  }
  $sel set {x y z} $newcoords
}
