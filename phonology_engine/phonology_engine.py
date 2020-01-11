# -*- coding: utf-8 -*-
from os.path import join, dirname, abspath
from .pe_output import PhonologyEngineOutput, PhonologyEngineNormalizedPhrases
from .pe_native import phonology_engine_process_phrase, phonology_engine_normalize_text
import re

_phrase_separators = '.?!;:\r\n,'
_max_prase_length = 200
_valid_word_formats = [None, 'word', 'word_with_syllables', 'word_with_all_numeric_stresses', 'word_with_only_multiple_numeric_stresses', 'number_stressed_word', 'utf8_stressed_word', 'ascii_stressed_word']

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

    def _get_word_mappings(self, phrase, normalized_phrase, letter_map, separators, offset_source=0, offset_normalized=0):
        if len(normalized_phrase) != len(letter_map):
            raise Exception("Phrase length differs from phrase letter map length (%d != %d)." % (len(normalized_phrase), len(letter_map)))
        mappings = []
        normalized_words = []

        span_first = 0
        map_length = len(letter_map)
        for i, _ in enumerate(letter_map):
            is_last = i == map_length - 1
            if normalized_phrase[i] == ' ' or is_last:
                if is_last:
                    i += 1
                    mapped_end = len(phrase)
                else:
                    last_index = len(letter_map) - 1 - letter_map[::-1].index(letter_map[i - 1])
                    if last_index == len(letter_map) - 1:
                        mapped_end = len(phrase)
                    else:
                        mapped_end = letter_map[last_index + 1]
                if i - span_first >= 1:
                    mapping = (letter_map[span_first], mapped_end), (span_first, i)
                    offsetted_mapping = (mapping[0][0] + offset_source, mapping[0][1] + offset_source), (mapping[1][0] + offset_source, mapping[1][1] + offset_source)
                    mappings.append( offsetted_mapping )
                    normalized_words.append( normalized_phrase[mapping[1][0]:mapping[1][1]])
                span_first = i + 1

        return mappings, normalized_words

    def _process(self, text, separators, normalize=True, include_syllables=True, normalize_only=False, letter_map=None):
        p = ('[^' + re.escape(separators) + ']+') if separators else '^.*$'
        pattern = re.compile(p)
        if len(text.strip()) == 0:
            yield text

        last_span_end = 0
        offset_normalized = 0
        for m in pattern.finditer(text):
            span = m.span()
            last_span_end = span[1]
            phrase = m.group()

            if normalize:
                handle = phonology_engine_normalize_text(phrase)
                with PhonologyEngineNormalizedPhrases(handle) as normalized_phrases:
                    if normalize_only:
                        for normalized_phrase, letter_map in normalized_phrases:
                            word_mappings, words = self._get_word_mappings(phrase, normalized_phrase, letter_map, separators, span[0], offset_normalized)
                            offset_normalized += len(normalized_phrase)
                            processed_phrase = []
                            
                            for (orig, norm), word in zip(word_mappings, words):
                                d = {
                                    'span_source': orig,                   
                                    'span_normalized': norm
                                }
                                d.update( { k:word for k in _valid_word_formats if k} )
                                processed_phrase.append(d)
                            yield processed_phrase, phrase, normalized_phrase, letter_map
                    else:
                        for normalized_phrase, letter_map in normalized_phrases:
                            word_mappings, _ = self._get_word_mappings(phrase, normalized_phrase, letter_map, separators, span[0], offset_normalized)
                            offset_normalized += len(normalized_phrase)

                            processed_phrase = self._process_phrase(normalized_phrase, include_syllables)
                            if len(processed_phrase) != len(word_mappings):
                                raise Exception("Word span calculation incosistent.")

                            for i, (orig, norm) in enumerate(word_mappings):
                                processed_phrase[i]['span_source'] = orig
                                processed_phrase[i]['span_normalized'] = norm
                                
                            yield processed_phrase, phrase, normalized_phrase, letter_map
            else:
                processed_phrase = self._process_phrase(phrase, include_syllables)
                yield processed_phrase, phrase, phrase, list(range(len(phrase)))

    def get_collapse_formats(self):
        return _valid_word_formats

    def process(self, s, include_syllables=False):
        return self._process(s.upper(), separators=self.phrase_separators, normalize=True, include_syllables=include_syllables, normalize_only=False)

    def process_and_collapse(self, s, word_format='word', normalize=True, include_syllables=False):
        return self.collapse(s, self._process(s, separators=self.phrase_separators, normalize=normalize, include_syllables=include_syllables, normalize_only=False), word_format)

    def collapse(self, original_text, output, word_format='word'):
        if word_format not in _valid_word_formats:
            raise Exception('Invalide word format "%s". Can be one of: %s.' % (word_format, str(_valid_word_formats)))

        def consolidate_phrase_words(phrase):
            last_word_details = None
            for word_details in phrase:
                if last_word_details == None:
                    last_word_details = word_details
                else:
                    if word_details['span_source'] == last_word_details['span_source']:
                        last_word_details['span_normalized'] = (
                            min(last_word_details['span_normalized'][0], word_details['span_normalized'][0]),
                            max(last_word_details['span_normalized'][1], word_details['span_normalized'][1]),
                        )

                        for word_format in _valid_word_formats:
                            if word_format:
                                last_word_details[word_format] += ' ' + word_details[word_format]
                    else:
                        yield last_word_details
                        last_word_details = word_details
            if last_word_details:
                yield last_word_details                

        res = original_text
        output_reversed = reversed(list(output))
        for element in output_reversed:
            processed_phrase, _, _, _ = element

            for word_details in reversed(list(consolidate_phrase_words(processed_phrase))):
                start, end = word_details['span_source']
                res = res[:start] + word_details[word_format] + res[end:]
        
        return res

    def normalize(self, text):
        return self._process(text, separators=self.phrase_separators, normalize=True, include_syllables=False, normalize_only=True)

    def normalize_and_collapse(self, text):
        return self.collapse(text, self._process(text, separators=self.phrase_separators, normalize=True, include_syllables=False, normalize_only=True))


