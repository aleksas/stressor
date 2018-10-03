#!/bin/bash

sudo apt-get install -y libc6-dev-i386

cd native/source

mkdir -p ../../phonology_engine/Linux_x86

g++ -fPIC -m32 -g \
  -I ../include/ \
  Transkr.cpp transcrLUSS.cpp Skiemen.cpp Kircdb.cpp fv2id.cpp \
  ArKirciuoti.cpp strtokf.cpp stringWithLetterPosition.cpp TextNormalization.cpp \
  -shared -o ../../phonology_engine/Linux_x86/libPhonologyEngine.so -Wno-write-strings

mkdir -p ../../phonology_engine/Linux_x86_64

g++ -fPIC -g \
  -I ../include/ \
  Transkr.cpp transcrLUSS.cpp Skiemen.cpp Kircdb.cpp fv2id.cpp \
  ArKirciuoti.cpp strtokf.cpp stringWithLetterPosition.cpp TextNormalization.cpp \
  -shared -o ../../phonology_engine/Linux_x86_64/libPhonologyEngine.so -Wno-write-strings
