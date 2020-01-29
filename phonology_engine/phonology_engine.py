# -*- coding: utf-8 -*-
from os.path import join, dirname, abspath
from .pe_output import PhonologyEngineOutput, PhonologyEngineNormalizedPhrases
from .pe_output import _syllable_chars, _numeric_stress_map, _utf8_stress_map, _ascii_stress_map
from .pe_native import phonology_engine_process_phrase, phonology_engine_normalize_text
import re

_phrase_separators = u'.?!;:\r\n,'
_truncated_chars = u'„“"\''
_max_prase_length = 200
_word_format_symbols = {
    None:'',
    'word': '',
    'word_with_syllables': _syllable_chars,
    'word_with_all_numeric_stresses': [_syllable_chars] + list(_numeric_stress_map.values()),
    'word_with_only_multiple_numeric_stresses': _numeric_stress_map.values(),
    'number_stressed_word': _numeric_stress_map.values(),
    'utf8_stressed_word': _utf8_stress_map.values(),
    'ascii_stressed_word': _ascii_stress_map.values()
}

class PhonologyEngine:
    def __init__(self):
        def _collapsor(processed_phrase, phrase, normalized_phrase, letter_map, word_format=None):
            if word_format:
                return processed_phrase[word_format]
            else:
                return processed_phrase

        self.collapsor = _collapsor
        self.phrase_separators = _phrase_separators

    def _process_phrase(self, phrase, include_syllables):
        if len(phrase) > _max_prase_length:
            raise Exception('Phrase "%s" length exceeds %d char limit' % (phrase, _max_prase_length))
        
        handle = phonology_engine_process_phrase(phrase)

        offset = 0
        
        with PhonologyEngineOutput(handle) as output:
            res = []
            for i in range(output.get_word_count()):
                word = output.get_word(i, include_syllables=False)

                try:
                    start_index = phrase.index(word, offset)
                    word_span = start_index, start_index + len(word)
                    offset = word_span[1]
                except ValueError:
                    word_span = None

                res.append(
                    {
                    'word': word,
                    'word_with_syllables': output.get_word(i, include_syllables=True),
                    'number_stressed_word': output.get_word_with_numeric_stress(i, include_syllables=include_syllables),
                    'utf8_stressed_word': output.get_word_with_utf8_stress(i, include_syllables=include_syllables),
                    'ascii_stressed_word': output.get_word_with_ascii_stress(i, include_syllables=include_syllables),
                    'word_with_all_numeric_stresses': output.get_word_with_all_numeric_stresses(i, include_syllables=include_syllables),
                    'word_with_only_multiple_numeric_stresses': output.get_word_with_only_multiple_numeric_stresses(i, include_syllables=include_syllables),
                    'syllables': output.get_word_syllables(i),
                    'stress_options': output.get_word_stress_options(i),
                    'word_span': word_span
                    }
                )
                                
            return res

    def _process(self, text, separators, normalize=True, include_syllables=True, normalize_only=False):
        p = (r'[^' + re.escape(separators) + r']+') if separators else r'^.*$'
        pattern = re.compile(p)
        if len(text.strip()) == 0:
            yield text

        for m in pattern.finditer(text):
            phrase = m.group()

            if normalize:
                handle = phonology_engine_normalize_text(phrase)
                with PhonologyEngineNormalizedPhrases(handle) as normalized_phrases:
                    if normalize_only:
                        for normalized_phrase, letter_map in normalized_phrases:
                            yield normalized_phrase, phrase, normalized_phrase, letter_map
                    else:
                        for normalized_phrase, letter_map in normalized_phrases:
                            processed_phrase = self._process_phrase(normalized_phrase, include_syllables)
                            yield processed_phrase, phrase, normalized_phrase, letter_map
            else:
                processed_phrase = self._process_phrase(phrase, include_syllables)
                yield processed_phrase, phrase, phrase, list(range(len(phrase)))

    def get_collapse_formats(self):
        return _word_format_symbols.keys()

    def process(self, s, include_syllables=False):
        return self._process(s, separators=self.phrase_separators, normalize=True, include_syllables=include_syllables, normalize_only=False)

    def process_and_collapse(self, s, word_format='word', normalize=True, include_syllables=False):
        processed = self._process(s, separators=self.phrase_separators, normalize=normalize, include_syllables=include_syllables, normalize_only=False)
        return self.collapse(s, processed, word_format)

    def collapse(self, original_text, output, word_format='word'):
        if word_format not in _word_format_symbols:
            raise Exception('Invalide word format "%s". Can be one of: %s.' % (word_format, str(_word_format_symbols.keys())))

        processed_words = []
        for processed_phrase, _, _, _ in output:
            if isinstance(processed_phrase, list):
                for word_details in processed_phrase:
                    if isinstance(word_details, dict):
                        processed_words.append(word_details[word_format])
                    else:
                        processed_words.append(word_details)
            else:
                processed_words.append(processed_phrase)

        return ' '.join(processed_words)

    def normalize(self, text):
        return self._process(text, separators=self.phrase_separators, normalize=True, include_syllables=False, normalize_only=True)

    def normalize_and_collapse(self, text):
        return self.collapse(text, self._process(text, separators=self.phrase_separators, normalize=True, include_syllables=False, normalize_only=True))


