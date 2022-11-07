import numpy as np
import matplotlib.pyplot as plt
import tree_landscapes as TL
import scipy.interpolate as interp

def spline_landscape(btl, smooth = 0.):
    xvals, yvals = btl.export_landscape()
    xmin, xmax = xvals[0], xvals[-1]
    return (xmin, xmax), interp.UnivariateSpline(xvals, yvals, s = smooth)

btl = TL.TreeLandscape(levels = 5, boundary_factor=2, level_height=4)
xvals, yvals = btl.export_landscape()

Temp = 200 * ( max(yvals) - min(yvals) )
xrange, btlspline = spline_landscape(btl)
epsilon = 0.05
xrange = (1+epsilon) * np.linspace(xrange[0], xrange[1], 1000)
free_energy_proxy = -np.exp( - btlspline(xrange) / Temp )

plt.figure()
plt.plot(xrange, free_energy_proxy)
plt.ylim(-1.1, 0)

# plt.figure()
# plt.plot(xvals, yvals, lw = 0, marker = "o", ms = 5)
# plt.plot( xrange / (1 + epsilon), btlspline(xrange / (1 + epsilon)), lw = 2 )
plt.show()


