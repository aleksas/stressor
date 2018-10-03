from . import wm_engine_native

class WMEngineOutput:
    def __init__(self, text, normalize=True):
        self.handle = wm_engine_native.synthesizeWholeTextAlt(text, normalize)

    def free(self):
        wm_engine_native.WMEngineOutputFree(self.handle)

    def getWordCount(self):
        return wm_engine_native.WMEngineOutputGetWordCount(self.handle).value

    def getWord(self, index):
        if index >= self.getWordCount():
            raise Exception('Value out of bounds')

        return wm_engine_native.WMEngineOutputGetWord(self.handle, index)

    def getWordSyllables(self, index):
        if index >= self.getWordCount():
            raise Exception('Value out of bounds')

        return wm_engine_native.WMEngineOutputGetWordSyllables(self.handle, index)

    def getWordStressOptions(self, index):
        if index >= self.getWordCount():
            raise Exception('Value out of bounds')

        return wm_engine_native.WMEngineOutputGetWordStressOptions(self.handle, index)

        