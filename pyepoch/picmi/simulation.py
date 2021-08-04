import math

import picmistandard
from pyepoch.picmi.grids import Cartesian2DGrid
from pyepoch.picmi.parsers import write_control, write_boundaries, parse_layouts_species, infer_charge_mass, \
    write_species, parse_diagnostics, write_diagnostic


class Simulation(picmistandard.PICMI_Simulation):
    def init(self, kw):
        pass

    def write_input_file(self, file_name):
        if not isinstance(self.solver.grid, Cartesian2DGrid):
            raise Exception('pyepoch supports only Cartesian2DGrid')
        with open(file_name, "w") as f:
            write_control(self.solver.grid, self.max_time, f)
            write_boundaries(self.solver.grid, f)
            parsed_species = parse_layouts_species(self.layouts, self.species)
            parsed_species = [infer_charge_mass(ps) for ps in parsed_species]
            for s in parsed_species:
                write_species(s, f)
            parsed_diagnostics = parse_diagnostics(self.diagnostics)
            for d in parsed_diagnostics:
                write_diagnostic(d, 2, f)  # TODO remove hardcoded dimension

            for laser, method in zip(self.lasers, self.laser_injection_methods):
                self._write_laser(laser, method, f)

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
