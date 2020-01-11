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
    res = pe.process_and_collapse('Laba diena, kaip laikais?')
    assert_equal(res, u'LABA DIENA, KAIP LAIKAIS?')

def test_process_and_collapse_word_1():
    pe = PhonologyEngine()
    res = pe.process_and_collapse(u'Ištikima savo dvasiniam ir doroviniam paveldui Sąjunga remiasi nedalomomis ir visuotinėmis vertybėmis: laba diena. Kur buvai?', 'word')
    assert_equal(res, u'IŠTIKIMA SAVO DVASINIAM IR DOROVINIAM PAVELDUI SĄJUNGA REMIASI NEDALOMOMIS IR VISUOTINĖMIS VERTYBĖMIS: LABA DIENA. KUR BUVAI?')

def test_process_and_collapse_word_with_syllables_1():
    pe = PhonologyEngine()
    res = pe.process_and_collapse(u'Ištikima savo dvasiniam ir doroviniam paveldui Sąjunga remiasi nedalomomis ir visuotinėmis vertybėmis: laba diena. Kur buvai?', 'word_with_syllables')
    assert_equal(res, u'I-ŠTI-KI-MA SA-VO DVA-SI-NIAM IR DO-RO-VI-NIAM PA-VEL-DUI SĄ-JUN-GA RE-MIA-SI NEDALOMOMIS IR VI-SUO-TI-NĖ-MIS VER-TY-BĖ-MIS: LA-BA DIE-NA. KUR BU-VAI?')

def test_process_and_collapse_word_with_all_numeric_stresses_1():
    pe = PhonologyEngine()
    res = pe.process_and_collapse(u'Ištikima savo dvasiniam ir doroviniam paveldui Sąjunga remiasi nedalomomis ir visuotinėmis vertybėmis: Laba diena. Kur buvai?', 'word_with_all_numeric_stresses')
    assert_equal(res, u'I0ŠTIKIMA SA0VO DVA2SINIAM IR DORO1VINIAM PA2VELDUI SĄ1JUNGA RE2MIASI NEDALOMOMIS IR VISU1OTINĖMIS VERTY1BĖMIS: LA2BA0 DIENA0. KUR2 BUVAI2?')

def test_process_and_collapse_word_with_only_multiple_numeric_stresses_1():
    pe = PhonologyEngine()
    res = pe.process_and_collapse(u'Ištikima savo dvasiniam ir doroviniam paveldui Sąjunga remiasi nedalomomis ir visuotinėmis vertybėmis: Laba diena. Kur buvai?', 'word_with_only_multiple_numeric_stresses')
    assert_equal(res, u'IŠTIKIMA SAVO DVASINIAM IR DOROVINIAM PAVELDUI SĄJUNGA REMIASI NEDALOMOMIS IR VISUOTINĖMIS VERTYBĖMIS: LA2BA0 DIENA. KUR BUVAI?')

def test_process_and_collapse_number_stressed_word_1():
    pe = PhonologyEngine()
    res = pe.process_and_collapse(u'Ištikima savo dvasiniam ir doroviniam paveldui Sąjunga remiasi nedalomomis ir visuotinėmis vertybėmis: laba diena. Kur buvai?', 'number_stressed_word')
    assert_equal(res, u'I0ŠTIKIMA SA0VO DVA2SINIAM IR DORO1VINIAM PA2VELDUI SĄ1JUNGA RE2MIASI NEDALOMOMIS IR VISU1OTINĖMIS VERTY1BĖMIS: LA2BA DIENA0. KUR2 BUVAI2?')

def test_process_and_collapse_utf8_stressed_word_1():
    pe = PhonologyEngine()
    res = pe.process_and_collapse(u'Ištikima savo dvasiniam ir doroviniam paveldui Sąjunga remiasi nedalomomis ir visuotinėmis vertybėmis: laba diena. Kur buvai?', 'utf8_stressed_word')
    assert_equal(res, u'ÌŠTIKIMA SÀVO DVÃSINIAM IR DORÓVINIAM PÃVELDUI SĄ́JUNGA RẼMIASI NEDALOMOMIS IR VISÚOTINĖMIS VERTÝBĖMIS: LÃBA DIENÀ. KUR̃ BUVAĨ?')

def test_process_and_collapse_ascii_stressed_word_1():
    pe = PhonologyEngine()
    res = pe.process_and_collapse(u'Ištikima savo dvasiniam ir doroviniam paveldui Sąjunga remiasi nedalomomis ir visuotinėmis vertybėmis: laba diena. Kur buvai?', 'ascii_stressed_word')
    assert_equal(res, u'I`ŠTIKIMA SA`VO DVA~SINIAM IR DORO^VINIAM PA~VELDUI SĄ^JUNGA RE~MIASI NEDALOMOMIS IR VISU^OTINĖMIS VERTY^BĖMIS: LA~BA DIENA`. KUR~ BUVAI~?')

def test_normalize_text_1():
    pe = PhonologyEngine()
    pe.normalize(u'1 žmogus. Ištikima savo dvasiniam ir doroviniam paveldui Sąjunga remiasi nedalomomis ir visuotinėmis vertybėmis: laba diena. Kur buvai?')

def test_normalize_and_collapse_text_1():
    pe = PhonologyEngine()
    res = pe.normalize_and_collapse(u'1 žmogus. Ištikima savo dvasiniam ir doroviniam paveldui Sąjunga remiasi nedalomomis ir visuotinėmis vertybėmis: laba diena. Kur buvai?')
    assert_equal(res, u'VIENAS ŽMOGUS. IŠTIKIMA SAVO DVASINIAM IR DOROVINIAM PAVELDUI SĄJUNGA REMIASI NEDALOMOMIS IR VISUOTINĖMIS VERTYBĖMIS: LABA DIENA. KUR BUVAI?')

def test_normalize_and_collapse_text_2():
    pe = PhonologyEngine()
    res = pe.process_and_collapse(u'31 kačiukas perbėgo kelią.', 'ascii_stressed_word')
    assert_equal(res, u'TRI`SDEŠIMT VI^ENAS KAČIU`KAS PE^RBĖGO KE~LIĄ.')

def test_normalize_and_collapse_abbr_1():
    pe = PhonologyEngine()
    pe.phrase_separators = ''
    res = pe.normalize_and_collapse(u'proc.')
    assert_equal(res, u'PROCENTAS')

def test_normalize_and_collapse_text_roman_num_1():
    pe = PhonologyEngine()
    pe.phrase_separators = ''
    res = pe.normalize_and_collapse(u'IV.')
    assert_equal(res, u'KETVIRTAS')
