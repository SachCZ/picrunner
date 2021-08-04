import unittest

from pyepoch import picmi


class TestAnalyticAppliedField(unittest.TestCase):
    def test_is_disabled(self):
        with self.assertRaises(picmi.UnsupportedClassError):
            picmi.AnalyticAppliedField()


class TestConstantAppliedField(unittest.TestCase):
    def test_is_disabled(self):
        with self.assertRaises(picmi.UnsupportedClassError):
            picmi.ConstantAppliedField()


class TestMirror(unittest.TestCase):
    def test_is_disabled(self):
        with self.assertRaises(picmi.UnsupportedClassError):
            picmi.Mirror()
