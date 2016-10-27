# Set up the environment and required imports
import math
from dateutil.parser import parse
from string import punctuation


# JSON has no "NaN", so we need to strip them. The problem? They show up in lists of strings....
# Thanks, SO: http://stackoverflow.com/questions/944700/how-to-check-for-nan-in-python
# Check for NaN
def is_nan(x):
    return isinstance(x, float) and math.isnan(x)


# Parse date
def dateParse(date):
    return parse(date).date()


# Strip the punctuation out of strings
def strip_punctuation(s):
    return ''.join(str(c) for c in str(s) if str(c) not in punctuation)


# Create a concatenated list of codes for a specific date
def build_string(data):
    string = ''
    for code in data.code.values:
        string = string + ' ' + code

    string = strip_punctuation(string)
    string = ' '.join(sorted(string.split()))
    return string

