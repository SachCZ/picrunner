import picmistandard
from scipy.constants import m_e, c, e
from pyepoch.picmi.simulation import Simulation
from pyepoch.picmi.grids import Cartesian2DGrid, Cartesian3DGrid, CylindricalGrid, InvalidBCError
from pyepoch.picmi.exceptions import UnsupportedArgError, UnsupportedClassError
from pyepoch.picmi.solvers import ElectromagneticSolver, ElectrostaticSolver, InvalidMethodError
from pyepoch.picmi.particles import MultiSpecies, GriddedLayout, AnalyticDistribution, Species, PseudoRandomLayout, \
    UniformDistribution, ParticleListDistribution, GaussianBunchDistribution
from pyepoch.picmi.lasers import LaserAntenna, GaussianLaser, AnalyticLaser
from pyepoch.picmi.diagnostics import ParticleDiagnostic, FieldDiagnostic, ElectrostaticFieldDiagnostic, \
    LabFrameFieldDiagnostic, LabFrameParticleDiagnostic, InvalidDataError
from pyepoch.picmi.applied_fields import AnalyticAppliedField, ConstantAppliedField, Mirror


class Constants:
    m_e = m_e
    c = c
    q_e = e


picmistandard.register_constants(
    Constants()
)
picmistandard.register_codename("epoch")
