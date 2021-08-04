import unittest
from pyepoch import picmi


class TestElectromagneticSolver(unittest.TestCase):
    def test_supported(self):
        solver = picmi.ElectromagneticSolver(
            grid=1  # there would be grid
        )
        self.assertEqual(solver.grid, 1)

    def test_only_yee_supported(self):
        with self.assertRaises(picmi.InvalidMethodError):
            picmi.ElectromagneticSolver(
                grid=1,  # there would be grid
                method="Lehe"
            )

    def test_unsupported(self):
        unsupported_args = ["stencil_order", "cfl", "I_nodal", "source_smoother", "field_smoother", "subcycling",
                            "galilean_velocity"]
        for arg in unsupported_args:
            with self.assertRaises(picmi.UnsupportedArgError, msg="Should throw if {} is specified".format(arg)):
                picmi.ElectromagneticSolver("x", **{arg: 1})


class TestElectrostaticSolver(unittest.TestCase):
    def test_is_disabled(self):
        with self.assertRaises(picmi.UnsupportedClassError):
            picmi.ElectrostaticSolver()
