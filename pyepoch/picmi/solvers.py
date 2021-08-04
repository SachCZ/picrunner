import picmistandard

from pyepoch.picmi.exceptions import PyEpochError, UnsupportedArgError, UnsupportedClassError


class InvalidMethodError(PyEpochError):
    pass


class ElectromagneticSolver(picmistandard.PICMI_ElectromagneticSolver):
    unsupported_args = ["stencil_order", "cfl", "I_nodal", "source_smoother", "field_smoother", "subcycling",
                        "galilean_velocity"]

    def __init__(self, grid, **kw):
        for key in kw:
            if key in self.unsupported_args:
                raise UnsupportedArgError("{} is not supported".format(key))

        super().__init__(grid, **kw)
        if not (self.method == "Yee" or self.method is None):
            raise InvalidMethodError("Only method Yee supported for epoch")

    def init(self, kw):
        pass


class ElectrostaticSolver(picmistandard.PICMI_ElectrostaticSolver):
    def __init__(self, **kw):
        raise UnsupportedClassError
        # noinspection PyUnreachableCode
        super().__init__(**kw)
