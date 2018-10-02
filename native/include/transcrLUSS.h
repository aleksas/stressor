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

typedef void * WMEngineOutputHandle;
typedef int Result;
	
EXPORT Result initTranscrLUSS();

EXPORT Result synthesizeWholeTextAlt(char *tekstas, bool normalize, WMEngineOutputHandle * pHandle);
EXPORT Result WMEngineOutputFree(WMEngineOutputHandle * pHandle);

EXPORT Result WMEngineOutputGetWordCount(WMEngineOutputHandle hOutput, int * pValue);
EXPORT Result WMEngineOutputGetWord(WMEngineOutputHandle hOutput, int wordIndex, char ** pszValue);
EXPORT Result WMEngineOutputGetWordSyllables(WMEngineOutputHandle hOutput, int wordIndex, char ** pszValue);
EXPORT Result WMEngineOutputGetWordStressOptionCount(WMEngineOutputHandle hOutput, int wordIndex, int * pValue);
EXPORT Result WMEngineOutputGetWordStressOptionSelected(WMEngineOutputHandle hOutput, int wordIndex, int * pValue);
EXPORT Result WMEngineOutputGetWordStressOption(WMEngineOutputHandle hOutput, int wordIndex, int optionIndex, int * pLetterIndex, int * pStressType, int * pGrammarRule);

}

#endif
