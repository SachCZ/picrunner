import unittest

from pyepoch import picmi


class TestLaserAntenna(unittest.TestCase):
    def test_supported(self):
        antenna = picmi.LaserAntenna(
            position=[3, 2],
            normal_vector=[1, 0]
        )
        self.assertEqual(antenna.position, [3, 2])
        self.assertEqual(antenna.normal_vector, [1, 0])


class TestGaussianLaser(unittest.TestCase):
    def setUp(self):
        self.standard_kw = {
            "wavelength": 100,
            "waist": 10,
            "duration": 15,
            "E0": 1e13
        }

    def test_supported(self):
        laser = picmi.GaussianLaser(**self.standard_kw)
        self.assertEqual(laser.wavelength, 100)
        self.assertEqual(laser.waist, 10)
        self.assertEqual(laser.duration, 15)
        self.assertAlmostEqual(laser.E0, 1e13)

    def test_unsupported(self):
        unsupported_args = ["focal_position", "centroid_position", "propagation_direction", "polarization_direction",
                            "a0", "phi0", "zeta", "beta", "phi2", "name", "fill_in"]

        for arg in unsupported_args:
            with self.assertRaises(picmi.UnsupportedArgError, msg="Should throw if {} is specified".format(arg)):
                picmi.GaussianLaser(**self.standard_kw, **{arg: 1})


class TestAnalyticLaser(unittest.TestCase):
    def test_is_disabled(self):
        with self.assertRaises(picmi.UnsupportedClassError):
            picmi.AnalyticLaser()
