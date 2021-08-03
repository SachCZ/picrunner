import picmistandard


class ParticleDiagnostic(picmistandard.PICMI_ParticleDiagnostic):
    def __init__(self, epoch_dt_snapshot=None, **kw):
        self.dt_snapshot = None
        super().__init__(epoch_dt_snapshot=epoch_dt_snapshot, **kw)

    def init(self, kw):
        self.dt_snapshot = kw.pop("epoch_dt_snapshot")


class FieldDiagnostic(picmistandard.PICMI_FieldDiagnostic):
    def __init__(self, epoch_dt_snapshot=None, **kw):
        self.dt_snapshot = None
        super().__init__(epoch_dt_snapshot=epoch_dt_snapshot, **kw)

    def init(self, kw):
        self.dt_snapshot = kw.pop("epoch_dt_snapshot")
