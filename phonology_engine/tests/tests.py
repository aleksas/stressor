# -*- coding: utf-8 -*-
from nose.tools import assert_equal
from phonology_engine import PhonologyEngine

def test_process_1():
    pe = PhonologyEngine()
    pe.process('Laba diena')

def test_process_2():
    pe = PhonologyEngine()
    pe.process('Laba diena, kaip laikais?')

def test_process_and_collapse_1():
    pe = PhonologyEngine()
    pe.process_and_collapse('Laba diena, kaip laikais?')

def test_process_and_collapse_word_1():
    pe = PhonologyEngine()
    pe.process_and_collapse(u'Ištikima savo dvasiniam ir doroviniam paveldui Sąjunga remiasi nedalomomis ir visuotinėmis vertybėmis: labas labas. Kur buvai?', 'word')

def test_process_and_collapse_number_stressed_word_1():
    pe = PhonologyEngine()
    pe.process_and_collapse(u'Ištikima savo dvasiniam ir doroviniam paveldui Sąjunga remiasi nedalomomis ir visuotinėmis vertybėmis: labas labas. Kur buvai?', 'number_stressed_word')

def test_process_and_collapse_utf8_stressed_word_1():
    pe = PhonologyEngine()
    pe.process_and_collapse(u'Ištikima savo dvasiniam ir doroviniam paveldui Sąjunga remiasi nedalomomis ir visuotinėmis vertybėmis: labas labas. Kur buvai?', 'utf8_stressed_word')

def test_process_and_collapse_ascii_stressed_word_1():
    pe = PhonologyEngine()
    pe.process_and_collapse(u'Ištikima savo dvasiniam ir doroviniam paveldui Sąjunga remiasi nedalomomis ir visuotinėmis vertybėmis: labas labas. Kur buvai?', 'ascii_stressed_word')

def test_normalize_text_1():
    pe = PhonologyEngine()
    pe.normalize(u'1 žmogus. Ištikima savo dvasiniam ir doroviniam paveldui Sąjunga remiasi nedalomomis ir visuotinėmis vertybėmis: labas labas. Kur buvai?')

def test_normalize_and_collapse_text_1():
    pe = PhonologyEngine()
    pe.normalize_and_collapse(u'1 žmogus. Ištikima savo dvasiniam ir doroviniam paveldui Sąjunga remiasi nedalomomis ir visuotinėmis vertybėmis: labas labas. Kur buvai?')
