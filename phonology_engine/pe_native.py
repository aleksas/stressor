# -*- coding: utf-8 -*-
from ctypes import *
from platform import uname, architecture
from os.path import join, dirname
from struct import unpack

_supported_os = ['Windows', 'Linux']
_supported_architecture = ['64bit', '32bit']

_os = uname()[0]
_architecture = architecture()[0]

if _os not in _supported_os or _architecture not in _supported_architecture:
    msgs = []
    if _os not in _supported_os:
        msgs.append('%s OS not supported. Must be one of: %s. ' % (_os, str(_supported_os)))
    if _architecture not in _supported_architecture:
        msgs.append('%s CPU architecture not supported. Must be one of: %s.' % (_os, str(_supported_architecture)))
    
    raise Exception(' '.join(msgs))

folder = ''
prefix = ''
if _os == "Windows":
    if _architecture == '64bit':
        folder = 'Win64_x64'
    if _architecture == '32bit':
        folder = 'Win32_x86'
    lib_ext = ".dll"
elif _os == "Linux":
    if _architecture == '64bit':
        folder = 'Linux_x86_64'
    if _architecture == '32bit':
        folder = 'Linux_x86'
    lib_ext = ".so"
    prefix = 'lib'

_native_encoding = 'windows-1257'

_lib_path = join(dirname(__file__), folder, prefix + "PhonologyEngine" + lib_ext)
_PhonologyEngineLibrary = CDLL(_lib_path)

_PhonologyEngineInit = _PhonologyEngineLibrary.PhonologyEngineInit

_PhonologyEngineNozmalizeText = _PhonologyEngineLibrary.PhonologyEngineNormalizeText#(char * szText, NormalizedTextHandle * pHandle);
_PhonologyEngineNozmalizeText.argtypes = [c_char_p, POINTER(c_void_p)]

_PhonologyEngineNormalizedTextFree = _PhonologyEngineLibrary.PhonologyEngineNormalizedTextFree#(NormalizedTextHandle * pHandle);
_PhonologyEngineNormalizedTextFree.argtypes = [POINTER(c_void_p)]

_PhonologyEngineNormalizedTextGetPhraseCount = _PhonologyEngineLibrary.PhonologyEngineNormalizedTextGetPhraseCount#(NormalizedTextHandle handle, int * pValue);
_PhonologyEngineNormalizedTextGetPhraseCount.argtypes = [c_void_p, POINTER(c_int)]

_PhonologyEngineNormalizedTextGetPhrase = _PhonologyEngineLibrary.PhonologyEngineNormalizedTextGetPhrase#(NormalizedTextHandle handle, int index, char ** pSzValue);
_PhonologyEngineNormalizedTextGetPhrase.argtypes = [c_void_p, c_int, POINTER(c_char_p)]

_PhonologyEngineNormalizedTextGetPhraseLetterMap = _PhonologyEngineLibrary.PhonologyEngineNormalizedTextGetPhraseLetterMap#(NormalizedTextHandle handle, int index, int ** pArValue, int * pCount)
_PhonologyEngineNormalizedTextGetPhraseLetterMap.argtypes = [c_void_p, c_int, POINTER(POINTER(c_int)), POINTER(c_int)]

_PhonologyEngineProcessPhrase = _PhonologyEngineLibrary.PhonologyEngineProcessPhrase#(char * szNormalizedText, PhonologyEngineOutputHandle * pHandle);
_PhonologyEngineProcessPhrase.argtypes = [c_char_p, POINTER(c_void_p)]

_PhonologyEngineOutputFree = _PhonologyEngineLibrary.PhonologyEngineOutputFree#(PhonologyEngineOutputHandle * pHandle);
_PhonologyEngineOutputFree.argtypes = [POINTER(c_void_p)]

_PhonologyEngineOutputGetWordCount = _PhonologyEngineLibrary.PhonologyEngineOutputGetWordCount#(PhonologyEngineOutputHandle hOutput, int * pValue);
_PhonologyEngineOutputGetWordCount.argtypes = [c_void_p, POINTER(c_int)]

_PhonologyEngineOutputGetWord = _PhonologyEngineLibrary.PhonologyEngineOutputGetWord#(PhonologyEngineOutputHandle hOutput, int wordIndex, char ** pszValue);
_PhonologyEngineOutputGetWord.argtypes = [c_void_p, c_int, POINTER(c_char_p)]

_PhonologyEngineOutputGetWordSyllables = _PhonologyEngineLibrary.PhonologyEngineOutputGetWordSyllables#(PhonologyEngineOutputHandle hOutput, int wordIndex, char ** pszValue);
_PhonologyEngineOutputGetWordSyllables.argtypes = [c_void_p, c_int, POINTER(c_char_p)]

_PhonologyEngineOutputGetWordStressOptionCount = _PhonologyEngineLibrary.PhonologyEngineOutputGetWordStressOptionCount#(PhonologyEngineOutputHandle hOutput, int wordIndex, int * pValue);
_PhonologyEngineOutputGetWordStressOptionCount.argtypes = [c_void_p, c_int, POINTER(c_int)]

_PhonologyEngineOutputGetWordStressOptionSelected = _PhonologyEngineLibrary.PhonologyEngineOutputGetWordStressOptionSelected#(PhonologyEngineOutputHandle hOutput, int wordIndex, int * pValue);
_PhonologyEngineOutputGetWordStressOptionSelected.argtypes = [c_void_p, c_int, POINTER(c_int)]

_PhonologyEngineOutputGetWordStressOption = _PhonologyEngineLibrary.PhonologyEngineOutputGetWordStressOption#(PhonologyEngineOutputHandle hOutput, int wordIndex, int optionIndex, int * pLetterIndex, int * pStressType, int * pVocabulary, int * pGrammarRule)
_PhonologyEngineOutputGetWordStressOption.argtypes = [c_void_p, c_int, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int)]

def _check(res):
    if res != 0:
        raise Exception("_PhonologyEngineInit failed: %d" % res)

_check( _PhonologyEngineInit() )

def phonology_engine_normalize_text(text):
    handle = c_void_p()
    cs = c_char_p(text.encode(_native_encoding))

    _check( _PhonologyEngineNozmalizeText( cs, byref(handle) ) )

    return handle

def phonology_engine_normalized_text_free(handle):
    _check( _PhonologyEngineNormalizedTextFree( byref(handle) ) )

def phonology_engine_normalized_text_get_phrase_count(handle):
    value = c_int(0)

    _check( _PhonologyEngineNormalizedTextGetPhraseCount( handle, byref(value) ) )

    return value.value

def phonology_engine_normalized_text_get_phrase(handle, index):
    cs = c_char_p()

    _check( _PhonologyEngineNormalizedTextGetPhrase( handle, c_int(index), byref(cs) ) )

    if not cs.value:
        return ''
    return cs.value.decode(_native_encoding)

def phonology_engine_normalized_text_get_phrase_letter_map(handle, index):
    ci = POINTER(c_int)()
    c = c_int(0)

    _check( _PhonologyEngineNormalizedTextGetPhraseLetterMap( handle, c_int(index), byref(ci), byref(c) ) )

    return [ci[i] for i in range(c.value)]

def phonology_engine_process_phrase(text):

    handle = c_void_p()
    cs = c_char_p(text.encode(_native_encoding))

    _check( _PhonologyEngineProcessPhrase( cs, byref(handle) ) )

    return handle

def phonology_engine_output_free(handle):
    _check( _PhonologyEngineOutputFree( byref(handle) ) )

def phonology_engine_output_get_word_count(handle):
    value = c_int(0)
    _check( _PhonologyEngineOutputGetWordCount(handle, byref(value)))
    return value.value

def phonology_engine_output_get_word(handle, word_index):
    cs = c_char_p()
    _check( _PhonologyEngineOutputGetWord(handle, c_int(word_index), byref(cs)) )    
    return cs.value.decode(_native_encoding)

def phonology_engine_output_get_word_syllables(handle, word_index):
    cs = c_char_p()

    _check( _PhonologyEngineOutputGetWordSyllables(handle, c_int(word_index), byref(cs)) ) 

    values = []
    if cs.value:
        values = [unpack("<b", v)[0] if not isinstance(v, int) else v for v in cs.value.split(b'\n')[0]]

    indeces = []
    
    if len(values) > 1 and values[-1] == 2:
        values = values[0:-1]

    for i, v in enumerate(values):
        if v == 2:
            indeces.append(i)

    return indeces

def _get_case_name(case):
    if case >= 7:
        case -= 7

    if case == 0:
        return u'Vardininkas'#, 'Nominativus'
    elif case == 1:
        return u'Kilmininkas'#, 'Genitivus'
    elif case == 2:
        return u'Naudininkas'#, 'Dativus'
    elif case == 3:
        return u'Galininkas'#, 'Accusativus'
    elif case == 4:
        return u'Įnagininkas'#, 'Instrumentalis'
    elif case == 5:
        return u'Vietininkas'#, 'Locativus'
    elif case == 6:
        return u'Šauksmininkas'#, 'Vocativus'
    else:
        return 'UNKNOWN'

def phonology_engine_output_decode_option(option):
    stressed_letter_index, stress_type, vocabulary, value = option

    if not isinstance(value, int):
        raise Exception("Invalide value type, must be int")

    result = {}
    if vocabulary == 0:
        result['rule'] = u'Veiksmazodžių kamienas ir galune (taisytina)'
    if vocabulary == 1:
        result['rule'] = u'Nekaitomas žodis'
    if vocabulary == 2:
        result['rule'] = u'Linksnis ir kamieno tipas'

        stem_type = value >> 8
        case = value - (stem_type << 8)

        if case >= 0 and case <= 6:
            result['number'] = 'vienaskaita'
        elif case >= 0 and case <= 12:
            result['number'] = 'daugiskaita'

        result['stem_type'] = stem_type
        result['grammatical_case'] = _get_case_name(case)
        result['stressed_letter_index'] = stressed_letter_index
        result['stress_type'] = stress_type
        
    return result

def phonology_engine_output_get_word_stress_options(handle, word_index):
    count, selected_index = c_int(0), c_int(0)

    _check( _PhonologyEngineOutputGetWordStressOptionCount(handle, c_int(word_index), byref(count)) ) 
    _check( _PhonologyEngineOutputGetWordStressOptionSelected(handle, c_int(word_index), byref(selected_index)) ) 

    count = count.value

    selected_index = selected_index.value if count > 0 else None

    options = {'selected_index': selected_index, 'options': [], 'decoded_options': []}

    for i in range(count):
        letter_index, stress_type, vocabulary, grammar_rule = c_int(0), c_int(0), c_int(0), c_int(0)
        
        _check( _PhonologyEngineOutputGetWordStressOption(handle, c_int(word_index), i, byref(letter_index), byref(stress_type), byref(vocabulary) , byref(grammar_rule)) )

        letter_index, stress_type, vocabulary, grammar_rule = letter_index.value, stress_type.value, vocabulary.value, grammar_rule.value

        option = (letter_index, stress_type, vocabulary, grammar_rule)
        options['options'].append(option)

        decoded_option = phonology_engine_output_decode_option(option)
        options['decoded_options'].append(decoded_option)

    return options