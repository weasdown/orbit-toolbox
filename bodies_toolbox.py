from math import sqrt

# Planet data

"""TO DO: 

Check whether gravity should be in km.s^-2 or m.s^-2 for consistency with other units
Add gravity to bodies to match Earth entry
Add Sun
Add dictionary for moons that links to their parent planets

"""


def body_type(body):
    """Determines the body type of body"""
    if body in Planet:
        return "Planet"
    elif body in Moon:
        return "Moon"
    else:
        return False


Planet = {
    "Mercury": {
        "Position": 1,
        "mu": 2.203E4,  # km^3 s^-2
        "radius": 2440,  # km
        "Moons": False
    },

    "Venus": {
        "Position": 2,
        "mu": 3.249E5,  # km^3 s^-2
        "radius": 6052,  # km
        "Moons": False
    },

    "Earth": {
        "Position": 3,
        "mu": 3.986E5,  # km^3 s^-2
        "radius": 6378,  # km
        "gravity": 9.80665E-3,  # km s^-2
        "Moons": ["Moon"]
    },

    "Mars": {
        "Position": 4,
        "mu": 4.283E4,  # km^3 s^-2
        "radius": 3390,  # km
        "Moons": ["Phobos", "Diemos"]
    },

    "Jupiter": {
        "Position": 5,
        "mu": 1.267E8,  # km^3 s^-2
        "radius": 69911,  # km
        "Moons": ["Io", "Europa", "Ganymede", "Callisto", "Others"]
    },

    "Saturn": {
        "Position": 6,
        "mu": 3.793E7,  # km^3 s^-2
        "radius": 58232,  # km
        "Moons": ["Titan", "Rhea", "Iapetus", "Dione", "Tethys", "Enceladus", "Mimas", "Others"]
    },

    "Uranus": {
        "Position": 7,
        "mu": 5.793E6,  # km^3 s^-2
        "radius": 25362,  # km
        "Moons": ["Titania", "Oberon", "Umbriel", "Ariel", "Miranda", "Others"]
    },

    "Neptune": {
        "Position": 8,
        "mu": 6.836E6,  # km^3 s^-2
        "radius": 24622,  # km
        "Moons": ["Triton", "Others"]
    }

}

Moon = {
    "Moon": {
        "Parent": Planet["Earth"],
        "mu": 4.904E3,  # km^3 s^-2
        "radius": 1737.4,  # km
        "Distance": 384399  # Semi-major axis from parent, km
    }
}

TU = sqrt(Planet["Earth"]["radius"] ** 3 / Planet["Earth"]["mu"])
