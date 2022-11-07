import numpy as np
import matplotlib.pyplot as plt
import tree_landscapes as TL
import scipy.interpolate as interp

def spline_landscape(btl, smooth = 0.):
    xvals, yvals = btl.export_landscape()
    xmin, xmax = xvals[0], xvals[-1]
    return (xmin, xmax), interp.UnivariateSpline(xvals, yvals, s = smooth)

btl = TL.TreeLandscape(levels = 8, boundary_factor=2, level_height=10)
xvals, yvals = btl.export_landscape()

Temp = 2 * ( max(yvals) - min(yvals) )
xrange, btlspline = spline_landscape(btl)
epsilon = 0.05
xrange = (1+epsilon) * np.linspace(xrange[0], xrange[1], 1000)
free_energy_proxy = -np.exp( - btlspline(xrange) / Temp )

plt.plot(xrange, free_energy_proxy)
plt.ylim(-1.1, 0)
plt.show()

# plt.plot(xvals, yvals, lw = 0, marker = "o", ms = 5)
# plt.plot( xrange, btlspline(xrange), lw = 2 )


