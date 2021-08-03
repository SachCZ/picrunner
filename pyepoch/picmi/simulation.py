import itertools
import math
from copy import deepcopy

import picmistandard
from pyepoch.picmi.grids import Cartesian2DGrid
from pyepoch.picmi.particles import MultiSpecies, AnalyticDistribution
from pyepoch.picmi.fbpic_charge_and_mass import particle_charge, particle_mass
from pyepoch.picmi.diagnostics import ParticleDiagnostic, FieldDiagnostic
from pyepoch.picmi.particles import GriddedLayout, PseudoRandomLayout


class Simulation(picmistandard.PICMI_Simulation):
    def init(self, kw):
        pass

    def write_input_file(self, file_name):
        if not isinstance(self.solver.grid, Cartesian2DGrid):
            raise Exception('pyepoch supports only Cartesian2DGrid')
        with open(file_name, "w") as f:
            self._write_control(f)
            self._write_boundaries(f)
            layout_species = self._get_layout_species()
            for s, layout in layout_species:
                self._write_species(s, layout, f)
            for laser, method in zip(self.lasers, self.laser_injection_methods):
                self._write_laser(laser, method, f)
            particle_diag = [diag for diag in self.diagnostics if isinstance(diag, ParticleDiagnostic)]
            field_diag = [diag for diag in self.diagnostics if isinstance(diag, FieldDiagnostic)]
            reduced_field_diag = []
            for pd, fd in itertools.product(particle_diag, field_diag):
                if pd.name == fd.name:
                    if pd.period != fd.period or pd.dt_snapshot != fd.dt_snapshot:
                        raise Exception("Diagnostics with same name must have same period")
                    pd.data_list += fd.data_list
                else:
                    reduced_field_diag.append(fd)
            diagnostics = particle_diag + reduced_field_diag
            for diag in diagnostics:
                self._write_diagnostics(diag, self.solver.grid, f)

    def _get_layout_species(self):
        for s, layout in zip(self.species, self.layouts):
            if isinstance(s, MultiSpecies):
                for s_in in s.species_instances_list:
                    yield s_in, layout
            else:
                yield s, layout

    def _write_control(self, opened_file):
        grid = self.solver.grid

        opened_file.write("begin:control\n")
        opened_file.write("    nx = {}\n".format(int(grid.nx + 1)))
        opened_file.write("    ny = {}\n".format(int(grid.ny + 1)))
        opened_file.write("    t_end = {}\n".format(self.max_time))
        opened_file.write("    x_min = {}\n".format(grid.xmin))
        opened_file.write("    x_max = {}\n".format(grid.xmax))
        opened_file.write("    y_min = {}\n".format(grid.ymin))
        opened_file.write("    y_max = {}\n".format(grid.ymax))
        opened_file.write("end:control\n\n")

    def _write_boundaries(self, opened_file):
        grid = self.solver.grid

        opened_file.write("begin:boundaries\n")
        opened_file.write("    bc_x_min = {}\n".format(grid.bc_xmin))
        opened_file.write("    bc_x_max = {}\n".format(grid.bc_xmax))
        opened_file.write("    bc_y_min = {}\n".format(grid.bc_ymin))
        opened_file.write("    bc_y_max = {}\n".format(grid.bc_ymax))
        opened_file.write("end:boundaries\n\n")

    def _write_species(self, s, layout, opened_file):
        charge = s.charge if s.charge else particle_charge[s.particle_type]
        mass = s.charge if s.mass else particle_mass[s.particle_type]
        opened_file.write("begin:species\n")
        opened_file.write("    name = {}\n".format(s.name))
        opened_file.write("    charge = {}\n".format(charge / particle_charge["proton"]))
        opened_file.write("    mass = {}\n".format(mass / particle_mass["electron"]))
        if isinstance(layout, GriddedLayout):
            opened_file.write("    nparticles_per_cell = {}\n".format(layout.n_macroparticle_per_cell))
        elif isinstance(layout, PseudoRandomLayout):
            opened_file.write("    nparticles = {}\n".format(layout.n_macroparticles))
        if isinstance(s.initial_distribution, AnalyticDistribution):
            opened_file.write("    number_density = {}\n".format(s.initial_distribution.get_parsed_density_expresion()))
        else:
            raise Exception('pyepoch supports only analytic distribution for species initial distribution')

        opened_file.write("end:species\n\n")

    def _write_laser(self, laser, method, opened_file):

        opened_file.write("begin:constant\n")
        boundary = ""
        grid = self.solver.grid
        if len(method.position) == 2:
            if method.position[0] == grid.xmin:
                boundary = "x_min"
                opened_file.write("    r = sqrt((y - {})^2)\n".format(method.position[1]))
            elif method.position[0] == grid.xmax:
                boundary = "x_max"
                opened_file.write("    r = sqrt((y - {})^2)\n".format(method.position[1]))
            elif method.position[1] == grid.ymin:
                boundary = "y_min"
                opened_file.write("    r = sqrt((x - {})^2)\n".format(method.position[0]))
            elif method.position[1] == grid.ymax:
                boundary = "y_max"
                opened_file.write("    r = sqrt((x - {})^2)\n".format(method.position[0]))
            else:
                raise Exception('pyepoch supports only laser antena at a boundary')

        else:
            raise Exception('pyepoch supports only 2d geometry')
        opened_file.write("end:constant\n\n")

        opened_file.write("begin:laser\n")
        opened_file.write("    boundary = {}\n".format(boundary))
        opened_file.write("    amp = {}\n".format(laser.E0))
        opened_file.write("    lambda = {}\n".format(laser.wavelength))
        opened_file.write("    profile = gauss(r, 0.0, {})\n".format(laser.waist * math.sqrt(2) / 2))
        opened_file.write("end:laser\n\n")

    def _write_diagnostics(self, diag, grid, opened_file):
        if not isinstance(grid, Cartesian2DGrid):
            raise Exception("Only 2DGrid is supported")

        opened_file.write("begin:output\n")
        opened_file.write("    name = {}\n".format(diag.name))
        if diag.dt_snapshot:
            opened_file.write("    dt_snapshot = {}\n".format(diag.dt_snapshot))
        else:
            opened_file.write("    nstep_snapshot = {}\n".format(diag.period))
        if "position" in diag.data_list:
            opened_file.write("    particles = always\n")
        if "momentum" in diag.data_list:
            opened_file.write("    px = always\n")
            opened_file.write("    py = always\n")
        if "weighting" in diag.data_list:
            opened_file.write("    particle_weight = always\n")
        if "E" in diag.data_list:
            opened_file.write("    grid = always\n")  # TODO this doesnt scale at all
            opened_file.write("    ex = always\n")
            opened_file.write("    ey = always\n")

        opened_file.write("end:output\n\n")
