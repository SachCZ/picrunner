import unittest
from copy import deepcopy

import numpy as np

from pyepoch import picmi


class TestCartesian2DGrid(unittest.TestCase):
    def setUp(self):
        self.standard_kw = {
            "nx": 249,
            "ny": 135,
            "xmin": -10,
            "xmax": 5,
            "ymin": -20,
            "ymax": 15,
            "bc_xmin": "dirichlet",
            "bc_xmax": "neumann",
            "bc_ymin": "periodic",
            "bc_ymax": "open"
        }
        self.grid = picmi.Cartesian2DGrid(
            **self.standard_kw
        )

    def test_supported(self):
        self.assertEqual(self.grid.number_of_cells, [249, 135])
        np.testing.assert_almost_equal(self.grid.lower_bound, [-10, -20])
        np.testing.assert_almost_equal(self.grid.upper_bound, [5, 15])
        self.assertEqual(self.grid.lower_boundary_conditions, ["dirichlet", "periodic"])
        self.assertEqual(self.grid.upper_boundary_conditions, ["neumann", "open"])

    def test_check_bc(self):
        new_kw = deepcopy(self.standard_kw)
        for bc in ["bc_xmin", "bc_xmax", "bc_ymin", "bc_ymax"]:
            new_kw[bc] = "simple_laser"
            with self.assertRaises(picmi.InvalidBCError, msg="Should throw if {} is not standard".format(bc)):
                picmi.Cartesian2DGrid(**new_kw)

    def test_epoch_enable_bcs(self):
        new_kw = deepcopy(self.standard_kw)
        new_kw["bc_xmin"] = "simple_laser"
        new_kw["epoch_enable_bcs"] = True
        try:
            picmi.Cartesian2DGrid(**new_kw)
        except picmi.InvalidBCError:
            self.fail("grid should not throw when epoch_enable_bcs is True and non standard bs is specified")

    def test_unsupported(self):
        unsupported_args = ["moving_window_velocity", "refined_regions", "lower_bound_particles",
                            "upper_bound_particles", "xmin_particles", "xmax_particles", "ymin_particles",
                            "ymax_particles", "lower_boundary_conditions_particles",
                            "upper_boundary_conditions_particles", "bc_xmin_particles", "bc_xmax_particles",
                            "bc_ymin_particles", "bc_ymax_particles", "guard_cells", "pml_cells"]
        for arg in unsupported_args:
            with self.assertRaises(picmi.UnsupportedArgError, msg="Should throw if {} is specified".format(arg)):
                picmi.Cartesian2DGrid(**self.standard_kw, **{arg: 1})


class TestCartesian3DGrid(unittest.TestCase):
    def test_is_disabled(self):
        with self.assertRaises(picmi.UnsupportedClassError):
            picmi.Cartesian3DGrid()


class TestCylindricalGrid(unittest.TestCase):
    def test_is_disabled(self):
        with self.assertRaises(picmi.UnsupportedClassError):
            picmi.CylindricalGrid()
