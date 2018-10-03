from . import pe_native

class PhonologyEngineOutput:
    def __init__(self, text, normalize=True):
        self.handle = pe_native.synthesizeWholeTextAlt(text, normalize)

    def free(self):
        pe_native.PhonologyEngineOutputFree(self.handle)

    def getWordCount(self):
        return pe_native.PhonologyEngineOutputGetWordCount(self.handle).value

    def getWord(self, index):
        if index >= self.getWordCount():
            raise Exception('Value out of bounds')

        return pe_native.PhonologyEngineOutputGetWord(self.handle, index)

    def getWordSyllables(self, index):
        if index >= self.getWordCount():
            raise Exception('Value out of bounds')

        return pe_native.PhonologyEngineOutputGetWordSyllables(self.handle, index)

    def getWordStressOptions(self, index):
        if index >= self.getWordCount():
            raise Exception('Value out of bounds')

        return pe_native.PhonologyEngineOutputGetWordStressOptions(self.handle, index)

        