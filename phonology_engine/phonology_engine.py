# -*- coding: utf-8 -*-
from os.path import join, dirname, abspath
from .wm_wngine_output import WMEngineOutput

_phrase_separators = '.?!;:\r\n'
_max_prase_length = 200

class PhonologyEngine:
    def __init__(self):
        pass

    def _process(self, text, separators=_phrase_separators):
        text = text.strip()
        if len(text) == 0:
            return text
        if len(separators) == 0:
            if len(text) > _max_prase_length:
                raise Exception('Phrase "%s" length exceeds %d char limit' % (text, _max_prase_length))

            output = WMEngineOutput(text)
            
            res = [
                    {
                    'word': output.getWord(i),
                    'syllables': output.getWordSyllables(i),
                    'stress_options': output.getWordStressOptions(i)
                    }

                    for i in range(output.getWordCount())
                ]
                
            return res

        processed_phrases = []
        for phrase in text.split(separators[0]):
            processed_phrases.append(self._process(phrase, separators[1:]))
        
        return (separators[0], processed_phrases)

    def process(self, s):
        return self._process(s)

if __name__ == '__main__':
    from pprint import pprint

    pe = PhonologyEngine()
    proc = pe.process('Europos tautos kuri geriausia. Laba diena. Viskas bus gerai!')
    pprint(proc)