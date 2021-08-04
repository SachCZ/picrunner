import picmistandard

from pyepoch.picmi.exceptions import UnsupportedArgError, UnsupportedClassError, PyEpochError


class InvalidDataError(PyEpochError):
    pass


class ParticleDiagnostic(picmistandard.PICMI_ParticleDiagnostic):
    unsupported_args = ["species", "write_dir", "step_min", "step_max", "parallelio"]
    supported_data = ["position", "momentum", "weighting"]

    def __init__(self, epoch_dt_snapshot=None, **kw):
        self.dt_snapshot = epoch_dt_snapshot
        for key in kw:
            if key in self.unsupported_args:
                raise UnsupportedArgError("{} is not supported".format(key))
        super().__init__(**kw)
        if not self.name:
            raise UnsupportedArgError("name is required in epoch diagnostics")
        for var in self.data_list:
            if var not in self.supported_data:
                raise InvalidDataError("{} not supported for diagnostics".format(var))

    def init(self, kw):
        pass


class FieldDiagnostic(picmistandard.PICMI_FieldDiagnostic):
    unsupported_args = ["write_dir", "step_min", "step_max", "parallelio", "number_of_cells", "lower_bound",
                        "upper_bound"]
    supported_data = ["rho", "E", "B", "J"]

    def __init__(self, grid, epoch_dt_snapshot=None, **kw):
        self.dt_snapshot = epoch_dt_snapshot
        for key in kw:
            if key in self.unsupported_args:
                raise UnsupportedArgError("{} is not supported".format(key))
        super().__init__(grid, **kw)
        if not self.name:
            raise UnsupportedArgError("name is required in epoch diagnostics")
        for var in self.data_list:
            if var not in self.supported_data:
                raise InvalidDataError("{} not supported for diagnostics".format(var))

    def init(self, kw):
        pass


class ElectrostaticFieldDiagnostic(picmistandard.PICMI_ElectrostaticFieldDiagnostic):
    def __init__(self, **kw):
        raise UnsupportedClassError
        # noinspection PyUnreachableCode
        super().__init__(**kw)


class LabFrameParticleDiagnostic(picmistandard.PICMI_LabFrameParticleDiagnostic):
    def __init__(self, **kw):
        raise UnsupportedClassError
        # noinspection PyUnreachableCode
        super().__init__(**kw)


class LabFrameFieldDiagnostic(picmistandard.PICMI_LabFrameFieldDiagnostic):
    def __init__(self, **kw):
        raise UnsupportedClassError
        # noinspection PyUnreachableCode
        super().__init__(**kw)
