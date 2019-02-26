
import sys
sys.path.insert(0, '../../')
from abf_pmf_processor import Grad, Pmf

# combine windows of upper leaflet
czar_grads = [
    'win01.03.czar.grad',
    'win02.04.czar.grad',
    'win03.04.czar.grad',
    'win04.04.czar.grad',
    'win05.04.czar.grad',
    'win06.04.czar.grad']
list_grads = []
for f in czar_grads:
    g = Grad(f)
    list_grads.append(g)
joined_grad = Grad.join_windows(list_grads)
pmf_top = joined_grad.integrate()

# combine windows of lower leaflet
czar_grads = [
    'win06-bot.02.czar.grad',
    'win07-bot.03.czar.grad',
    'win08-bot.03.czar.grad',
    'win09-bot.04.czar.grad',
    'win10-bot.03.czar.grad']
list_grads = []
for f in czar_grads:
    g = Grad(f)
    list_grads.append(g)
joined_grad = Grad.join_windows(list_grads)
pmf_bot = joined_grad.integrate()

# shift bulk water region to have average pmf of zero
# note: you can also load pmf directly from file like so
#pmf_top = Pmf('../merge15-run0czarLan/averaged-top.pmf')
pmf_top.shift_bulk_zero( 35, 39.9)
pmf_bot.shift_bulk_zero(-35,-39.9)

# combine upper and lower leaflets
joined_pmf = Pmf.join_leaflets([pmf_top, pmf_bot], 295)

# symmetrize pmf
joined_pmf.symmetrize()

# write out pmf (this same call can be used on Grad objects)
joined_pmf.write_data('pmf.dat')

# plot final data
import matplotlib.pyplot as plt
plt.plot(joined_pmf.xdata, joined_pmf.ydata)
plt.grid()
plt.show()

# VTL data source:
# /dfs2/tw/limvt/08_permeate/taut2/winmerge/merge15-run0czarLan
