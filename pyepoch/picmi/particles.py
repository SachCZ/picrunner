import picmistandard

from pyepoch.picmi.exceptions import UnsupportedArgError, UnsupportedClassError


class Species(picmistandard.PICMI_Species):
    def init(self, kw):
        pass


class MultiSpecies(picmistandard.PICMI_MultiSpecies):
    def init(self, kw):
        pass


picmistandard.PICMI_MultiSpecies.Species_class = Species


class AnalyticDistribution(picmistandard.PICMI_AnalyticDistribution):
    unsupported_args = ["momentum_expression", "lower_bound", "upper_bound", "rms_velocity", "directed_velocity",
                        "fill_in"]

    def __init__(self, density_expression, **kw):
        for key in kw:
            if key in self.unsupported_args:
                raise UnsupportedArgError("{} is not supported".format(key))

        super().__init__(density_expression, **kw)

    def init(self, kw):
        for key in self.user_defined_kw:
            self.density_expression = self.density_expression.replace(key, "{}".format(self.user_defined_kw[key]))


class GaussianBunchDistribution(picmistandard.PICMI_GaussianBunchDistribution):
    def __init__(self, **kw):
        raise UnsupportedClassError
        # noinspection PyUnreachableCode
        super().__init__(**kw)


class UniformDistribution(picmistandard.PICMI_UniformDistribution):
    def __init__(self, **kw):
        raise UnsupportedClassError
        # noinspection PyUnreachableCode
        super().__init__(**kw)


class ParticleListDistribution(picmistandard.PICMI_ParticleListDistribution):
    def __init__(self, **kw):
        raise UnsupportedClassError
        # noinspection PyUnreachableCode
        super().__init__(**kw)


class GriddedLayout(picmistandard.PICMI_GriddedLayout):
    def __init__(self, **kw):
        raise UnsupportedClassError
        # noinspection PyUnreachableCode
        super().__init__(**kw)


class PseudoRandomLayout(picmistandard.PICMI_PseudoRandomLayout):
    unsupported_args = ["grid", "seed"]

    def __init__(self, **kw):
        for key in kw:
            if key in self.unsupported_args:
                raise UnsupportedArgError("{} is not supported".format(key))

        super().__init__(**kw)

    def init(self, kw):
        pass
