import unittest
from io import StringIO

from pyepoch import picmi
from pyepoch.picmi.parsers import write_control, write_boundary


class TestParsers(unittest.TestCase):
    def setUp(self):
        micron = 1e-6
        femto = 1e-15
        xmin = -10 * micron
        xmax = -xmin
        ymin = xmin
        ymax = xmax
        self.max_time = 50 * femto
        self.grid = picmi.Cartesian2DGrid(
            nx=249,
            ny=249,
            xmin=xmin,
            xmax=xmax,
            ymin=ymin,
            ymax=ymax,
            bc_xmin="simple_laser",
            bc_xmax="simple_outflow",
            bc_ymin="periodic",
            bc_ymax="periodic",
            epoch_enable_bcs=True
        )

    def tearDown(self):
        pass

    def test_write_control(self):
        with StringIO("") as s:
            write_control(self.grid, self.max_time, s)
            result = s.getvalue()

        self.assertEqual(result, (
            "begin:control\n"
            "    nx = 250\n"
            "    ny = 250\n"
            "    t_end = 5e-14\n"
            "    x_min = -9.999999999999999e-06\n"
            "    x_max = 9.999999999999999e-06\n"
            "    y_min = -9.999999999999999e-06\n"
            "    y_max = 9.999999999999999e-06\n"
            "end:control\n\n"
        ))

    def test_write_boundary(self):
        with StringIO("") as s:
            write_boundary(self.grid, s)
            result = s.getvalue()

        self.assertEqual(result, (
            "begin:boundaries\n"
            "    bc_x_min = simple_laser\n"
            "    bc_x_max = simple_outflow\n"
            "    bc_y_min = periodic\n"
            "    bc_y_max = periodic\n"
            "end:boundaries\n\n"
        ))
