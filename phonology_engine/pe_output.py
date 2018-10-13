from __future__ import with_statement
from . import pe_native

_stress_ascii_chars = '`^~'
_syllable_chars = '-'

class PhonologyEngineNormalizedPhrases:
    def __init__(self, handle, remove_stress_chars=True, remove_syllable_chars=True):
        self.handle = handle

        self.current = 0
        self.max = self.get_phrase_count() - 1

        self.remove_stress_chars = remove_stress_chars
        self.remove_syllable_chars = remove_syllable_chars

    def __del__(self):
        pe_native.phonology_engine_normalized_text_free(self.handle)
        
    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        del self

    def __iter__(self):
        return self

    def __next__(self): # Python 3
        return self.next()

    def next(self):  # Python 2
        if self.current > self.max:
            raise StopIteration
        else:
            value = self.get_phrase(self.current)

            if self.remove_stress_chars:
                for c in _stress_ascii_chars:
                    value = value.replace(c, '')

            if self.remove_syllable_chars:
                for c in _syllable_chars:
                    value = value.replace(c, '')

            self.current += 1
            return value
    
    def get_phrase_count(self):
        return pe_native.phonology_engine_normalized_text_get_phrase_count(self.handle)
    
    def get_phrase(self, index):
        return pe_native.phonology_engine_normalized_text_get_phrase(self.handle, index)

class PhonologyEngineOutput:
    def __init__(self, handle):
        self.handle = handle

    def __del__(self):
        pe_native.phonology_engine_output_free(self.handle)
        
    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        del self

    def get_word_count(self):
        return pe_native.phonology_engine_output_get_word_count(self.handle)

    def get_word(self, index, include_syllables=False):
        if index >= self.get_word_count():
            raise Exception('Value out of bounds')

        word =  pe_native.phonology_engine_output_get_word(self.handle, index)
        syllables = self.get_word_syllables(index)
        
        if include_syllables and syllables:
            res = []
            for i in range(len(word)):
                val = word[i]
                for j in syllables:
                    if j == 0:
                        continue
                    if j == i:
                        val = '-' + val
                res.append(val)
            return ''.join(res)
        else:
            return word


    def get_word_syllables(self, index):
        if index >= self.get_word_count():
            raise Exception('Value out of bounds')

        return pe_native.phonology_engine_output_get_word_syllables(self.handle, index)

    def get_word_stress_options(self, index):
        if index >= self.get_word_count():
            raise Exception('Value out of bounds')

        return pe_native.phonology_engine_output_get_word_stress_options(self.handle, index)

    def get_word_with_numeric_stress(self, word_index, stress_option_index=None, include_syllables=True):
        if not stress_option_index:
            stress_option_index = self.get_word_stress_options(word_index)['selected_index']
        
        stress_options = self.get_word_stress_options(word_index)['options']
        stress_option = None
        if len(stress_options) > 0:
            stress_option = stress_options[stress_option_index]

        syllables = self.get_word_syllables(word_index)
        word = self.get_word(word_index, include_syllables=False)
        res = []

        for i in range(len(word)):
            val = word[i]
            if stress_option and i == stress_option[0]:
                val += str(stress_option[1])

            if include_syllables and syllables:
                for j in syllables:
                    if j == 0:
                        continue
                    if j == i:
                        val = '-' + val
                
            res.append(val)

        
        return ''.join(res)

    def get_word_with_utf8_stress(self, word_index, stress_option_index=None, include_syllables=True):
        cm = {
            '0': u'\u0300', # grave
            '1': u'\u0301', # acute
            '2': u'\u0303'  # tilde
            }

        word = self.get_word_with_numeric_stress(word_index, stress_option_index, include_syllables)
        for k,v in cm.items():
            word = word.replace(k, v)
        
        return word
        
    def get_word_with_ascii_stress(self, word_index, stress_option_index=None, include_syllables=True):
        cm = {
            '0': "`", # grave
            '1': "^", # acute - no printable acute accent in ascii table only in extended ASCII:239
            '2': "~"  # tilde
            }

        word = self.get_word_with_numeric_stress(word_index, stress_option_index, include_syllables)
        for k,v in cm.items():
            word = word.replace(k, v)
        
        return word
