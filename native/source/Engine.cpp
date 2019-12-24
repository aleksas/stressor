#include "../include/common.h"
#include "../include/Engine.h"
#include "../include/LithUSS_Error.h"
#include "transcrLUSSInternal.h"
#include "TextNormalization.h"

#include <stdlib.h>
#include <string.h>
#include <stdio.h>

char * szEmptyStr = "\0";

extern "C" {

EXPORT Result PhonologyEngineNormalizeText(char * szText, NormalizedTextHandle * pHandle)
{
	Result res = 0;
	char * szNormalizedText = NULL;
	int * pArLetterPosistion = NULL;
	int bufferSize = 0;

	if (!pHandle) return -1;

	NormalizedText * pNormalizedText = (NormalizedText*) calloc(1, sizeof(NormalizedText));
	if (!pNormalizedText) return -2;

	res = normalize(szText, &szNormalizedText, &pArLetterPosistion, &bufferSize);
	if (res != 0) return res;

	char *pos = szNormalizedText;
	char sakinys[200];
	char * pPhrases[1024];
	int * pPhraseLetterMap[1024];
	int n, phraseCount = 0;

	while ((pos != (void*)1))
	{
		int hr2 = 0;
		int lp = (int)(pos - szNormalizedText);
		n = sscanf(pos, "%[^\n]", sakinys);
		if (n < 0)
			break;
		if (n == 0)
			sakinys[0] = 0; //arba if(n == 0) continue; apsauga nuo tusciu eiluciu \n

		int rules2use = 1155 * 75 / 100; //75% total_auto_rules
		if (strcmp(sakinys, " ") == 0)
			sakinys[0] = 0; //jei eilute tuscia arba tik neskaitytini simboliai
		
		pPhrases[phraseCount] = (char*) malloc((strlen(sakinys) + 1) * sizeof(char));
		pPhraseLetterMap[phraseCount] = (int*) malloc((strlen(sakinys)) * sizeof(int));
		if (!pPhrases[phraseCount] || !pPhraseLetterMap[phraseCount]) return -3;
		strcpy(pPhrases[phraseCount], sakinys);
		memcpy(pPhraseLetterMap[phraseCount], pArLetterPosistion + lp, strlen(sakinys) * sizeof(int));

		pos = strchr(pos, '\n') + 1;
		phraseCount++;
	}

	pNormalizedText->phraseCount = phraseCount;
	pNormalizedText->pSzPhrases = (char**) malloc(sizeof(char*) * phraseCount);
	pNormalizedText->pArLetterMap = (int**) malloc(sizeof(int*) * phraseCount);

	if (!pNormalizedText->pSzPhrases || !pNormalizedText->pArLetterMap) return -4;

	memcpy(pNormalizedText->pSzPhrases, pPhrases, sizeof(char*) * phraseCount);
	memcpy(pNormalizedText->pArLetterMap, pPhraseLetterMap, sizeof(int*) * phraseCount);

	*pHandle = pNormalizedText;	

	free(pArLetterPosistion);
	free(szNormalizedText);

	return 0;
}

EXPORT Result PhonologyEngineNormalizedTextFree(NormalizedTextHandle * pHandle)
{
	if (!pHandle) return -1;

	NormalizedText * pNormalizedText = GetObjectPtr(NormalizedText, *pHandle);

	if (pNormalizedText)
	{
		for (int i = 0; i < pNormalizedText->phraseCount; i++)
		{
			free(pNormalizedText->pSzPhrases[i]);
			free(pNormalizedText->pArLetterMap[i]);
		}
	}

	free(pNormalizedText->pSzPhrases);
	free(pNormalizedText->pArLetterMap);
	free(pNormalizedText);
	*pHandle = NULL;

	return 0;
}

EXPORT Result PhonologyEngineNormalizedTextGetPhraseCount(NormalizedTextHandle handle, int * pValue)
{
	NormalizedText * pOutput = GetObjectPtr(NormalizedText, handle);

	if (!handle) return -1;
	if (!pValue) return -2;

	*pValue = pOutput->phraseCount;

	return 0;
}

EXPORT Result PhonologyEngineNormalizedTextGetPhrase(NormalizedTextHandle handle, int index, char ** pSzValue)
{
	NormalizedText * pOutput = GetObjectPtr(NormalizedText, handle);

	if (!handle) return -1;
	if (!pSzValue) return -2;

	int count = 0;

	if (index < 0 || index >= pOutput->phraseCount) return -3;

	*pSzValue = pOutput->pSzPhrases[index];

	return 0;
}

EXPORT Result PhonologyEngineNormalizedTextGetPhraseLetterMap(NormalizedTextHandle handle, int index, int ** pArValue, int * pCount)
{
	NormalizedText * pOutput = GetObjectPtr(NormalizedText, handle);

	if (!handle) return -1;
	if (!pArValue) return -2;
	if (!pCount) return -3;

	int count = 0;

	if (index < 0 || index >= pOutput->phraseCount) return -4;

	*pArValue = pOutput->pArLetterMap[index];
	*pCount = strlen(pOutput->pSzPhrases[index]);

	return 0;
}

////////////Pagrindine sintezavimo funkcija////////////////////////////////////////////////////////////////////////////////
EXPORT Result PhonologyEngineProcessPhrase(char * szNormalizedText, PhonologyEngineOutputHandle * pHandle)
{
	char stringBuffer[1024];
	char stressBuffer[1024];	
	int bufferSize = 1024;

	PhonologyEngineOutput * pOutput = (PhonologyEngineOutput*) calloc(1, sizeof(PhonologyEngineOutput));
	
	if (!pOutput)
		return -1;
		
	int rules2use = 1155 * 75 / 100; //75% total_auto_rules
	int unitsRowsLength = KircTranskrAlt(szNormalizedText, rules2use, stringBuffer, stressBuffer, bufferSize, &pOutput->pArOutputWords, &pOutput->wordCount);
	if (unitsRowsLength > 2)
		return ERROR_LITHUSS_EVENTS_ARRAY_OVERFLOW;

	*pHandle = pOutput;

	return 0;
}

EXPORT Result PhonologyEngineOutputFree(PhonologyEngineOutputHandle * pHandle)
{
	if (!pHandle) return -1;

	PhonologyEngineOutput * pOutput = GetObjectPtr(PhonologyEngineOutput, *pHandle);

	for (int i = 0; i < pOutput->wordCount; i++)
	{
		free(pOutput->pArOutputWords[i].pStressOptions);
	}
	free(pOutput->pArOutputWords);
	free(pOutput);
	*pHandle = NULL;

	return 0;
}

EXPORT Result PhonologyEngineOutputGetWordCount(PhonologyEngineOutputHandle hOutput, int * pValue)
{
	PhonologyEngineOutput * pOutput = GetObjectPtr(PhonologyEngineOutput, hOutput);

	if (!hOutput) return -1;
	if (!pValue) return -2;

	*pValue = pOutput->wordCount;

	return 0;
}

EXPORT Result PhonologyEngineOutputGetWord(PhonologyEngineOutputHandle hOutput, int wordIndex, char ** pszValue)
{
	PhonologyEngineOutput * pOutput = GetObjectPtr(PhonologyEngineOutput, hOutput);

	if (!hOutput) return -1;
	if (!pszValue) return -2;
	if (wordIndex >= pOutput->wordCount) return -3;

	*pszValue = pOutput->pArOutputWords[wordIndex].szWord;

	return 0;
}

EXPORT Result PhonologyEngineOutputGetWordSyllables(PhonologyEngineOutputHandle hOutput, int wordIndex, char ** pszValue)
{
	PhonologyEngineOutput * pOutput = GetObjectPtr(PhonologyEngineOutput, hOutput);

	if (!hOutput) return -1;
	if (!pszValue) return -2;
	if (wordIndex >= pOutput->wordCount) return -3;

	if (pOutput->pArOutputWords[wordIndex].pStressOptions)
	{
		*pszValue = pOutput->pArOutputWords[wordIndex].pStressOptions->Skiem;
	} else {
		*pszValue = szEmptyStr;
	}

	return 0;
}

EXPORT Result PhonologyEngineOutputGetWordStressOptionCount(PhonologyEngineOutputHandle hOutput, int wordIndex, int * pValue)
{
	PhonologyEngineOutput * pOutput = GetObjectPtr(PhonologyEngineOutput, hOutput);

	if (!hOutput) return -1;
	if (!pValue) return -2;

	if (wordIndex >= pOutput->wordCount) return -3;

	*pValue = pOutput->pArOutputWords[wordIndex].stressOptionCount;

	return 0;
}

EXPORT Result PhonologyEngineOutputGetWordStressOptionSelected(PhonologyEngineOutputHandle hOutput, int wordIndex, int * pValue)
{
	PhonologyEngineOutput * pOutput = GetObjectPtr(PhonologyEngineOutput, hOutput);

	if (!hOutput) return -1;
	if (!pValue) return -2;
	if (wordIndex >= pOutput->wordCount) return -3;

	*pValue = pOutput->pArOutputWords[wordIndex].selectedStressOptionIndex;

	return 0;
}

EXPORT Result PhonologyEngineOutputGetWordStressOption(PhonologyEngineOutputHandle hOutput, int wordIndex, int optionIndex, int * pLetterIndex, int * pStressType, int * pVocabulary, int * pGrammarRule)
{
	PhonologyEngineOutput * pOutput = GetObjectPtr(PhonologyEngineOutput, hOutput);

	if (!hOutput) return -1;
	if (!pLetterIndex) return -2;
	if (!pStressType) return -3;
	if (!pVocabulary) return -3;
	if (!pGrammarRule) return -4;
	if (wordIndex >= pOutput->wordCount) return -5;
	if (optionIndex >= pOutput->pArOutputWords[wordIndex].stressOptionCount) return -6;

	*pLetterIndex = pOutput->pArOutputWords[wordIndex].pStressOptions[optionIndex].KirtRaide - 1;
	*pStressType = pOutput->pArOutputWords[wordIndex].pStressOptions[optionIndex].Priegaide;
	*pVocabulary = pOutput->pArOutputWords[wordIndex].pStressOptions[optionIndex].Zodynas;
	*pGrammarRule = pOutput->pArOutputWords[wordIndex].pStressOptions[optionIndex].GramForma;

	return 0;
}

}