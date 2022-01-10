# HOHMANN BASIC
# Basic program to calculate a Hohmann transfer between two coplanar, circular orbits.
# The altitudes of the two orbits are defined by user input.

# ---------------------------------------------------
# Imports
from orbit_toolbox import vis_viva, period, v_circ, half_period

# ---------------------------------------------------
# Constants
radius_Earth = 6378  # km
mu_Earth = 3.986E5  # km^3 s^-2

# ---------------------------------------------------
# User-defined variables
h_start = int(input("Start altitude (km): "))  # km
h_end = int(input("End altitude (km): "))  # km

# ---------------------------------------------------
# Basic orbit calcs
# Orbit SMAs
a_start = h_start + radius_Earth
a_end = h_end + radius_Earth
a_trans = (a_start + a_end) / 2

# Orbit velocities
v1 = v_circ("Earth", a_start)
v2 = vis_viva("Earth", a_start, a_trans)
v3 = vis_viva("Earth", a_end, a_trans)
v4 = v_circ("Earth", a_end)

# Delta-vs
dv1 = v2 - v1
dv2 = v4 - v3
dv_total = dv1 + dv2
t_transfer = half_period("Earth", a_trans)

# ---------------------------------------------------
# Outputs
print(dv1)
print(dv2)
print(dv_total)
print(t_transfer)
