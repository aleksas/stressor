# -*- coding: utf-8 -*-
from os.path import join, dirname, abspath
from .pe_output import PhonologyEngineOutput
from .pe_native import phonology_engine_process_phrase

_phrase_separators = '.?!;:\r\n'
_max_prase_length = 200

class PhonologyEngine:
    def __init__(self):
        pass

    def _process(self, text, separators=_phrase_separators, normalize=True):
        text = text.strip()
        if len(text) == 0:
            return text
        if len(separators) == 0:
            if len(text) > _max_prase_length:
                raise Exception('Phrase "%s" length exceeds %d char limit' % (text, _max_prase_length))
            
            handle = phonology_engine_process_phrase(text, normalize)
            
            with PhonologyEngineOutput(handle) as output:
                res = [
                        {
                        'word': output.get_word(i),
                        'syllables': output.get_word_syllables(i),
                        'stress_options': output.get_word_stress_options(i)
                        }

                        for i in range(output.get_word_count())
                    ]
                    
                return res

        phrases = text.split(separators[0])
        if len(phrases) == 1:
            return self._process(phrases[0], separators[1:])
        else:
            processed_phrases = []
            for phrase in phrases:
                processed_phrases.append(self._process(phrase, separators[1:]))
            
            return (separators[0], processed_phrases)

    def process(self, s, normalize=True):
        return self._process(s, normalize)

if __name__ == '__main__':
    from pprint import pprint

    pe = PhonologyEngine()
    proc = pe.process('Europos tautos kuri geriausia. Laba diena. Viskas bus gerai!')
    pprint(proc)