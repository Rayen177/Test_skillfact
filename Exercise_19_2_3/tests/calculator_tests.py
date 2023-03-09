import pytest
from app.calculator import Calculator

class TestCalc:
    def setup(self):
        self.calc = Calculator

    def test_multi_pass(self):
        assert self.calc.multiply(self, 2, 2) == 4

    def test_devision_pass(self):
        assert self.calc.devision(self, 27, 9) == 3

    def test_adding_pass(self):
        assert self.calc.adding(self, 11, 23) == 34

    def test_subtraction_pass(self):
        assert self.calc.subtraction(self, 56, 45) == 11