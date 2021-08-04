import picmistandard

from pyepoch.picmi import UnsupportedArgError, UnsupportedClassError


class LaserAntenna(picmistandard.PICMI_LaserAntenna):
    def init(self, kw):
        pass


class GaussianLaser(picmistandard.PICMI_GaussianLaser):
    unsupported_args = ["focal_position", "centroid_position", "propagation_direction", "polarization_direction",
                        "a0", "phi0", "zeta", "beta", "phi2", "name", "fill_in"]

    def __init__(self, **kw):
        for key in kw:
            if key in self.unsupported_args:
                raise UnsupportedArgError("{} is not supported".format(key))

        super().__init__(**kw)

    def init(self, kw):
        pass


class AnalyticLaser(picmistandard.PICMI_AnalyticLaser):
    def __init__(self, **kw):
        raise UnsupportedClassError
        # noinspection PyUnreachableCode
        super().__init__(**kw)
