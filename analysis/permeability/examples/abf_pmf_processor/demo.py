from abf_pmf_processor import Grad, Pmf

# example of combining windows
czar_grads = [
    '../merge15-run0czarLan/win01.03.czar.grad',
    '../merge15-run0czarLan/win02.04.czar.grad',
    '../merge15-run0czarLan/win03.04.czar.grad',
    '../merge15-run0czarLan/win04.04.czar.grad',
    '../merge15-run0czarLan/win05.04.czar.grad',
    '../merge15-run0czarLan/win06.04.czar.grad']
list_grads = []
for f in czar_grads:
    g = Grad(f)
    list_grads.append(g)
joined_grad = Grad.join_windows(list_grads)
pmf_fr_grad = joined_grad.integrate()
pmf_fr_grad.write_data('test.dat')

# example of shifting pmf
pmf_top = Pmf('../merge15-run0czarLan/averaged-top.pmf')
pmf_bot = Pmf('../merge15-run0czarLan/averaged-bot.pmf')
pmf_top.shift_bulk_zero( 35, 39.9)
pmf_bot.shift_bulk_zero(-35,-39.9)

# example of joining leaflets
joined_pmf = Pmf.join_leaflets([pmf_top, pmf_bot], 295)
joined_pmf.write_data('test.dat')

# example of symmetrizing pmf
joined_pmf.symmetrize()

# plot example data
import matplotlib.pyplot as plt
plt.plot(joined_pmf.xdata, joined_pmf.ydata)
plt.grid()
plt.show()
