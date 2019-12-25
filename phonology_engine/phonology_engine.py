# -*- coding: utf-8 -*-
from os.path import join, dirname, abspath
from .pe_output import PhonologyEngineOutput, PhonologyEngineNormalizedPhrases
from .pe_native import phonology_engine_process_phrase, phonology_engine_normalize_text

_phrase_separators = '.?!;:\r\n,'
_max_prase_length = 200
_valid_word_formats = ['word', 'word_with_syllables', 'word_with_all_numeric_stresses', 'word_with_only_multiple_numeric_stresses', 'number_stressed_word', 'utf8_stressed_word', 'ascii_stressed_word']

class PhonologyEngine:
    def __init__(self):
        def _collapsor(output, word_format=None):
            if word_format:
                return output[word_format]
            else:
                return output

        self.collapsor = _collapsor
        self.phrase_separators = _phrase_separators

    def _process(self, text, separators, normalize=True, include_syllables=True, normalize_only=False):
        text = text.strip()
        if len(text) == 0:
            return text
            
        if len(separators) == 0:
            if normalize:
                handle = phonology_engine_normalize_text(text)
                with PhonologyEngineNormalizedPhrases(handle) as normalized_phrases:
                    processed_phrases = []

                    if normalize_only:
                        return ('', [' '.join([p for p,_ in normalized_phrases])])
                    else:
                        r = []
                        for phrase, letter_map in normalized_phrases:
                            processed_phrases.append(self._process(text=phrase, separators=separators, normalize=False, include_syllables=include_syllables, normalize_only=normalize_only))
                            r.append((phrase, letter_map))

                        return ('', processed_phrases, r)
                        
            else:
                if len(text) > _max_prase_length:
                    raise Exception('Phrase "%s" length exceeds %d char limit' % (text, _max_prase_length))
                
                handle = phonology_engine_process_phrase(text)
                
                with PhonologyEngineOutput(handle) as output:
                    res = [
                            {
                            'word': output.get_word(i, include_syllables=False),
                            'word_with_syllables': output.get_word(i, include_syllables=True),
                            'number_stressed_word': output.get_word_with_numeric_stress(i, include_syllables=include_syllables),
                            'utf8_stressed_word': output.get_word_with_utf8_stress(i, include_syllables=include_syllables),
                            'ascii_stressed_word': output.get_word_with_ascii_stress(i, include_syllables=include_syllables),
                            'word_with_all_numeric_stresses' :output.get_word_with_all_numeric_stresses(i, include_syllables=include_syllables),
                            'word_with_only_multiple_numeric_stresses' :output.get_word_with_only_multiple_numeric_stresses(i, include_syllables=include_syllables),
                            'syllables': output.get_word_syllables(i),
                            'stress_options': output.get_word_stress_options(i)
                            }

                            for i in range(output.get_word_count())
                        ]
                                        
                    return res

        phrases = text.split(separators[0])
        other_separators = separators[1:]
        if len(phrases) == 1:
            return self._process(text=phrases[0], separators=other_separators, normalize=normalize, include_syllables=include_syllables, normalize_only=normalize_only)
        else:
            processed_phrases = []
            for phrase in phrases:
                processed_phrases.append(self._process(phrase, other_separators, normalize=normalize, include_syllables=include_syllables, normalize_only=normalize_only))
            
            return (separators[0], processed_phrases)

    def get_collapse_formats(self):
        return _valid_word_formats

    def process(self, s, include_syllables=False):
        return self._process(s.upper(), separators=self.phrase_separators, normalize=True, include_syllables=include_syllables, normalize_only=False)

    def process_and_collapse(self, s, word_format='word', normalize=True, include_syllables=False):
        return self.collapse(self._process(s, separators=self.phrase_separators, normalize=normalize, include_syllables=include_syllables, normalize_only=False), word_format)

    def collapse(self, output, word_format='word'):
        if word_format not in _valid_word_formats:
            raise Exception('Invalide word format "%s". Can be one of: %s.' % (word_format, str(_valid_word_formats)))

        if isinstance(output, tuple):
            return ((output[0] + ' ').join([self.collapse(r, word_format) for r in output[1]])).strip()
        elif isinstance(output, list):
            return ' '.join([self.collapse(r, word_format) for r in output])
        elif isinstance(output, dict):
            return self.collapsor(output, word_format)
        elif output == '':
            return ''
        else: ## assume it's string otherwise six package is needed for py2.7/3 compat
            return self.collapsor(output)

    def normalize(self, text):
        return self._process(text, separators=self.phrase_separators, normalize=True, include_syllables=False, normalize_only=True)

    def normalize_and_collapse(self, text):
        return self.collapse(self._process(text, separators=self.phrase_separators, normalize=True, include_syllables=False, normalize_only=True))


