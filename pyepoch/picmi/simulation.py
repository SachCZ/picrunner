import os
import subprocess

import picmistandard

from pyepoch.picmi.exceptions import PyEpochError
from pyepoch.picmi.grids import Cartesian2DGrid
from pyepoch.picmi.parsers import write_control, write_boundaries, parse_layouts_species, infer_charge_mass, \
    write_species, parse_diagnostics, write_diagnostic, write_laser, parse_laser_method


class Simulation(picmistandard.PICMI_Simulation):
    def __init__(self, solver, **kw):
        self.epoch_exe = ""
        self.processors_count = 1
        super().__init__(solver, **kw)

    def step(self, nsteps=1):
        if not self.epoch_exe:
            raise PyEpochError("epoch path not specified")

        os.mkdir("output")
        self.write_input_file("output/input.deck")

        with subprocess.Popen(
                ["mpirun", "-np", "{}".format(self.processors_count), self.epoch_exe],
                stdin=subprocess.PIPE
        ) as proc:
            proc.communicate(b"output")

    def init(self, kw):
        pass

    def write_input_file(self, file_name):
        with open(file_name, "w") as f:
            self.write_to_opened_file(f)

    def write_to_opened_file(self, f):
        grid = self.solver.grid
        if not isinstance(self.solver.grid, Cartesian2DGrid):
            raise Exception('pyepoch supports only Cartesian2DGrid')
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

    def set_processors_count(self, count):
        self.processors_count = count

    def set_epoch_path(self, epoch_path):
        self.epoch_exe = epoch_path
