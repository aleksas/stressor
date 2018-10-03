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

typedef void * PhonologyEngneOutputHandle;
typedef int Result;
	
EXPORT Result PhonologyEngneInit();

EXPORT Result PhonologyEngneProcessPhrase(char *tekstas, bool normalize, PhonologyEngneOutputHandle * pHandle);
EXPORT Result PhonologyEngneOutputFree(PhonologyEngneOutputHandle * pHandle);

EXPORT Result PhonologyEngneOutputGetWordCount(PhonologyEngneOutputHandle hOutput, int * pValue);
EXPORT Result PhonologyEngneOutputGetWord(PhonologyEngneOutputHandle hOutput, int wordIndex, char ** pszValue);
EXPORT Result PhonologyEngneOutputGetWordSyllables(PhonologyEngneOutputHandle hOutput, int wordIndex, char ** pszValue);
EXPORT Result PhonologyEngneOutputGetWordStressOptionCount(PhonologyEngneOutputHandle hOutput, int wordIndex, int * pValue);
EXPORT Result PhonologyEngneOutputGetWordStressOptionSelected(PhonologyEngneOutputHandle hOutput, int wordIndex, int * pValue);
EXPORT Result PhonologyEngneOutputGetWordStressOption(PhonologyEngneOutputHandle hOutput, int wordIndex, int optionIndex, int * pLetterIndex, int * pStressType, int * pGrammarRule);

}

#endif
