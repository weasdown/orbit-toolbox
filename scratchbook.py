from orbit_toolbox import Orbit, Planet

body = "Earth"
periapsis = Planet["Earth"]["radius"] + 400
apoapsis = Planet["Earth"]["radius"] + 700

a = (periapsis+apoapsis)/2

test = Orbit()

print(f"Velocity, circular (3 d.p.): {round(test.v_circ(body, a),3)} km/s")
print(f"Velocity, vis-viva (3 d.p.): {round(test.vis_viva(body, periapsis, a),3)} km/s")
