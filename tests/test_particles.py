import unittest
from pyepoch import picmi


class TestAnalyticDistribution(unittest.TestCase):
    def test_supported(self):
        distribution = picmi.AnalyticDistribution(
            density_expression="x > x0",
            x0=5
        )
        self.assertEqual("x > 5", distribution.density_expression)

    def test_unsupported(self):
        unsupported_args = ["momentum_expression", "lower_bound", "upper_bound", "rms_velocity", "directed_velocity",
                            "fill_in"]
        for arg in unsupported_args:
            with self.assertRaises(picmi.UnsupportedArgError, msg="Should throw if {} is specified".format(arg)):
                picmi.AnalyticDistribution("x", **{arg: 1})


class TestPseudoRandomLayout(unittest.TestCase):
    def test_supports_per_cell(self):
        distribution = picmi.PseudoRandomLayout(
            n_macroparticles_per_cell=8
        )
        self.assertEqual(8, distribution.n_macroparticles_per_cell)

    def test_supports_total(self):
        distribution = picmi.PseudoRandomLayout(
            n_macroparticles=1000
        )
        self.assertEqual(1000, distribution.n_macroparticles)

    def test_unsupported(self):
        for arg in ["grid", "seed"]:
            with self.assertRaises(picmi.UnsupportedArgError, msg="Should throw if {} is specified".format(arg)):
                picmi.PseudoRandomLayout(n_macroparticles=1000, **{arg: 1})


class TestGriddedLayout(unittest.TestCase):
    def test_is_disabled(self):
        with self.assertRaises(picmi.UnsupportedClassError):
            picmi.GriddedLayout()


class TestGaussianBunchDistribution(unittest.TestCase):
    def test_is_disabled(self):
        with self.assertRaises(picmi.UnsupportedClassError):
            picmi.GaussianBunchDistribution()


class TestUniformDistribution(unittest.TestCase):
    def test_is_disabled(self):
        with self.assertRaises(picmi.UnsupportedClassError):
            picmi.UniformDistribution()


class TestParticleListDistribution(unittest.TestCase):
    def test_is_disabled(self):
        with self.assertRaises(picmi.UnsupportedClassError):
            picmi.ParticleListDistribution()
