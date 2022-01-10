from math import sqrt, pi, exp, sin, radians, log
from bodies_toolbox import Planet, Moon, body_type, TU


# ---------------------------------------------------
# Classes
class Transfer:
    def __init__(self, identifier, manvre_type, start_time) -> None:
        self._identifier = identifier
        self._type = manvre_type
        self._start_time = start_time
        self._dv = None
        self._t_trans = None

    def hohmann(self, body, r_init, r_final):
        """Calculates a simple Hohmann transfer between two circular, coplanar orbits"""
        """Arguments: body (string), initial radius (int/float), final radius (int/float)"""
        """Outputs: Δv of first burn, km/s (float); Δv of second burn, km/s (float); total Δv, km/s (float); transfer 
        time, s (float) """
        # Semi-major axes
        a_trans = (r_init + r_final) / 2

        # Orbit velocities
        v_init = v_circ(body, r_init)
        v_trans_a = vis_viva(body, r_init, a_trans)
        v_trans_b = vis_viva(body, r_final, a_trans)
        v_final = v_circ(body, r_final)

        # Delta-vs and transfer time
        dv_a = v_trans_a - v_init
        dv_b = v_final - v_trans_b
        dv_total = abs(dv_a) + abs(dv_b)
        t_trans = half_period(body, a_trans)

        self._dv = dv_total
        self._t_trans = t_trans

        return [dv_a, dv_b, dv_total, t_trans]


class Orbit:
    def __init__(self) -> None:
        self._velocity = None

    # @body.setter
    # def body(self, body):
    #     self._body = body

    def v_circ(self, body, a):
        """Calculates the velocity of a circular orbit"""
        if body_type(body) == "Planet":
            self._velocity = sqrt(Planet[str(body)]["mu"] / a)
        if body_type(body) == "Moon":
            self._velocity = sqrt(Moon[str(body)]["mu"] / a)

        return self._velocity

    def vis_viva(self, body, r, a):
        """Uses the vis-viva equation to find the velocity at a particular point in an orbit"""
        if body_type(body) == "Planet":
            self._velocity = sqrt(Planet[body]["mu"] * (2 / r - 1 / a))
        elif body_type(body) == "Moon":
            self._velocity = sqrt(Moon[body]["mu"] * (2 / r - 1 / a))
        else:
            raise Exception("Body not found during vis_viva")

        return self._velocity


# ---------------------------------------------------
# Functions

# Velocity
def v_circ(body, a):
    """Calculates the velocity of a circular orbit"""
    if body_type(body) == "Planet":
        return sqrt(Planet[body]["mu"] / a)
    if body_type(body) == "Moon":
        return sqrt(Moon[body]["mu"] / a)


def vis_viva(body, r, a):
    """Uses the vis-viva equation to find the velocity at a particular point in an orbit"""
    if body_type(body) == "Planet":
        return sqrt(Planet[body]["mu"] * (2 / r - 1 / a))
    elif body_type(body) == "Moon":
        return sqrt(Moon[body]["mu"] * (2 / r - 1 / a))
    else:
        raise Exception("Body not found during vis_viva")


# Time
def period(body, a):
    """Calculates the period of an orbit"""
    if body_type(body) == "Planet":
        return 2 * pi * sqrt(a ** 3 / Planet[body]["mu"])
    elif body_type(body) == "Moon":
        return 2 * pi * sqrt(a ** 3 / Moon[body]["mu"])
    else:
        raise Exception("Body not found during period")


def half_period(body, a):
    """Calculates half the period of an orbit"""
    if body_type(body) == "Planet":
        return pi * sqrt(a ** 3 / Planet[body]["mu"])
    elif body_type(body) == "Moon":
        return pi * sqrt(a ** 3 / Moon[body]["mu"])
    else:
        raise Exception("Body not found during half_period")


# Manoeuvres
def hohmann(body, r_init, r_final):
    """Calculates a simple Hohmann transfer between two circular, coplanar orbits"""
    # Semi-major axes
    a_trans = (r_init + r_final) / 2

    # Orbit velocities
    v_init = v_circ(body, r_init)
    v_trans_a = vis_viva(body, r_init, a_trans)
    v_trans_b = vis_viva(body, r_final, a_trans)
    v_final = v_circ(body, r_final)

    # Delta-vs and transfer time
    dv_a = v_trans_a - v_init
    dv_b = v_final - v_trans_b
    dv_total = abs(dv_a) + abs(dv_b)
    t_trans = half_period(body, a_trans)

    return dv_a, dv_b, dv_total, t_trans


def bi_elliptic(body, r_init, r_b, r_final):
    """Calculates a bi-elliptic transfer between two circular, coplanar orbits"""
    # Semi-major axes
    a_trans_1 = (r_init + r_b) / 2
    a_trans_2 = (r_b + r_final) / 2

    # Orbital velocities
    v_init = v_circ(body, r_init)
    v_trans_1_a = vis_viva(body, r_init, a_trans_1)
    v_trans_1_b = vis_viva(body, r_b, a_trans_1)
    v_trans_2_b = vis_viva(body, r_b, a_trans_2)
    v_trans_2_c = vis_viva(body, r_final, a_trans_2)
    v_final = v_circ(body, r_final)

    # Delta-vs and transfer time
    dv_a = v_trans_1_a - v_init
    dv_b = v_trans_2_b - v_trans_1_b
    dv_c = v_final - v_trans_2_c
    dv_total = abs(dv_a) + abs(dv_b) + abs(dv_c)
    t_trans = half_period(body, a_trans_1) + half_period(body, a_trans_2)

    return dv_a, dv_b, dv_c, dv_total, t_trans


def inclination(v, di):
    """Calculates the delta-v for an inclination change of di degrees"""
    return 2 * v * sin(radians(di))


def low_thrust(body, a_init, a_final, i_init, i_final, Isp, F, m_i):
    #### TODO NEEDS FIXING ####

    """Calculates a low thrust transfer between orbits of different semi-major axis and inclination
    Taken from Algorithm 47 on page 387 of Vallado"""
    if body_type(body) == "Planet":
        g = Planet[body]["gravity"]
    elif body_type(body) == "Moon":
        g = Moon[body]["gravity"]
    else:
        raise Exception("Body not found during low_thrust")

    R = a_final / a_init
    mdot = -F / Isp * g
    mdot_spec = mdot / m_i
    a_thrusti = F / m_i
    di = i_final - i_init

    dv = 1 - sqrt(1 / R)
    t_trans = 1 / -mdot_spec * (1 - exp(mdot_spec * dv / a_thrusti))

    return dv, t_trans


def low_thrust_no_inc(h_init, h_final, a_thrusti, pmf):
    # TODO NEEDS GENERALISING
    a_init = (h_init + Planet["Earth"]["radius"]) / Planet["Earth"]["radius"]
    DU_star = h_init + Planet["Earth"]["radius"]
    mu = 1
    TU_star = sqrt((DU_star / Planet["Earth"]["radius"]) ** 3 / mu) * TU
    a_final = 6.61
    a_thrusti /= DU_star / TU_star ** 2
    R = a_final / a_init
    dv_acc = (1 - sqrt(1 / R)) * DU_star / TU_star  # km/s
    mdot_spec = a_thrusti / dv_acc * log(1 - pmf) / TU_star  # /s
    t_trans = pmf / abs(mdot_spec)  # s

    return dv_acc, t_trans
