import math
from pyepoch import picmi
from scipy.constants import c, m_e, epsilon_0, e


def critical(omega):
    return omega ** 2 * m_e * epsilon_0 / e ** 2


def get_simulation():
    micron = 1e-6
    femto = 1e-15
    xmin = -10 * micron
    xmax = -xmin
    ymin = xmin
    ymax = xmax
    max_time = 50 * femto
    grid = picmi.Cartesian2DGrid(
        nx=249,
        ny=249,
        xmin=xmin,
        xmax=xmax,
        ymin=ymin,
        ymax=ymax,
        bc_xmin="simple_laser",  # simple_laser is not standard
        bc_xmax="simple_outflow",  # simple_outflow is not standard
        bc_ymin="periodic",
        bc_ymax="periodic",
        epoch_enable_bcs=True
    )
    solver = picmi.ElectromagneticSolver(grid)
    simulation = picmi.Simulation(solver, max_time=max_time)

    lamb = 1.06 * micron
    omega = 2 * math.pi * c / lamb
    den_cone = 4 * critical(omega)
    th = 1 * micron / 2
    ri = "abs(x - 5*{}) - sqrt(2.0) * th".format(micron)
    ro = "abs(x - 5*{}) - sqrt(2.0) * th".format(micron)
    xi = "3*{} - th".format(micron)
    xo = "3*{} + th".format(micron)
    r = "sqrt(y^2)"
    initial_density = "where(({r} > {ri}) & ({r} < {ro}), {den_cone}, 0.0".format(
        r=r,
        ri=ri,
        ro=ro,
        den_cone=den_cone
    )
    initial_density = "where((x > {xi}) & (x < {xo}) & ({r} < {ri}), {den_cone}, {dens})".format(
        xi=xi,
        xo=xo,
        r=r,
        ri=ri,
        den_cone=den_cone,
        dens=initial_density
    )
    initial_density = "where((x > {xo}), 0.0, {dens}".format(
        xo=xo,
        dens=initial_density
    )
    plasma_distribution = picmi.AnalyticDistribution(
        density_expression=initial_density,
        th=th
    )

    plasma = picmi.MultiSpecies(
        particle_types=["proton", "electron"],
        names=["proton", "electron"],
        initial_distribution=plasma_distribution
    )

    plasma_layout = picmi.PseudoRandomLayout(
        n_macroparticles=4 * 250 * 250
    )

    laser = picmi.GaussianLaser(
        wavelength=lamb,
        waist=2 / math.sqrt(2) * 2.5 * micron,
        duration=max_time,
        E0=1e13
    )
    antena = picmi.LaserAntenna(
        position=[xmin, (ymax + ymin) / 2],
        normal_vector=[0, 1]
    )

    normal_diag_particles = picmi.ParticleDiagnostic(
        epoch_dt_snapshot=1 * femto,
        data_list=["position", "momentum", "weighting"],
        name="normal"
    )

    normal_diag_field = picmi.FieldDiagnostic(
        grid=grid,
        epoch_dt_snapshot=1 * femto,
        data_list=["E"],
        name="normal"
    )

    simulation.add_diagnostic(normal_diag_particles)
    simulation.add_diagnostic(normal_diag_field)

    simulation.add_laser(laser, injection_method=antena)

    simulation.add_species(plasma, plasma_layout)
    return simulation


def main():
    simulation = get_simulation()
    simulation.set_epoch_path("/home/martin/Sources/epoch-4.17.16/epoch2d/bin/epoch2d")
    simulation.set_processors_count(4)
    simulation.step()


if __name__ == '__main__':
    main()
