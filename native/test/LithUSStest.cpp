///////////////////////////////////////////////////////////////////////////////////////////////////
//
// Projektas LIEPA (https://liepa.ra�tija.lt)
// Sintezatoriaus komponentas LithUSStest.exe
// Failas LithUSStest.cpp
// Autorius dr. Pijus Kasparaitis (pkasparaitis@yahoo.com)
// 2015 08 11
//
///////////////////////////////////////////////////////////////////////////////////////////////////

extern "C" {
	#include "../include/common.h"
	#include "../include/LithUSS_Error.h"
	#include "../include/Engine.h"
}

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define MAX_PASTR_SK 10
#define MAX_PASTR_ILG 1000
#define PAGE_SIZE 1600

void spausdinti_loga(const char *pranesimas)
{
	FILE *stream;
	stream = fopen("LUSS_log.txt", "a+");
	fprintf(stream, "%s\n", pranesimas);
	printf("%s\n", pranesimas);
	fclose(stream);
}

typedef struct SynthData
{
	char *text;
	int *evsz;
} SYNTHDATA, *PSYNTHDATA;

int main(int argc, char *argv[])
{
	//tekstiniu duomenu nuskaitymas pastraipomis
	FILE *df;
	char eil[MAX_PASTR_SK][MAX_PASTR_ILG];
	int pastrSk;

	int hr = 0;
	if ((df = fopen("duom.txt", "rb")) == NULL)
	{
		spausdinti_loga("Nepavyko atidaryti duom.txt failo");
		hr = -1;
	}

	hr = PhonologyEngineInit();

	if (hr == 0)
	{
		int i = 0, j = 0, ch;
		do
		{
			ch = fgetc(df);
			if ((ch == '\n') || (ch == '\r') || (ch == EOF))
			{
				eil[i][j] = 0;
				if (j > 0)
				{
					if (i < MAX_PASTR_SK - 1)
						i++;
				}
				j = 0;
			}
			else
			{
				eil[i][j] = ch;
				if (ch > 200) 
					*(&ch) = ch; 
				if (j < MAX_PASTR_ILG - 1)
					j++;
			}
		} while (ch != EOF);
		fclose(df);
		pastrSk = i;
	}

	int evsize[MAX_PASTR_SK];
	PSYNTHDATA pDataArray[MAX_PASTR_SK];

	//sintezavimas pastraipomis
	//struct event {short Id; short phonviz; int charOffset; long signOffset;};

	int k;

	if (hr == 0)
	{
		for (k = 0; k < pastrSk; k++)
		{
			pDataArray[k] = (PSYNTHDATA) malloc(sizeof(SYNTHDATA));
			if (pDataArray[k] != NULL)
			{
				pDataArray[k]->text = eil[k];

				int eillen = strlen(eil[k]) * 2;
				if (eillen < PAGE_SIZE)
					eillen = PAGE_SIZE;

				evsize[k] = eillen;
				pDataArray[k]->evsz = &evsize[k];
			}
		}
	}

	unsigned long hrM[MAX_PASTR_SK];
	PhonologyEngineOutputHandle hOutput;

	if (hr == 0)
	{
		for (k = 0; k < pastrSk; k++)
		{
			if (pDataArray[k]->evsz == NULL)
				return 9;

			NormalizedTextHandle handle = NULL;
			int res = PhonologyEngineNormalizeText(pDataArray[k]->text, &handle);
			if (res != 0) return res;

			int phraseCount = 0;
			res = PhonologyEngineNormalizedTextGetPhraseCount(handle, &phraseCount);
			if (res != 0) return res;

			for (int p = 0; p < phraseCount; p++)
			{			
				char * szPhrase = NULL;
				res = PhonologyEngineNormalizedTextGetPhrase(handle, p, &szPhrase);
				if (res != 0) return res;

				hrM[k] = -PhonologyEngineProcessPhrase(szPhrase, &hOutput);

				int wordCount;
				res = PhonologyEngineOutputGetWordCount(hOutput, &wordCount);
				if (res != 0) return res;

				for (int l = 0; l < wordCount; l++)
				{
					char * szWord = NULL;
					char * szSyllables = NULL;
					int optionCount = 0, letterIndex, stressType, vocabulary, grammarRule;
					res = PhonologyEngineOutputGetWord(hOutput, l, &szWord);
					if (res != 0) return res;
					res = PhonologyEngineOutputGetWordStressOptionCount(hOutput, l, &optionCount);
					if (res != 0) return res;

					for (int m = 0; m < optionCount; m++)
					{
						res = PhonologyEngineOutputGetWordStressOption(hOutput, l, m, &letterIndex, &stressType, &vocabulary, &grammarRule);
						if (res != 0) return res;

						res = PhonologyEngineOutputGetWordSyllables(hOutput, l, &szSyllables);

						printf("Option: %d, %d, %d\n\n", letterIndex, stressType, grammarRule);
					}

					printf("%s\n", szWord);
				}
			}

			res = PhonologyEngineNormalizedTextFree(&handle);
			if (res != 0) return -6;

			res = PhonologyEngineOutputFree(&hOutput);
			if (res != 0) return -7;
		}
	}

	return hr;
}
