import unittest
from calculator_logic import (
    find_indexes,
    replace_negative,
    do_powers,
    do_multidiv,
    do_plussub,
    calculator
)


class TestCalculator(unittest.TestCase):
    def test_find_indexes_basic(self):
        test_str = "2+(3-5)"
        expected_return = (2, 6)
        self.assertEqual(find_indexes(test_str), expected_return)

    def test_find_indexes_basic_inner(self):
        test_str = "2+(3-(5-8)+7)"
        expected_return = (5, 9)
        self.assertEqual(find_indexes(test_str), expected_return)

    def test_find_indexes_err_no_nums(self):
        test_str = ""
        with self.assertRaises(ValueError):
            find_indexes(test_str)

    def test_replace_negative_valid(self):
        returned = replace_negative(-13)
        expected_return_in_re = r"n\d+n"
        self.assertRegex(returned, expected_return_in_re)

    def test_do_replace_negative_err_no_nums(self):
        test_str = ""
        with self.assertRaises(ValueError):
            replace_negative(test_str)

    def test_do_powers_simple(self):
        test_eq = "3^4"
        expected_return = "81.0"
        self.assertEqual(do_powers(test_eq), expected_return)

    def test_do_powers_with_addition(self):
        test_eq = "7+3^4"
        expected_return = "7+81.0"
        self.assertEqual(do_powers(test_eq), expected_return)

    def test_do_powers_err_no_nums(self):
        test_str = ""
        with self.assertRaises(ValueError):
            do_powers(test_str)

    def test_do_multidiv_simple(self):
        test_eq = "3*4"
        expected_return = "12.0"
        self.assertEqual(do_multidiv(test_eq), expected_return)

    def test_do_multidiv_with_addition(self):
        test_eq = "7+3*4"
        expected_return = "7+12.0"
        self.assertEqual(do_multidiv(test_eq), expected_return)

    def test_do_multidiv_err_no_nums(self):
        test_str = ""
        with self.assertRaises(ValueError):
            do_multidiv(test_str)

    def test_do_splussub_simple(self):
        test_eq = "3+4"
        expected_return = 7.0
        self.assertEqual(do_plussub(test_eq), expected_return)

    def test_do_plussub_multiple(self):
        test_eq = "7+3+4"
        expected_return = 14.0
        self.assertEqual(do_plussub(test_eq), expected_return)

    def test_do_plussub_err_no_nums(self):
        test_str = ""
        with self.assertRaises(ValueError):
            do_plussub(test_str)

    def test_calculator(self):
        test_eq = "7+(3+4^3)-13*2"
        expected_return = 48.0
        self.assertEqual(calculator(test_eq), expected_return)

    def test_calculator_err_no_nums(self):
        test_str = ""
        self.assertRaises(ValueError, calculator, test_str)
