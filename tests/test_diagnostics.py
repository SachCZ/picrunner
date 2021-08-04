import unittest

from pyepoch import picmi


class TestParticleDiagnostics(unittest.TestCase):
    def test_supported(self):
        diagnostics = picmi.ParticleDiagnostic(
            name="normal",
            period=10,
            data_list=["position"]
        )
        self.assertEqual(diagnostics.name, "normal")
        self.assertEqual(diagnostics.period, 10)
        self.assertEqual(diagnostics.data_list, ["position"])

    def test_epoch_dt_snapshot_is_supported(self):
        diagnostics = picmi.ParticleDiagnostic(
            name="normal",
            epoch_dt_snapshot=1e-3
        )
        self.assertAlmostEqual(diagnostics.dt_snapshot, 1e-3)

    def test_name_is_required(self):
        with self.assertRaises(picmi.UnsupportedArgError, msg="should throw is name is not supplied"):
            picmi.ParticleDiagnostic()

    def test_unsupported(self):
        unsupported_args = ["species", "write_dir", "step_min", "step_max", "parallelio"]
        for arg in unsupported_args:
            with self.assertRaises(picmi.UnsupportedArgError, msg="Should throw if {} is specified".format(arg)):
                picmi.ParticleDiagnostic(name="normal", **{arg: 1})

    def test_supported_data_is_checked(self):
        with self.assertRaises(picmi.InvalidDataError):
            picmi.ParticleDiagnostic(name="normal", data_list=["psi"])


class TestFieldDiagnostics(unittest.TestCase):
    def test_supported(self):
        diagnostics = picmi.FieldDiagnostic(
            grid=1,
            name="normal",
            period=10,
            data_list=["E"]
        )
        self.assertEqual(diagnostics.name, "normal")
        self.assertEqual(diagnostics.period, 10)
        self.assertEqual(diagnostics.data_list, ["E"])

    def test_epoch_dt_snapshot_is_supported(self):
        diagnostics = picmi.FieldDiagnostic(
            grid=1,
            name="normal",
            epoch_dt_snapshot=1e-3
        )
        self.assertAlmostEqual(diagnostics.dt_snapshot, 1e-3)

    def test_name_is_required(self):
        with self.assertRaises(picmi.UnsupportedArgError, msg="should throw is name is not supplied"):
            picmi.FieldDiagnostic(grid=1)

    def test_unsupported(self):
        unsupported_args = ["write_dir", "step_min", "step_max", "parallelio", "number_of_cells", "lower_bound",
                            "upper_bound"]
        for arg in unsupported_args:
            with self.assertRaises(picmi.UnsupportedArgError, msg="Should throw if {} is specified".format(arg)):
                picmi.FieldDiagnostic(grid=1, name="normal", **{arg: 1})

    def test_supported_data_is_checked(self):
        with self.assertRaises(picmi.InvalidDataError):
            picmi.ParticleDiagnostic(name="normal", data_list=["psi"])


class TestElectrostaticFieldDiagnostic(unittest.TestCase):
    def test_is_disabled(self):
        with self.assertRaises(picmi.UnsupportedClassError):
            picmi.ElectrostaticFieldDiagnostic()


class TestLabFrameParticleDiagnostic(unittest.TestCase):
    def test_is_disabled(self):
        with self.assertRaises(picmi.UnsupportedClassError):
            picmi.LabFrameParticleDiagnostic()


class TestLabFrameFieldDiagnostic(unittest.TestCase):
    def test_is_disabled(self):
        with self.assertRaises(picmi.UnsupportedClassError):
            picmi.LabFrameFieldDiagnostic()
