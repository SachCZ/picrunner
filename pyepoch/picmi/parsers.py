import itertools
from copy import copy

from pyepoch.picmi.diagnostics import ParticleDiagnostic, FieldDiagnostic
from pyepoch.picmi.exceptions import PyEpochError
from pyepoch.picmi.particles import MultiSpecies
from pyepoch.picmi.fbpic_charge_and_mass import particle_charge, particle_mass


def write_control(grid, final_time, opened_file):
    opened_file.write("begin:control\n")
    opened_file.write("    nx = {}\n".format(int(grid.nx + 1)))
    opened_file.write("    ny = {}\n".format(int(grid.ny + 1)))
    opened_file.write("    t_end = {}\n".format(final_time))
    opened_file.write("    x_min = {}\n".format(grid.xmin))
    opened_file.write("    x_max = {}\n".format(grid.xmax))
    opened_file.write("    y_min = {}\n".format(grid.ymin))
    opened_file.write("    y_max = {}\n".format(grid.ymax))
    opened_file.write("end:control\n\n")


def write_boundaries(grid, opened_file):
    opened_file.write("begin:boundaries\n")
    opened_file.write("    bc_x_min = {}\n".format(grid.bc_xmin))
    opened_file.write("    bc_x_max = {}\n".format(grid.bc_xmax))
    opened_file.write("    bc_y_min = {}\n".format(grid.bc_ymin))
    opened_file.write("    bc_y_max = {}\n".format(grid.bc_ymax))
    opened_file.write("end:boundaries\n\n")


def _parse_one_layout_species(layout, species):
    result = {
        "name": species.name,
        "type": species.particle_type,
        "charge": species.charge,
        "mass": species.mass,
        "number_density": parse_expression(species.initial_distribution.density_expression)
    }
    if layout.n_macroparticles_per_cell:
        result["nparticles_per_cell"] = layout.n_macroparticles_per_cell
    elif layout.n_macroparticles:
        result["nparticles"] = layout.n_macroparticles
    return result


def parse_layouts_species(layouts, species):
    for layout, s in zip(layouts, species):
        if isinstance(s, MultiSpecies):
            for s_in in s.species_instances_list:
                yield _parse_one_layout_species(layout, s_in)
        else:
            yield _parse_one_layout_species(layout, s)


def infer_charge_mass(parsed_species):
    result = copy(parsed_species)
    if result["type"] and not result["charge"]:
        result["charge"] = particle_charge[result["type"]]
    if result["type"] and not result["mass"]:
        result["mass"] = particle_mass[result["type"]]
    return result


def write_species(parsed_species, opened_file):
    opened_file.write("begin:species\n")
    opened_file.write("    name = {}\n".format(parsed_species["name"]))
    opened_file.write("    charge = {}\n".format(parsed_species["charge"] / particle_charge["proton"]))
    opened_file.write("    mass = {}\n".format(parsed_species["mass"] / particle_mass["electron"]))
    if "nparticles_per_cell" in parsed_species:
        opened_file.write("    nparticles_per_cell = {}\n".format(parsed_species["nparticles_per_cell"]))
    if "nparticles" in parsed_species:
        opened_file.write("    nparticles = {}\n".format(parsed_species["nparticles"]))
    opened_file.write("    number_density = {}\n".format(parsed_species["number_density"]))
    opened_file.write("end:species\n\n")


def parse_expression(expression):
    expression = expression.replace("where", "if").replace("&", " and ").replace(">", " gt ")
    return expression.replace("<", " lt ").replace("==", " eq ").replace("|", " or ")


class ParsingError(PyEpochError):
    pass


def _parse_one_diagnostic(name, data_list, period=None, dt_snapshot=None):
    result = {
        "name": name,
        "data_list": data_list
    }
    if dt_snapshot:
        result["dt_snapshot"] = dt_snapshot
    elif period:
        result["period"] = period
    else:
        raise Exception("Fatal error")
    return result


def parse_diagnostics(diagnostics):
    particle_diag = [diag for diag in diagnostics if isinstance(diag, ParticleDiagnostic)]
    field_diag = [diag for diag in diagnostics if isinstance(diag, FieldDiagnostic)]
    reduced_diagnostics = []
    omit_names = []
    for pd, fd in itertools.product(particle_diag, field_diag):
        if pd.name == fd.name:
            if pd.period != fd.period or pd.dt_snapshot != fd.dt_snapshot:
                raise ParsingError("Diagnostics with same name must have same period or if specified same dt_snapshot")
            reduced_diagnostics.append(
                _parse_one_diagnostic(pd.name, pd.data_list + fd.data_list, pd.period, pd.dt_snapshot))
            omit_names.append(pd.name)

    rest = [_parse_one_diagnostic(
        d.name,
        d.data_list,
        d.period,
        d.dt_snapshot
    ) for d in diagnostics if d.name not in omit_names]

    return reduced_diagnostics + rest


def write_diagnostic(parsed_diag, dimension, opened_file):
    axes = "xyz" if dimension == 3 else ("xy" if dimension == 2 else "x")
    opened_file.write("begin:output\n")
    opened_file.write("    name = {}\n".format(parsed_diag["name"]))
    if "dt_snapshot" in parsed_diag:
        opened_file.write("    dt_snapshot = {}\n".format(parsed_diag["dt_snapshot"]))
    else:
        opened_file.write("    nstep_snapshot = {}\n".format(parsed_diag["period"]))
    dl = parsed_diag["data_list"]
    if "position" in dl:
        opened_file.write("    particles = always\n")
    if "momentum" in dl:
        for ax in axes:
            opened_file.write("    p{} = always\n".format(ax))
    if "weighting" in dl:
        opened_file.write("    particle_weight = always\n")

    if "E" in dl or "B" in dl or "J" in dl:
        opened_file.write("    grid = always\n")
    if "E" in dl:
        for ax in axes:
            opened_file.write("    e{} = always\n".format(ax))
    if "B" in dl:
        for ax in axes:
            opened_file.write("    b{} = always\n".format(ax))
    if "J" in dl:
        for ax in axes:
            opened_file.write("    j{} = always\n".format(ax))

    opened_file.write("end:output\n\n")
