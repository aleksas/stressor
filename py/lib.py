# -*- coding: utf-8 -*-

from ctypes import CDLL, c_int, c_char_p
from os.path import join, dirname, abspath

path = abspath('.')

libtranscrLUSS = CDLL(join(path, "libtranscrLUSS.so"))  

s = "LABA DIENA"

cs = c_char_p(s.encode('windows-1257'))

initTranscrLUSS = libtranscrLUSS.initTranscrLUSS
synthesizeWholeTextAlt = libtranscrLUSS.synthesizeWholeTextAlt

res = initTranscrLUSS()
res = synthesizeWholeTextAlt(cs)
res = initTranscrLUSS()