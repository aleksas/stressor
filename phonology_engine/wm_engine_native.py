from ctypes import *
from platform import uname, architecture
from os.path import join, dirname

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
_PhonologyEngneLibrary = CDLL(_lib_path)

_PhonologyEngneInit = _PhonologyEngneLibrary.PhonologyEngneInit

_PhonologyEngneProcessPhrase = _PhonologyEngneLibrary.PhonologyEngneProcessPhrase
_PhonologyEngneProcessPhrase.argtypes = [c_char_p, c_bool, POINTER(c_void_p)]

_PhonologyEngneOutputFree = _PhonologyEngneLibrary.PhonologyEngneOutputFree#(PhonologyEngneOutputHandle * pHandle);
_PhonologyEngneOutputFree.argtypes = [POINTER(c_void_p)]

_PhonologyEngneOutputGetWordCount = _PhonologyEngneLibrary.PhonologyEngneOutputGetWordCount#(PhonologyEngneOutputHandle hOutput, int * pValue);
_PhonologyEngneOutputGetWordCount.argtypes = [c_void_p, POINTER(c_int)]

_PhonologyEngneOutputGetWord = _PhonologyEngneLibrary.PhonologyEngneOutputGetWord#(PhonologyEngneOutputHandle hOutput, int wordIndex, char ** pszValue);
_PhonologyEngneOutputGetWord.argtypes = [c_void_p, c_int, POINTER(c_char_p)]

_PhonologyEngneOutputGetWordSyllables = _PhonologyEngneLibrary.PhonologyEngneOutputGetWordSyllables#(PhonologyEngneOutputHandle hOutput, int wordIndex, char ** pszValue);
_PhonologyEngneOutputGetWordSyllables.argtypes = [c_void_p, c_int, POINTER(c_char_p)]

_PhonologyEngneOutputGetWordStressOptionCount = _PhonologyEngneLibrary.PhonologyEngneOutputGetWordStressOptionCount#(PhonologyEngneOutputHandle hOutput, int wordIndex, int * pValue);
_PhonologyEngneOutputGetWordStressOptionCount.argtypes = [c_void_p, c_int, POINTER(c_int)]

_PhonologyEngneOutputGetWordStressOptionSelected = _PhonologyEngneLibrary.PhonologyEngneOutputGetWordStressOptionSelected#(PhonologyEngneOutputHandle hOutput, int wordIndex, int * pValue);
_PhonologyEngneOutputGetWordStressOptionSelected.argtypes = [c_void_p, c_int, POINTER(c_int)]

_PhonologyEngneOutputGetWordStressOption = _PhonologyEngneLibrary.PhonologyEngneOutputGetWordStressOption#(PhonologyEngneOutputHandle hOutput, int wordIndex, int optionIndex, int * pLetterIndex, int * pStressType, int * pGrammarRule)
_PhonologyEngneOutputGetWordStressOption.argtypes = [c_void_p, c_int, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int)]

def _check(res):
    if res != 0:
        raise Exception("_PhonologyEngneInit failed: %d" % res)

_check( _PhonologyEngneInit() )

def synthesizeWholeTextAlt(text, normalize=True):
    semi_normalized_text = text.upper()

    handle = c_void_p()
    cs = c_char_p(semi_normalized_text.encode(_native_encoding))

    _check( _PhonologyEngneProcessPhrase( cs, normalize, byref(handle) ) )

    return handle

def PhonologyEngneOutputFree(handle):
    _PhonologyEngneOutputFree( byref(handle) )

def PhonologyEngneOutputGetWordCount(handle):
    value = c_int(0)
    _check( _PhonologyEngneOutputGetWordCount(handle, byref(value)))
    return value

def PhonologyEngneOutputGetWord(handle, word_index):
    cs = c_char_p()
    _check( _PhonologyEngneOutputGetWord(handle, c_int(word_index), byref(cs)) )    
    return cs.value.decode(_native_encoding)

def PhonologyEngneOutputGetWordSyllables(handle, word_index):
    cs = c_char_p()

    _check( _PhonologyEngneOutputGetWordSyllables(handle, c_int(word_index), byref(cs)) ) 
    
    values = [int(v) for v in cs.value.split(b'\n')[0]]
    
    if values[-1] == 2 and len(values) > 1:
        values = values[0:-1]

    indeces = []
    for i, v in enumerate(values):
        if v == 2:
            indeces.append(i)

    return indeces

def PhonologyEngneOutputGetWordStressOptions(handle, word_index):
    count, selected = c_int(0), c_int(0)

    _check( _PhonologyEngneOutputGetWordStressOptionCount(handle, c_int(word_index), byref(count)) ) 
    _check( _PhonologyEngneOutputGetWordStressOptionSelected(handle, c_int(word_index), byref(selected)) ) 

    count, selected = count.value, selected.value

    options = {'count': count, 'selected': selected, 'stresses': []}

    for i in range(count):
        letter_index, stress_type, grammar_rule = c_int(0), c_int(0), c_int(0)
        
        _check( _PhonologyEngneOutputGetWordStressOption(handle, c_int(word_index), i, byref(letter_index), byref(stress_type), byref(grammar_rule) ) )

        letter_index, stress_type, grammar_rule = letter_index.value, stress_type.value, grammar_rule.value

        options['stresses'].append((letter_index, stress_type, grammar_rule))

    return options
