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
            letter_map = self.get_phrase_letter_map(self.current)

            if self.remove_stress_chars:
                for c in _stress_ascii_chars:
                    value = value.replace(c, '')

            if self.remove_syllable_chars:
                for c in _syllable_chars:
                    value = value.replace(c, '')

            self.current += 1
            return value, letter_map
    
    def get_phrase_count(self):
        return pe_native.phonology_engine_normalized_text_get_phrase_count(self.handle)
    
    def get_phrase(self, index):
        return pe_native.phonology_engine_normalized_text_get_phrase(self.handle, index)
    
    def get_phrase_letter_map(self, index):
        return pe_native.phonology_engine_normalized_text_get_phrase_letter_map(self.handle, index)

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

    def get_word_with_stress_and_syllables(self, word_index, stress_map, stress_option_index=None, only_multiple=False):
        stress_options = self.get_word_stress_options(word_index)['options']
        if stress_option_index != None:
            stress_options = [stress_options[stress_option_index]]        

        res = []
        
        word = self.get_word(word_index, include_syllables=False)
        syllable_indeces = self.get_word_syllables(word_index)

        if not syllable_indeces:
            syllable_indeces = [0]
        syllable_indeces.append(len(word))
        stress_count = 0

        for i in range(len(word)):
            letter = word[i]
            stresses = set([])
            for oi in range(len(stress_options)):
                stress_option = stress_options[oi]

                if stress_option and i == stress_option[0]:
                    stresses.add(stress_map[stress_option[1]])

            stress_count += len(stresses)
            res.append(letter + ''.join(stresses))
        
        if only_multiple and stress_count <= 1:
            res = word

        syllables = []
        for i,j in zip(syllable_indeces[:-1], syllable_indeces[1:]):
            syllables.append(''.join(res[i:j]))
        
        return syllables

    def get_word_with_stress(self, word_index, stress_map, stress_option_index=None, include_syllables=True):
        if not stress_option_index:
            stress_option_index = self.get_word_stress_options(word_index)['selected_index']

        res = self.get_word_with_stress_and_syllables(word_index, stress_map, stress_option_index)

        glue = '-' if include_syllables else ''

        return glue.join(res)

    def get_word_with_all_numeric_stresses(self, word_index, include_syllables=True):
        stress_map = {
            0: '0',
            1: '1',
            2: '2'
        }
        
        res = self.get_word_with_stress_and_syllables(word_index, stress_map, None)

        glue = '-' if include_syllables else ''

        return glue.join(res)

    def get_word_with_only_multiple_numeric_stresses(self, word_index, include_syllables=True):
        stress_map = {
            0: '0',
            1: '1',
            2: '2'
        }
        
        res = self.get_word_with_stress_and_syllables(word_index, stress_map, None, True)

        glue = '-' if include_syllables else ''

        return glue.join(res)
    
    def get_word_with_numeric_stress(self, word_index, stress_option_index=None, include_syllables=True):
        stress_map = {
            0: '0',
            1: '1',
            2: '2'
            }

        return self.get_word_with_stress(word_index, stress_map, stress_option_index, include_syllables)

    def get_word_with_utf8_stress(self, word_index, stress_option_index=None, include_syllables=True):
        stress_map = {
            0: u'\u0300', # grave
            1: u'\u0301', # acute
            2: u'\u0303'  # tilde
            }

        return self.get_word_with_stress(word_index, stress_map, stress_option_index, include_syllables)

    def get_word_with_ascii_stress(self, word_index, stress_option_index=None, include_syllables=True):
        stress_map = {
            0: "`", # grave
            1: "^", # acute - no printable acute accent in ascii table only in extended ASCII:239
            2: "~"  # tilde
            }

        return self.get_word_with_stress(word_index, stress_map, stress_option_index, include_syllables)

