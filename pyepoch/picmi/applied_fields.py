import picmistandard

from pyepoch.picmi import UnsupportedClassError


class AnalyticAppliedField(picmistandard.PICMI_AnalyticAppliedField):

    def __init__(self, **kw):
        raise UnsupportedClassError
        # noinspection PyUnreachableCode
        super().__init__(**kw)


class ConstantAppliedField(picmistandard.PICMI_ConstantAppliedField):
    def __init__(self, **kw):
        raise UnsupportedClassError
        # noinspection PyUnreachableCode
        super().__init__(**kw)


class Mirror(picmistandard.PICMI_Mirror):
    def __init__(self, **kw):
        raise UnsupportedClassError
        # noinspection PyUnreachableCode
        super().__init__(**kw)
