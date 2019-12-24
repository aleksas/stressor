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

typedef void * NormalizedTextHandle;
typedef void * PhonologyEngineOutputHandle;
typedef int Result;
	
EXPORT Result PhonologyEngineInit();

EXPORT Result PhonologyEngineNormalizeText(char * szText, NormalizedTextHandle * pHandle);
EXPORT Result PhonologyEngineNormalizedTextFree(NormalizedTextHandle * pHandle);
EXPORT Result PhonologyEngineNormalizedTextGetPhraseCount(NormalizedTextHandle handle, int * pValue);
EXPORT Result PhonologyEngineNormalizedTextGetPhrase(NormalizedTextHandle handle, int index, char ** pSzValue);
EXPORT Result PhonologyEngineNormalizedTextGetPhraseLetterMap(NormalizedTextHandle handle, int index, int ** pArValue, int * count);

EXPORT Result PhonologyEngineProcessPhrase(char * szNormalizedText, PhonologyEngineOutputHandle * pHandle);
EXPORT Result PhonologyEngineOutputFree(PhonologyEngineOutputHandle * pHandle);

EXPORT Result PhonologyEngineOutputGetWordCount(PhonologyEngineOutputHandle hOutput, int * pValue);
EXPORT Result PhonologyEngineOutputGetWord(PhonologyEngineOutputHandle hOutput, int wordIndex, char ** pszValue);
EXPORT Result PhonologyEngineOutputGetWordSyllables(PhonologyEngineOutputHandle hOutput, int wordIndex, char ** pszValue);
EXPORT Result PhonologyEngineOutputGetWordStressOptionCount(PhonologyEngineOutputHandle hOutput, int wordIndex, int * pValue);
EXPORT Result PhonologyEngineOutputGetWordStressOptionSelected(PhonologyEngineOutputHandle hOutput, int wordIndex, int * pValue);
EXPORT Result PhonologyEngineOutputGetWordStressOption(PhonologyEngineOutputHandle hOutput, int wordIndex, int optionIndex, int * pLetterIndex, int * pStressType, int * pVocabulary, int * pGrammarRule);

}

#endif
