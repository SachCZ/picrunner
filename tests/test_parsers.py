import unittest
from io import StringIO

from pyepoch import picmi
from scipy.constants import e, m_p, m_e
from pyepoch.picmi.parsers import write_control, write_boundaries, parse_expression, parse_layouts_species, \
    infer_charge_mass, write_species


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
        self.distribution = picmi.AnalyticDistribution(
            density_expression="where(x>5, 10, 0)"
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

    def test_write_boundaries(self):
        with StringIO("") as s:
            write_boundaries(self.grid, s)
            result = s.getvalue()

        self.assertEqual(result, (
            "begin:boundaries\n"
            "    bc_x_min = simple_laser\n"
            "    bc_x_max = simple_outflow\n"
            "    bc_y_min = periodic\n"
            "    bc_y_max = periodic\n"
            "end:boundaries\n\n"
        ))

    def test_parse_expression(self):
        self.assertEqual("if  and   or   gt   lt   eq ", parse_expression("where & | > < =="))

    def test_parse_layout_species(self):
        single_species = picmi.Species(
            particle_type="He",
            name="helium",
            initial_distribution=self.distribution
        )
        layout_single = picmi.PseudoRandomLayout(
            n_macroparticles_per_cell=10
        )
        multi_species = picmi.MultiSpecies(
            particle_types=["proton", "electron"],
            names=["protons", "electrons"],
            initial_distribution=self.distribution
        )
        layout_multi = picmi.PseudoRandomLayout(
            n_macroparticles=2000
        )
        result = list(parse_layouts_species([layout_single, layout_multi], [single_species, multi_species]))
        self.assertEqual(3, len(result))
        self.assertDictEqual(result[0], {
            "type": "He",
            "name": "helium",
            "charge": None,
            "mass": None,
            "number_density": "if(x gt 5, 10, 0)",
            "nparticles_per_cell": 10
        })
        self.assertDictEqual(result[1], {
            "type": "proton",
            "name": "protons",
            "charge": None,
            "mass": None,
            "number_density": "if(x gt 5, 10, 0)",
            "nparticles": 2000
        })
        self.assertDictEqual(result[2], {
            "type": "electron",
            "name": "electrons",
            "charge": None,
            "mass": None,
            "number_density": "if(x gt 5, 10, 0)",
            "nparticles": 2000
        })

    def test_infer_charge_mass(self):
        parsed_species = {
            "type": "proton",
            "name": "protons",
            "charge": None,
            "mass": None,
            "number_density": "if(x gt 5, 10, 0)",
            "nparticles": 2000
        }
        result = infer_charge_mass(parsed_species)
        self.assertAlmostEqual(result["charge"], -e)
        self.assertAlmostEqual(result["mass"], m_p)

    def test_write_species(self):
        parsed_species = {
            "type": "electron",
            "name": "electrons",
            "charge": -e,
            "mass": m_e,
            "number_density": "if(x gt 5, 10, 0)",
            "nparticles": 2000
        }
        with StringIO("") as s:
            write_species(parsed_species, s)
            result = s.getvalue()

        self.assertEqual(result, (
            "begin:species\n"
            "    name = electrons\n"
            "    charge = -1.0\n"
            "    mass = 1.0\n"
            "    nparticles = 2000\n"
            "    number_density = if(x gt 5, 10, 0)\n"
            "end:species\n\n"
        ))
