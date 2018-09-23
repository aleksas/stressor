///////////////////////////////////////////////////////////////////////////////////////////////////
//
// Projektas LIEPA (https://liepa.ra�tija.lt)
// Sintezatoriaus komponentas LithUSStest.exe
// Failas LithUSStest.cpp
// Autorius dr. Pijus Kasparaitis (pkasparaitis@yahoo.com)
// 2015 08 11
//
///////////////////////////////////////////////////////////////////////////////////////////////////
#include "StdAfx.h"

extern "C" {
	#include "../include/common.h"
	#include "../include/LithUSS_Error.h"
	#include "../include/transcrLUSS.h"
}

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
	short *largebf;
	unsigned int *largebfsize;
	int *evsz;
	int greitis;
	int tonas;
} SYNTHDATA, *PSYNTHDATA;

int TextToSound(void *lpParam)
{
	PSYNTHDATA pData = (PSYNTHDATA)lpParam;
	if (pData == NULL)
		return 7;
	if (pData->largebf == NULL)
		return 8;
	if (pData->evsz == NULL)
		return 9;
	int hr = -synthesizeWholeTextAlt(pData->text);
	return hr;
}

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

	hr = initTranscrLUSS();

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
	unsigned int largebufsize[MAX_PASTR_SK];
	PSYNTHDATA pDataArray[MAX_PASTR_SK];

	//sintezavimas pastraipomis
	//struct event {short Id; short phonviz; int charOffset; long signOffset;};

	int k;
	int greitis = 100;
	int tonas = 100;

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

				if (greitis >= 100)
				{
					largebufsize[k] = eillen * 1250 * greitis / 100;
				}
				else //greitis < 100)
				{
					largebufsize[k] = eillen * 1250 * greitis / 150;
				}
				pDataArray[k]->largebfsize = &largebufsize[k];
				pDataArray[k]->largebf = (short *)calloc(largebufsize[k], sizeof(short)); //butina uznulinti, todel calloc

				evsize[k] = eillen;
				pDataArray[k]->evsz = &evsize[k];

				pDataArray[k]->greitis = greitis;
				pDataArray[k]->tonas = tonas;
			}
		}
	}

	unsigned long hrM[MAX_PASTR_SK];
	if (hr == 0)
	{
		for (k = 0; k < pastrSk; k++)
		{
			hrM[k] = TextToSound(pDataArray[k]);
		}
	}

	return hr;
}
