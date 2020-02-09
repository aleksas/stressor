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
    assert_equal(res, u'LABA DIENA KAIP LAIKAIS')

def test_process_and_collapse_word_1():
    pe = PhonologyEngine()
    res = pe.process_and_collapse(u'Ištikima savo dvasiniam ir doroviniam paveldui Sąjunga remiasi nedalomomis ir visuotinėmis vertybėmis: laba diena. Kur buvai?', 'word')
    assert_equal(res, u'IŠTIKIMA SAVO DVASINIAM IR DOROVINIAM PAVELDUI SĄJUNGA REMIASI NEDALOMOMIS IR VISUOTINĖMIS VERTYBĖMIS LABA DIENA KUR BUVAI')

def test_process_and_collapse_word_with_syllables_1():
    pe = PhonologyEngine()
    res = pe.process_and_collapse(u'Ištikima savo dvasiniam ir doroviniam paveldui Sąjunga remiasi nedalomomis ir visuotinėmis vertybėmis: laba diena. Kur buvai?', 'word_with_syllables')
    assert_equal(res, u'I-ŠTI-KI-MA SA-VO DVA-SI-NIAM IR DO-RO-VI-NIAM PA-VEL-DUI SĄ-JUN-GA RE-MIA-SI NEDALOMOMIS IR VI-SUO-TI-NĖ-MIS VER-TY-BĖ-MIS LA-BA DIE-NA KUR BU-VAI')

def test_process_and_collapse_word_with_all_numeric_stresses_1():
    pe = PhonologyEngine()
    res = pe.process_and_collapse(u'Ištikima savo dvasiniam ir doroviniam paveldui Sąjunga remiasi nedalomomis ir visuotinėmis vertybėmis: Laba diena. Kur buvai?', 'word_with_all_numeric_stresses')
    assert_equal(res, u'I0ŠTIKIMA SA0VO DVA2SINIAM IR DORO1VINIAM PA2VELDUI SĄ1JUNGA RE2MIASI NEDALOMOMIS IR VISU1OTINĖMIS VERTY1BĖMIS LA2BA0 DIENA0 KUR2 BUVAI2')

def test_process_and_collapse_word_with_only_multiple_numeric_stresses_1():
    pe = PhonologyEngine()
    res = pe.process_and_collapse(u'Ištikima savo dvasiniam ir doroviniam paveldui Sąjunga remiasi nedalomomis ir visuotinėmis vertybėmis: Laba diena. Kur buvai?', 'word_with_only_multiple_numeric_stresses')
    assert_equal(res, u'IŠTIKIMA SAVO DVASINIAM IR DOROVINIAM PAVELDUI SĄJUNGA REMIASI NEDALOMOMIS IR VISUOTINĖMIS VERTYBĖMIS LA2BA0 DIENA KUR BUVAI')

def test_process_and_collapse_number_stressed_word_1():
    pe = PhonologyEngine()
    res = pe.process_and_collapse(u'Ištikima savo dvasiniam ir doroviniam paveldui Sąjunga remiasi nedalomomis ir visuotinėmis vertybėmis: laba diena. Kur buvai?', 'number_stressed_word')
    assert_equal(res, u'I0ŠTIKIMA SA0VO DVA2SINIAM IR DORO1VINIAM PA2VELDUI SĄ1JUNGA RE2MIASI NEDALOMOMIS IR VISU1OTINĖMIS VERTY1BĖMIS LA2BA DIENA0 KUR2 BUVAI2')

def test_process_and_collapse_utf8_stressed_word_1():
    pe = PhonologyEngine()
    res = pe.process_and_collapse(u'Ištikima savo dvasiniam ir doroviniam paveldui Sąjunga remiasi nedalomomis ir visuotinėmis vertybėmis: laba diena. Kur buvai?', 'utf8_stressed_word')
    assert_equal(res, u'ÌŠTIKIMA SÀVO DVÃSINIAM IR DORÓVINIAM PÃVELDUI SĄ́JUNGA RẼMIASI NEDALOMOMIS IR VISÚOTINĖMIS VERTÝBĖMIS LÃBA DIENÀ KUR̃ BUVAĨ')

def test_process_and_collapse_ascii_stressed_word_1():
    pe = PhonologyEngine()
    res = pe.process_and_collapse(u'Ištikima savo dvasiniam ir doroviniam paveldui Sąjunga remiasi nedalomomis ir visuotinėmis vertybėmis: laba diena. Kur buvai?', 'ascii_stressed_word')
    assert_equal(res, u'I`ŠTIKIMA SA`VO DVA~SINIAM IR DORO^VINIAM PA~VELDUI SĄ^JUNGA RE~MIASI NEDALOMOMIS IR VISU^OTINĖMIS VERTY^BĖMIS LA~BA DIENA` KUR~ BUVAI~')

def test_normalize_text_1():
    pe = PhonologyEngine()
    pe.normalize(u'1 žmogus. Ištikima savo dvasiniam ir doroviniam paveldui Sąjunga remiasi nedalomomis ir visuotinėmis vertybėmis: laba diena. Kur buvai?')

def test_normalize_and_collapse_text_1():
    pe = PhonologyEngine()
    res = pe.normalize_and_collapse(u'1 žmogus. Ištikima savo dvasiniam ir doroviniam paveldui Sąjunga remiasi nedalomomis ir visuotinėmis vertybėmis: laba diena. Kur buvai?')
    assert_equal(res, u'VIENAS ŽMOGUS  IŠTIKIMA SAVO DVASINIAM IR DOROVINIAM PAVELDUI SĄJUNGA REMIASI NEDALOMOMIS IR VISUOTINĖMIS VERTYBĖMIS  LABA DIENA  KUR BUVAI')

def test_normalize_and_collapse_text_2():
    pe = PhonologyEngine()
    res = pe.process_and_collapse(u'31 kačiukas perbėgo kelią.', 'ascii_stressed_word')
    assert_equal(res, u'TRI`SDEŠIMT VI^ENAS KAČIU`KAS PE^RBĖGO KE~LIĄ')

def test_normalize_and_collapse_text_3():
    pe = PhonologyEngine()
    res = pe.process_and_collapse(u'Kainuos šie telefonai „vos“ nuo 1400 eurų.', 'ascii_stressed_word')
    assert_equal(res, u'KAINUO~S ŠIE~ TELEFO`NAI VO~S NUO TŪ^KSTANTIS KETURI` ŠIMTAI~ EU~RŲ')

def test_normalize_and_collapse_text_4():
    pe = PhonologyEngine()
    res = pe.process_and_collapse(u'„vos“', 'ascii_stressed_word')
    assert_equal(res, u'VO~S')

def test_normalize_and_collapse_text_5():
    pe = PhonologyEngine()
    res = pe.process_and_collapse(u'„123“', 'ascii_stressed_word')
    assert_equal(res, u'ŠIM~TAS DVI`DEŠIMT TRY~S')

def test_normalize_and_collapse_text_6():
    pe = PhonologyEngine()
    res = pe.process_and_collapse(u'O pirmasis pasaulyje telefonas perlenkiamu ekranu - „Royole FlexPai“ - yra ne prototipinėje fazėje.', 'ascii_stressed_word')
    assert_equal(res, u'O PIRMA`SIS PASA^ULYJE TELEFO`NAS PE^RLENKIAMU EKRANU` ROYOLE FLEKSPAI YRA` NE PROTOTIPINĖJE FA~ZĖJE')

def test_normalize_and_collapse_text_3():
    pe = PhonologyEngine()
    res = pe.process_and_collapse(u'Kainuos šie telefonai „vos“ nuo 1400 eurų.', 'ascii_stressed_word')
    assert_equal(res, u'KAINUO~S ŠIE~ TELEFO`NAI VO~S NUO TŪ^KSTANTIS KETURI` ŠIMTAI~ EU~RŲ')

def test_normalize_and_collapse_text_4():
    pe = PhonologyEngine()
    res = pe.process_and_collapse(u'„vos“', 'ascii_stressed_word')
    assert_equal(res, u'VO~S')

def test_normalize_and_collapse_text_5():
    pe = PhonologyEngine()
    res = pe.process_and_collapse(u'„123“', 'ascii_stressed_word')
    assert_equal(res, u'ŠIM~TAS DVI`DEŠIMT TRY~S')

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

def test_word_span_consistency():
    pe = PhonologyEngine()
    t = u'Pradėkime nuo tų pirmųjų. Kinijos bendrovės „Royole“ pavadinimas Lietuvoje yra mažai kam girdėtas - ši įmonės negamina mūsų šalyje populiarių išmaniųjų telefonų. Na, ir telefonai atskirai nėra šio gamintojo arkliukas - jo specializacija yra lankstūs ekranai. Tuos ekranus galite klijuoti kur norite - ant rankinių, ant kepuraičių, ant marškinėlių. Jie ne ką storesni už popieriaus lapą.'
    liepa_processed_data = pe.process(t)
    for word_details, a, b, letter_map in liepa_processed_data:
        for word_detail in word_details:    
            span = word_detail['word_span']
            normalized = (len ( set( letter_map[span[0]:span[1]] ) ) == 1) and (span[1] - span[0] > 1)
            source_span = letter_map[span[0]], letter_map[span[1] - 1] + 1
            word = word_detail['ascii_stressed_word']
            orig_word = t[source_span[0]:source_span[1]]

            if not set(orig_word).intersection(set('^`~')):
                continue
            
            _ = t[max(0, source_span[0] - 2):min(len(t), source_span[1] + 2)]

            assert_equal(orig_word.lower(), word.replace('`', '').replace('^', '').replace('~', '').lower())

def test_sentence_split():
    pe = PhonologyEngine()
    t = u'Bezdonių'
    liepa_processed_data = pe.process(t)
    for word_details, _, _, _ in liepa_processed_data:
        for _ in word_details:
            pass