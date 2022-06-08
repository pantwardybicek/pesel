
from .validate import (validate_type, validate_str_format, validate_control_number, validate_dob,
                      needs_missing_fix, calculate_ymd)
from .fixers import fix_int, calculate_control, fix_missing_number, mask_irrelevant


class PESEL:
    """
    Instantiation parameteres:
        :param number: int or str - PESEL number, this can be either an integer (see: fix_integer),
            or a string of digits.
            The string must be appropriate length but one of the numbers can be missing and
            replaced with any non digit ASCII symbol. The missing number will be calculated and substituted.
        :param fix_integer: bool - if True fixes integers by adding zeros in front, default = True.

    Attributes:
        pesel - PESEL number
        dob - date of birth as a datetime.date object
        gender - gender derived from the PESEL number as one of 'K' (female) or 'M' (male)

    Methods:
        mask(token='x') - returns a masked PESEL number, as a string, with only dob and gender visible

    Class methods:
        control(numbers: str) : accepts 10 digit string and calculates the 11th number (control number)
        fix(p) : accepts an 11-digits string with one number replaced with any non digit ASCII symbol,
        returns the missing number
    """

    __slots__ = ('input_', 'pesel', 'fix_int')

    def __init__(self, number, fix_integer=True):
        self.input_ = number
        self.fix_int = fix_integer

        validate_type(number)
        self.pesel = str(number)

        if self.fix_int:
            self.pesel = fix_int(self.pesel)

        validate_str_format(self.pesel)

        if needs_missing_fix(self.pesel):
            self.pesel = fix_missing_number(self.pesel)

        validate_control_number(self.pesel)
        validate_dob(self.pesel)

    @classmethod
    def control(cls, numbers):
        """
        :param numbers: a string of 10 digits
        :return: missing number as a type int.
        """
        return calculate_control(numbers)

    @classmethod
    def fix(cls, p):
        """
        finds missing value in pesel if replaced with any non-digit ASCII symbol
        :param p: pesel number - a string with one of the digits replaced with any non digit ASCII symbol."""
        if not isinstance(p, str):
            raise TypeError('Can only fix missing number if passed value is type string.')
        if not needs_missing_fix(p):
            return p
        return fix_missing_number(p)

    @property
    def gender(self):
        if int(self.pesel[-2]) % 2:
            return 'M'
        else:
            return 'K'

    @property
    def dob(self):
        """date of birth"""
        return calculate_ymd(self.pesel)

    def mask(self, token='x'):
        return mask_irrelevant(self.pesel, self.gender, token)

    def __repr__(self):
        return f'PESEL:{self.pesel}'


def mask_pesel(pes, token='x'):
    return PESEL(pes).mask(token=token)
