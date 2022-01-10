# HOHMANN GUI
# A GUI version of HOHMANN BASIC.
# Basic program to calculate a Hohmann transfer between two coplanar, circular orbits.
# The altitudes of the two orbits are defined by user input.

# ---------------------------------------------------
# Imports
from orbit_toolbox import hohmann, Transfer
from bodies_toolbox import Planet
from guizero import App, Text, TextBox, PushButton

# ---------------------------------------------------
# Constants
Earth_radius = Planet["Earth"]["radius"]


# ---------------------------------------------------
# Functions
def hohmann_calc():
    Hoh_1 = Transfer(1, "hohmann", "09012022")
    hohmann_result = Hoh_1.hohmann("Earth", int(h_start_input.value)+Earth_radius, int(h_end_input.value)+Earth_radius)

    result_dv1.value = hohmann_result[0]
    result_dv2.value = hohmann_result[1]
    result_dv_total.value = hohmann_result[2]
    result_t_transfer.value = hohmann_result[3]


# ---------------------------------------------------
# App

# App and grid frameworks
app = App("Hohmann GUI", layout="grid")

# Input text and boxes
h_start_text = Text(app, text="Start altitude (km): ", grid=[0, 0])
h_start_input = TextBox(app, text="Insert start altitude (km) here", width="30", grid=[2, 0])
h_end_text = Text(app, text="End altitude (km): ", grid=[0, 1])
h_end_input = TextBox(app, text="Insert end altitude (km) here", width="30", grid=[2, 1])

# Calculation button
h_start_set = PushButton(app, command=hohmann_calc, text="Calculate transfer", grid=[1, 2])

# Output text and boxes
dv1_text = Text(app, text="dv1 (km.s^-1) =", grid=[0, 3])
result_dv1 = TextBox(app, text="dv1 =", width="30", grid=[2, 3])

dv2_text = Text(app, text="dv2 (km.s^-1) =", grid=[0, 4])
result_dv2 = TextBox(app, text="dv2 =", width="30", grid=[2, 4])

dv_total_text = Text(app, text="dv_total (km.s^-1) =", grid=[0, 5])
result_dv_total = TextBox(app, text="dv_total =", width="30", grid=[2, 5])

t_transfer_text = Text(app, text="t_transfer (s) =", grid=[0, 6])
result_t_transfer = TextBox(app, text="t_transfer =", width="30", grid=[2, 6])

app.display()
