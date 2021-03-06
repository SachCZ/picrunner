# Copyright 2019, FBPIC contributors
# Authors: Remi Lehe, Manuel Kirchen
# License: 3-Clause-BSD-LBNL
"""
This file is taken as is from FBPIC
"""

from scipy.constants import e, m_e, m_p, m_n, physical_constants
import periodictable

particle_charge = {
    'electron': -e,
    'positron': e,
    'proton': e,
    'anti-proton': -e,
    'neutron': 0,
    'anti-neutron': 0,
}
particle_mass = {
    'electron': m_e,
    'positron': m_e,
    'proton': m_p,
    'anti-proton': m_p,
    'neutron': m_n,
    'anti-neutron': m_n,
}

m_u = physical_constants['atomic mass constant'][0]
for el in periodictable.elements:
    particle_mass[el.symbol] = el.mass * m_u
    particle_charge[el.symbol] = 0
