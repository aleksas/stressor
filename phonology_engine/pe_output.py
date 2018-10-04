from . import pe_native

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
        return pe_native.phonology_engine_output_get_word_count(self.handle).value

    def get_word(self, index):
        if index >= self.get_word_count():
            raise Exception('Value out of bounds')

        return pe_native.phonology_engine_output_get_word(self.handle, index)

    def get_word_syllables(self, index):
        if index >= self.get_word_count():
            raise Exception('Value out of bounds')

        return pe_native.phonology_engine_output_get_word_syllables(self.handle, index)

    def get_word_stress_options(self, index):
        if index >= self.get_word_count():
            raise Exception('Value out of bounds')

        return pe_native.phonology_engine_output_get_word_stress_options(self.handle, index)

        