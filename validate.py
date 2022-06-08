
from .errors import PESELError
from .back import DIGIT_WEIGHTS, YEARS, MONTH_ADD_ON, MAX_MONTH_DAYS
import datetime


def validate_int_len(pes):
    if len(str(pes)) > 11:
        raise PESELError('Invalid lenght. Can not accept more than 11 digits.')
    elif len(str(pes)) < 8:
        raise PESELError('Invalid length. Can not accept les than 9 digits.')


def validate_type(pes):
    if isinstance(pes, (str, int)):
        return True
    else:
        raise PESELError('Can accept only type int or str.') from TypeError


def validate_str_format(pes):
    if len(pes) != 11:
        raise PESELError('Invalid PESEL length. Expected 11 digits.')

    numbers = [n for n in pes if n.isdigit()]
    if len(numbers) < 10:
        raise PESELError('Could not interpret the input value. Check __doc__.')


def validate_control_number(pes):
    if sum(int(a)*b for a, b in zip(pes, DIGIT_WEIGHTS)) % 10 == 0:
        return True
    else:
        raise PESELError(f'Invalid PESEL number: {pes}. Control number does not match. Check input value.')


def validate_missing_sequence(pes):
    if not isinstance(pes, str):
        raise TypeError('Can can only fix missing number if passed pesel is type str.')
    if len(pes) != 11:
        raise ValueError('Can only fix missing number if passed string has 11 signs')
    if sum([n.isdigit() for n in pes]) != 10:
        raise ValueError('Can only fix missing number if 10 other digits are present')
    return True


def needs_missing_fix(pes):
    if all((n.isdigit() for n in pes)):
        return False
    else:
        return True


def validate_month(month: str):
    m = int(month) % 20
    if 1 > m or m > 12:
        raise ValueError(f'Invalid month coding: {month}')
    else:
        return True


def validate_day(day: str):
    d = int(day)
    if 1 > d or d > 31:
        raise ValueError(f'Invalid day coding: {day}')
    else:
        return True


def validate_daymonth(day, month):
    m = int(month) % 20
    if MAX_MONTH_DAYS[m] >= int(day):
        return True
    else:
        raise ValueError(f'Month {month} can not have {day} days.')


def validate_dob(pes):
    m = pes[2:4]
    d = pes[4:6]
    try:
        validate_month(m)
        validate_day(d)
        validate_daymonth(d, m)
    except ValueError as err:
        raise PESELError('Invalid date of birth coding.') from err
    else:
        return True


def calculate_ymd(pes):
    y = pes[0:2]
    m = pes[2:4]
    d = pes[4:6]
    maddon = (int(m) // 20) * 20
    y = YEARS[MONTH_ADD_ON.index(maddon)] + int(y)
    return datetime.date(y, int(m) % 20, int(d))
