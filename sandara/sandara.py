# -*- coding: utf-8 -*-

from ctypes import CDLL, c_int, c_char_p, create_string_buffer, byref
from os.path import join, dirname, abspath

orig_kirciai = {1:"nek", 2:"tr", 4:"des", 8:"gal", 16:"kirtis 1 s i des"}
map_stess = {0:0, 1:1, 2:2, 4:3, 8:4, 16:5}

path = abspath('.')

libtranscrLUSS = CDLL(join(path, "libtranscrLUSS.so"))  

s = "Europos tautos kurdamos dar glaudesnę tarpusavio sąjungą yra pasiryžusios bendrų vertybių pagrindu siekti taikios ateities"

cs = c_char_p(s.encode('windows-1257'))

initTranscrLUSS = libtranscrLUSS.initTranscrLUSS
synthesizeWholeTextAlt = libtranscrLUSS.synthesizeWholeTextAlt
GetMinBufferSize = libtranscrLUSS.GetMinBufferSize

res = initTranscrLUSS()

bufferSize = GetMinBufferSize()

stringBuffer = create_string_buffer(b'\000' * bufferSize)
stressBuffer = create_string_buffer(b'\000' * bufferSize)

res = synthesizeWholeTextAlt(cs, byref(stringBuffer), byref(stressBuffer), bufferSize)

sentence = stringBuffer.raw.decode('windows-1257').replace('\x00', ' ').replace('\xff', ' ').strip().replace('_', ' ')
stresses = [map_stess[int(b)] if int(b) >= 0 and int(b) <= 16 else 0 for b in stressBuffer.raw[0:len(sentence)]]

stressed = ''.join([a + str(s) if s > 1 else a for a,s in zip(sentence, stresses)]).strip()

stresses = stresses