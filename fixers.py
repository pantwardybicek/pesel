
from .validate import validate_int_len, validate_missing_sequence
from .back import DIGIT_WEIGHTS


def fix_int(pes) -> str:
    validate_int_len(pes)
    return str(pes).zfill(11)


def calculate_control(numbers) -> int:
    numbers = str(numbers)
    numbers = [n for n in numbers if n.isdigit()]
    if len(numbers) != 10:
        raise ValueError('Could not calculate the controll number. 10 digits required')
    s = sum(int(a) * b for a, b in zip(numbers, DIGIT_WEIGHTS[:-1]))
    m = s % 10
    if m == 0:
        c = 0
    else:
        c = 10 - m
    return c


def detect_symbol(pes):
    for x in pes:
        if not x.isdigit():
            return x
    raise ValueError('No symbol sign detected in pesel sequence')


def fix_missing_number(pes) -> str:
    validate_missing_sequence(pes)
    symbol = detect_symbol(pes)
    s = 0
    for n, w in zip(pes, DIGIT_WEIGHTS):
        if n == symbol:
            missing_w = w
        else:
            n = int(n)
            s += (n * w) % 10

    mod_s = 10 - (s % 10)
    if mod_s == 10:
        mod_s = 0

    for x in range(10):
        if (x * missing_w) % 10 == mod_s:
            break
    else:
        raise RuntimeError('No missing value result detected.')
    return ''.join([n for n in pes]).replace(symbol, str(x))


def mask_irrelevant(pes, gender, token='x'):
    return ''.join((pes[0:6], str(token) * 3, gender, str(token)))
