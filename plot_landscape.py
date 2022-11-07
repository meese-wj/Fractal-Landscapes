import numpy as np
import matplotlib.pyplot as plt
import tree_landscapes as TL
import scipy.interpolate as interp

def spline_landscape(btl, smooth = 0.):
    xvals, yvals = btl.export_landscape()
    xmin, xmax = xvals[0], xvals[-1]
    return (xmin, xmax), interp.UnivariateSpline(xvals, yvals, s = smooth)

btl = TL.TreeLandscape(levels = 5, boundary_factor=2, level_height=2)
xvals, yvals = btl.export_landscape()

Temp = 200 * ( max(yvals) - min(yvals) )
xrange, btlspline = spline_landscape(btl)
epsilon = 0.05
xrange = (1+epsilon) * np.linspace(xrange[0], xrange[1], 1000)
free_energy_proxy = -np.exp( - btlspline(xrange) / Temp )

plt.figure()
plt.plot(xrange, free_energy_proxy)
plt.ylim(-1.1, 0)

# Uncomment to make the example in the README.md
# fig, ax = plt.subplots()
# ax.plot(xvals, yvals, lw = 0.5, 
#          marker = "o", mfc = "blue", 
#          ms = 6, mec = "orange", color = "orange")
# # ax.plot( xrange / (1 + epsilon), btlspline(xrange / (1 + epsilon)), lw = 2 )
# ax.set_xticks([])
# ax.set_yticks([])
# ax.set_xlabel("State")
# ax.set_ylabel("Energy")
# ax.set_title("BinaryTree Energy Landscape")
# plt.show()


