import picmistandard

from pyepoch.picmi.exceptions import PyEpochError, UnsupportedArgError, UnsupportedClassError


class InvalidBCError(PyEpochError):
    pass


class Cartesian2DGrid(picmistandard.PICMI_Cartesian2DGrid):
    standard_bcs = ["neumann", "dirichlet", "open", "periodic"]
    unsupported_args = ["moving_window_velocity", "refined_regions", "lower_bound_particles",
                        "upper_bound_particles", "xmin_particles", "xmax_particles", "ymin_particles",
                        "ymax_particles", "lower_boundary_conditions_particles",
                        "upper_boundary_conditions_particles", "bc_xmin_particles", "bc_xmax_particles",
                        "bc_ymin_particles", "bc_ymax_particles", "guard_cells", "pml_cells"]

    def __init__(self, epoch_enable_bcs=False, **kw):
        for key in kw:
            if key in self.unsupported_args:
                raise UnsupportedArgError("{} is not supported".format(key))
        self.epoch_enable_bcs = epoch_enable_bcs
        super().__init__(**kw)

    def init(self, kw):
        if not self.epoch_enable_bcs:
            for bc in [self.bc_xmin, self.bc_xmax, self.bc_ymin, self.bc_ymax]:
                if bc not in self.standard_bcs:
                    raise InvalidBCError(
                        "Invalid boundary condition {}, use epoch_enable_bcs=True to enable".format(bc)
                    )

        # TODO check epoch bcs vs standard particle bcs


class Cartesian3DGrid(picmistandard.PICMI_Cartesian3DGrid):
    def __init__(self, **kw):
        raise UnsupportedClassError
        # noinspection PyUnreachableCode
        super().__init__(**kw)


class CylindricalGrid(picmistandard.PICMI_CylindricalGrid):
    def __init__(self, **kw):
        raise UnsupportedClassError
        # noinspection PyUnreachableCode
        super().__init__(**kw)
