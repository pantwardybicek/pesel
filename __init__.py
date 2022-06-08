from .cls import PESEL, mask_pesel
from .fixers import calculate_control, fix_missing_number

__version__ = 1.0
__author__ = 'pantwardybicek@gmail.com'

__doc__ = """
pesel module contains:
class:
    PESEL (validates the PESEL number and retrieves date of birth and gender from the number)
functions:
    control (calculates missing control number for a 10 digit string representing first 10 digits of a PESEL number)
    fix (fixes tha PESEL number, passed as a string, if the missing digit is replaced with any non digot ASCII symbol)
    mask (validates and masks a pesel number)
    
    
Example of worklfow:
from pesel import PESEL, mask, fix, control

>>> p = 23450500711
>>> pes = PESEL(p)
>>> pes
PESEL:23450500711

>>> pes.pesel
23450500711

>>> pes.dob
datetime.date(2123, 5, 5)

>>> pes.gender
'M'

>>> pes.mask()
'234505xxxMx'

>>> mask(p)
'234505xxxMx'

>>> fix(23450500s11)
'23450500711'

>>> control(2345050071)
1

"""

fix = fix_missing_number
control = calculate_control
mask = mask_pesel
