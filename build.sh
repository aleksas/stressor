#!/bin/bash

g++ args -fPIC -m32 -g \
  Transkr.cpp transcrLUSS.cpp Skiemen.cpp Kircdb.cpp fv2id.cpp \
  ArKirciuoti.cpp strtokf.cpp stringWithLetterPosition.cpp TextNormalization.cpp \
  -shared -o ../../phonology_engine/Linux_x86/libPhonologyEngine.so -Wno-write-strings

g++ args -fPIC -g \
  Transkr.cpp transcrLUSS.cpp Skiemen.cpp Kircdb.cpp fv2id.cpp \
  ArKirciuoti.cpp strtokf.cpp stringWithLetterPosition.cpp TextNormalization.cpp \
  -shared -o ../../phonology_engine/Linux_x86_64/libPhonologyEngine.so -Wno-write-strings
