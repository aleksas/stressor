# -*- coding: utf-8 -*-

from ctypes import CDLL, c_int, c_char_p, create_string_buffer, byref
from os.path import join, dirname, abspath

lib_path = join(dirname(__file__), "Linux_x86_64", "libtranscrLUSS.so")
libtranscrLUSS = CDLL(lib_path)

initTranscrLUSS = libtranscrLUSS.initTranscrLUSS
synthesizeWholeTextAlt = libtranscrLUSS.synthesizeWholeTextAlt
GetMinBufferSize = libtranscrLUSS.GetMinBufferSize

orig_kirciai = {1:"nekirciuota", 2:"tr", 4:"des", 8:"gal", 16:"kirtis 1 s i des"}
map_stess = {0:0, 1:1, 2:2, 4:3, 8:4, 16:5}

native_encoding = 'windows-1257'

def check(res):
    if res != 0:
        raise Exception("initTranscrLUSS failed: %d" % res)

check( initTranscrLUSS() )

class Sandara:
    def __init__(self):
        self.minBufferSize = GetMinBufferSize()

        self.stringBuffer = create_string_buffer(b'\000' * self.minBufferSize)
        self.stressBuffer = create_string_buffer(b'\000' * self.minBufferSize)

    def process(self, s):
        cs = c_char_p(s.encode(native_encoding))

        check( synthesizeWholeTextAlt(
            cs,
            byref(self.stringBuffer),
            byref(self.stressBuffer),
            self.minBufferSize) )

        decoded_native = self.stringBuffer.raw.decode(native_encoding)

        sentence = decoded_native.replace('\x00', ' ').replace('\xff', ' ').strip().replace('_', ' ')
        stresses = [map_stess[int(b)] if int(b) >= 0 and int(b) <= 16 else 0 for b in self.stressBuffer.raw[0:len(sentence)]]

        stressed = ''.join([a + str(s) if s > 1 else a for a,s in zip(sentence, stresses)]).strip()

        return stressed
        