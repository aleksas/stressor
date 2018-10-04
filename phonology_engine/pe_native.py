from ctypes import *
from platform import uname, architecture
from os.path import join, dirname
from struct import unpack

folder = ''
prefix = ''
if uname()[0] == "Windows":
    if architecture()[0] == '64bit':
        folder = 'Win64_x64'
    if architecture()[0] == '32bit':
        folder = 'Win32_x86'
    lib_ext = ".dll"
elif uname()[0] == "Linux":
    if architecture()[0] == '64bit':
        folder = 'Linux_x86_64'
    if architecture()[0] == '32bit':
        folder = 'Linux_x86'
    lib_ext = ".so"
    prefix = 'lib'
else:
    raise Exception("Native lib not present for platform %s" % uname()[0])

_native_encoding = 'windows-1257'

_lib_path = join(dirname(__file__), folder, prefix + "PhonologyEngine" + lib_ext)
_PhonologyEngineLibrary = CDLL(_lib_path)

_PhonologyEngineInit = _PhonologyEngineLibrary.PhonologyEngineInit

_PhonologyEngineProcessPhrase = _PhonologyEngineLibrary.PhonologyEngineProcessPhrase
_PhonologyEngineProcessPhrase.argtypes = [c_char_p, c_bool, POINTER(c_void_p)]

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

_PhonologyEngineOutputGetWordStressOption = _PhonologyEngineLibrary.PhonologyEngineOutputGetWordStressOption#(PhonologyEngineOutputHandle hOutput, int wordIndex, int optionIndex, int * pLetterIndex, int * pStressType, int * pGrammarRule)
_PhonologyEngineOutputGetWordStressOption.argtypes = [c_void_p, c_int, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int)]

def _check(res):
    if res != 0:
        raise Exception("_PhonologyEngineInit failed: %d" % res)

_check( _PhonologyEngineInit() )

def phonology_engine_process_phrase(text, normalize=True):
    semi_normalized_text = text.upper()

    handle = c_void_p()
    cs = c_char_p(semi_normalized_text.encode(_native_encoding))

    _check( _PhonologyEngineProcessPhrase( cs, normalize, byref(handle) ) )

    return handle

def phonology_engine_output_free(handle):
    _PhonologyEngineOutputFree( byref(handle) )

def phonology_engine_output_get_word_count(handle):
    value = c_int(0)
    _check( _PhonologyEngineOutputGetWordCount(handle, byref(value)))
    return value

def phonology_engine_output_get_word(handle, word_index):
    cs = c_char_p()
    _check( _PhonologyEngineOutputGetWord(handle, c_int(word_index), byref(cs)) )    
    return cs.value.decode(_native_encoding)

def phonology_engine_output_get_word_syllables(handle, word_index):
    cs = c_char_p()

    _check( _PhonologyEngineOutputGetWordSyllables(handle, c_int(word_index), byref(cs)) ) 

    values = [unpack("<b", v)[0] for v in cs.value.split(b'\n')[0]]
    
    if values[-1] == 2 and len(values) > 1:
        values = values[0:-1]

    indeces = []
    for i, v in enumerate(values):
        if v == 2:
            indeces.append(i)

    return indeces

def phonology_engine_output_get_word_stress_options(handle, word_index):
    count, selected = c_int(0), c_int(0)

    _check( _PhonologyEngineOutputGetWordStressOptionCount(handle, c_int(word_index), byref(count)) ) 
    _check( _PhonologyEngineOutputGetWordStressOptionSelected(handle, c_int(word_index), byref(selected)) ) 

    count, selected = count.value, selected.value

    options = {'count': count, 'selected': selected, 'stresses': []}

    for i in range(count):
        letter_index, stress_type, grammar_rule = c_int(0), c_int(0), c_int(0)
        
        _check( _PhonologyEngineOutputGetWordStressOption(handle, c_int(word_index), i, byref(letter_index), byref(stress_type), byref(grammar_rule) ) )

        letter_index, stress_type, grammar_rule = letter_index.value, stress_type.value, grammar_rule.value

        options['stresses'].append((letter_index, stress_type, grammar_rule))

    return options
