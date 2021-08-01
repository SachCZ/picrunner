import picmistandard
from scipy.constants import m_e, c, e
from pyepoch.picmi.simulation import Simulation
from pyepoch.picmi.grids import Cartesian2DGrid
from pyepoch.picmi.solvers import ElectromagneticSolver
from pyepoch.picmi.particles import MultiSpecies, GriddedLayout, AnalyticDistribution, Species
from pyepoch.picmi.lasers import LaserAntenna, GaussianLaser


class Constants:
    m_e = m_e
    c = c
    q_e = e


picmistandard.register_constants(
    Constants()
)
picmistandard.register_codename("epoch")
