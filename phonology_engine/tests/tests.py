from nose.tools import assert_equal
from phonology_engine import PhonologyEngine

from pprint import pprint

def test_laba_diena():
    pe = PhonologyEngine()
    pe.process('Laba diena')