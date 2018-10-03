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

typedef void * PhonologyEngineOutputHandle;
typedef int Result;
	
EXPORT Result PhonologyEngineInit();

EXPORT Result PhonologyEngineProcessPhrase(char *tekstas, bool normalize, PhonologyEngineOutputHandle * pHandle);
EXPORT Result PhonologyEngineOutputFree(PhonologyEngineOutputHandle * pHandle);

EXPORT Result PhonologyEngineOutputGetWordCount(PhonologyEngineOutputHandle hOutput, int * pValue);
EXPORT Result PhonologyEngineOutputGetWord(PhonologyEngineOutputHandle hOutput, int wordIndex, char ** pszValue);
EXPORT Result PhonologyEngineOutputGetWordSyllables(PhonologyEngineOutputHandle hOutput, int wordIndex, char ** pszValue);
EXPORT Result PhonologyEngineOutputGetWordStressOptionCount(PhonologyEngineOutputHandle hOutput, int wordIndex, int * pValue);
EXPORT Result PhonologyEngineOutputGetWordStressOptionSelected(PhonologyEngineOutputHandle hOutput, int wordIndex, int * pValue);
EXPORT Result PhonologyEngineOutputGetWordStressOption(PhonologyEngineOutputHandle hOutput, int wordIndex, int optionIndex, int * pLetterIndex, int * pStressType, int * pGrammarRule);

}

#endif
