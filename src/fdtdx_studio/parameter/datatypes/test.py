import fdtdx

from .model import Model

print("\n===== SIMPLE CREATION TESTS =====\n")

model = Model([])


# ==========================================================
# 1) MATERIAL
# ==========================================================

print("-> Creating Material Object...")
mat = fdtdx.Material()
mat_obj = model.create_material_obj(name="MatTest", material=mat, partial_real_shape=(1, 1, 1))

print("Material object:", mat_obj)
print("Material name:", mat_obj.name)
print("Material content:", model.get_by_name("MatTest").material)
print()


# ==========================================================
# 2) UNIFORM PLANE SOURCE
# ==========================================================

print("-> Creating Uniform Plane Source...")

src_uniform = model.create_mode_plane_source_obj(
    name="UniformSource",
    direction=(1, 0, 0),
    azimuth_angle=30,
)

print("Uniform Source:", src_uniform)
print("Uniform Source name:", src_uniform.name)
print("Find via name:", model.get_by_name("UniformSource"))
print()


# ==========================================================
# 3) GAUSSIAN PLANE SOURCE
# ==========================================================

print("-> Creating Gaussian Plane Source...")

src_gauss = model.create_gaussian_plane_source_obj(
    name="GaussianSource",
    radius=5,
    std=0.3,
    normalize_by_energy=True,
)

print("Gaussian Source:", src_gauss)
print("Gaussian radius:", src_gauss.radius)
print("Found via name:", model.get_by_name("GaussianSource"))
print()


# ==========================================================
# 4) ENERGY DETECTOR
# ==========================================================

print("-> Creating Energy Detector...")

det_energy = model.create_energy_detector_obj(name="EnergyDet", partial_real_shape=(1, 1, 1), color=(0.5, 1.0, 0.5))

print("Energy Detector:", det_energy)
print("Energy Detector name:", det_energy.name)
print("Found via name:", model.get_by_name("EnergyDet"))
print()


# ==========================================================
# 5) FIELD DETECTOR
# ==========================================================

print("-> Creating Field Detector...")

det_field = model.create_field_detector_obj(name="FieldDet", components=("Ex", "Ey", "Ez"))

print("Field Detector:", det_field)
print("Field Detector components:", det_field.components)
print("Found via name:", model.get_by_name("FieldDet"))
print()


# ==========================================================
# 6) POYNTING FLUX DETECTOR
# ==========================================================

print("-> Creating Poynting Flux Detector...")

det_flux = model.create_poynting_flux_detector(name="FluxDet", direction=(0, 0, 1))

print("Poynting Flux Detector:", det_flux)
print("Direction:", det_flux.direction)
print("Found via name:", model.get_by_name("FluxDet"))
print()


# ==========================================================
# SHOW ALL OBJECTS
# ==========================================================

print("\n===== ALL OBJECTS IN MODEL =====")
for obj in model.get_track_object_list():
    print(" ->", obj)

print("\n===== DONE =====\n")
