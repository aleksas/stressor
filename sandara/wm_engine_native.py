from ctypes import *
from platform import uname, architecture
from os.path import join, dirname

folder = ''
prefix = ''
if uname()[0] == "Windows":
    if architecture()[0] == '64bit':
        folder = 'Windows_x64'
    if architecture()[0] == '32bit':
        folder = 'Windows_x86'
    lib_ext = ".dll"
if uname()[0] == "Linux":
    if architecture()[0] == '64bit':
        folder = 'Linux_x86_64'
    if architecture()[0] == '32bit':
        folder = 'Linux_x86'
    lib_ext = ".so"
    prefix = 'lib'
else:
    raise Exception("Native lib not present for platform %s" % uname()[0])

_native_encoding = 'windows-1257'

_lib_path = join(dirname(__file__), folder, prefix + "transcrLUSS" + lib_ext)
_libtranscrLUSS = CDLL(_lib_path)

_initTranscrLUSS = _libtranscrLUSS.initTranscrLUSS

_synthesizeWholeTextAlt = _libtranscrLUSS.synthesizeWholeTextAlt
_synthesizeWholeTextAlt.argtypes = [c_char_p, c_bool, POINTER(c_void_p)]

_WMEngineOutputFree = _libtranscrLUSS.WMEngineOutputFree#(WMEngineOutputHandle * pHandle);
_WMEngineOutputFree.argtypes = [POINTER(c_void_p)]

_WMEngineOutputGetWordCount = _libtranscrLUSS.WMEngineOutputGetWordCount#(WMEngineOutputHandle hOutput, int * pValue);
_WMEngineOutputGetWordCount.argtypes = [c_void_p, POINTER(c_int)]

_WMEngineOutputGetWord = _libtranscrLUSS.WMEngineOutputGetWord#(WMEngineOutputHandle hOutput, int wordIndex, char ** pszValue);
_WMEngineOutputGetWord.argtypes = [c_void_p, c_int, POINTER(c_char_p)]

_WMEngineOutputGetWordSyllables = _libtranscrLUSS.WMEngineOutputGetWordSyllables#(WMEngineOutputHandle hOutput, int wordIndex, char ** pszValue);
_WMEngineOutputGetWordSyllables.argtypes = [c_void_p, c_int, POINTER(c_char_p)]

_WMEngineOutputGetWordStressOptionCount = _libtranscrLUSS.WMEngineOutputGetWordStressOptionCount#(WMEngineOutputHandle hOutput, int wordIndex, int * pValue);
_WMEngineOutputGetWordStressOptionCount.argtypes = [c_void_p, c_int, POINTER(c_int)]

_WMEngineOutputGetWordStressOptionSelected = _libtranscrLUSS.WMEngineOutputGetWordStressOptionSelected#(WMEngineOutputHandle hOutput, int wordIndex, int * pValue);
_WMEngineOutputGetWordStressOptionSelected.argtypes = [c_void_p, c_int, POINTER(c_int)]

_WMEngineOutputGetWordStressOption = _libtranscrLUSS.WMEngineOutputGetWordStressOption#(WMEngineOutputHandle hOutput, int wordIndex, int optionIndex, int * pLetterIndex, int * pStressType, int * pGrammarRule)
_WMEngineOutputGetWordStressOption.argtypes = [c_void_p, c_int, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int)]

def _check(res):
    if res != 0:
        raise Exception("_initTranscrLUSS failed: %d" % res)

_check( _initTranscrLUSS() )

def synthesizeWholeTextAlt(text, normalize=True):
    semi_normalized_text = text.upper()

    handle = c_void_p()
    cs = c_char_p(semi_normalized_text.encode(_native_encoding))

    _check( _synthesizeWholeTextAlt( cs, normalize, byref(handle) ) )

    return handle

def WMEngineOutputFree(handle):
    _WMEngineOutputFree( byref(handle) )

def WMEngineOutputGetWordCount(handle):
    value = c_int(0)
    _check( _WMEngineOutputGetWordCount(handle, byref(value)))
    return value

def WMEngineOutputGetWord(handle, word_index):
    cs = c_char_p()
    _check( _WMEngineOutputGetWord(handle, c_int(word_index), byref(cs)) )    
    return cs.value.decode(_native_encoding)

def WMEngineOutputGetWordSyllables(handle, word_index):
    cs = c_char_p()

    _check( _WMEngineOutputGetWordSyllables(handle, c_int(word_index), byref(cs)) ) 
    
    values = [int(v) for v in cs.value.split(b'\n')[0]]
    
    if values[-1] == 2 and len(values) > 1:
        values = values[0:-1]

    indeces = []
    for i, v in enumerate(values):
        if v == 2:
            indeces.append(i)

    return indeces

def WMEngineOutputGetWordStressOptions(handle, word_index):
    count, selected = c_int(0), c_int(0)

    _check( _WMEngineOutputGetWordStressOptionCount(handle, c_int(word_index), byref(count)) ) 
    _check( _WMEngineOutputGetWordStressOptionSelected(handle, c_int(word_index), byref(selected)) ) 

    count, selected = count.value, selected.value

    options = {'count': count, 'selected': selected, 'stresses': []}

    for i in range(count):
        letter_index, stress_type, grammar_rule = c_int(0), c_int(0), c_int(0)
        
        _check( _WMEngineOutputGetWordStressOption(handle, c_int(word_index), i, byref(letter_index), byref(stress_type), byref(grammar_rule) ) )

        letter_index, stress_type, grammar_rule = letter_index.value, stress_type.value, grammar_rule.value

        options['stresses'].append((letter_index, stress_type, grammar_rule))

    return options
