///////////////////////////////////////////////////////////////////////////////////////////////////
//
// Projektas LIEPA (https://liepa.ra�tija.lt)
// Sintezatoriaus komponentas LithUSS.dll
// Failas transcrLUSS.h
// Autorius dr. Pijus Kasparaitis (pkasparaitis@yahoo.com)
// 2015 08 11
//
///////////////////////////////////////////////////////////////////////////////////////////////////

#ifndef __TRANSCRLUSS_H__
#define __TRANSCRLUSS_H__

#include "common.h"

extern "C" {

int KircTranskr(char* eil, char* TrZodis, int TrEilIlg, unsigned short* unitsR,  unsigned short* unitsRNextSep, 
				int* unitsLet, int* letPos, int rules2use);
int KircTranskrAlt(char *eil, int *letPos, int rules2use, char * stringBuffer, char * stressBuffer, int bufferSize);
				
EXPORT int initTranscrLUSS();

EXPORT int synthesizeWholeTextAlt(char *tekstas, char * stringBuffer, char * stressBuffer, int bufferSize);

}

#endif
