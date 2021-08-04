import picmistandard
from pyepoch.picmi.grids import Cartesian2DGrid
from pyepoch.picmi.parsers import write_control, write_boundaries, parse_layouts_species, infer_charge_mass, \
    write_species, parse_diagnostics, write_diagnostic, write_laser, parse_laser_method


class Simulation(picmistandard.PICMI_Simulation):
    def step(self, nsteps=1):
        pass

    def init(self, kw):
        pass

    def write_input_file(self, file_name):
        grid = self.solver.grid
        if not isinstance(grid, Cartesian2DGrid):
            raise Exception('pyepoch supports only Cartesian2DGrid')
        with open(file_name, "w") as f:
            write_control(grid, self.max_time, f)
            write_boundaries(grid, f)
            parsed_species = parse_layouts_species(self.layouts, self.species)
            parsed_species = [infer_charge_mass(ps) for ps in parsed_species]
            for s in parsed_species:
                write_species(s, f)
            parsed_diagnostics = parse_diagnostics(self.diagnostics)
            for d in parsed_diagnostics:
                write_diagnostic(d, 2, f)  # TODO remove hardcoded dimension

            parsed_lasers = [parse_laser_method(r, m, grid) for r, m in zip(self.lasers, self.laser_injection_methods)]
            for r in parsed_lasers:
                write_laser(r, f)
