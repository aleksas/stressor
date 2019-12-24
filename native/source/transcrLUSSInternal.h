#ifndef TRANSCR_LUSS_INTERNAL
#define TRANSCR_LUSS_INTERNAL

#include "Kircdb.h"
#include "Transkr.h"
#include "Skiemen.h"
#include "ArKirciuoti.h"
#include "rezultC.h"

#define ILGIS1 500 //analizuojamos tekstines eilute ilgis
#define VARSK1 10  //transkribavimo variantu skaicius
#define ZODIL1 50  //maksimalus kirciuojamo zodzio ilgis

extern "C" {

typedef struct _NormalizedText {
	int phraseCount;
	char ** pSzPhrases;
	int ** pArLetterMap;
} NormalizedText;

typedef struct _WordStressOptions {
	int stressOptionCount;
	int selectedStressOptionIndex;
    char szWord[MAX_WORD_LENTH];
	variantas * pStressOptions;
} WordStressOptions;

typedef struct PhonologyEngineOutput_ {
    int wordCount;
    WordStressOptions * pArOutputWords;
    } PhonologyEngineOutput;

#define GetObjectPtr(objectType, objectHandle) ((objectType*) objectHandle)

void TarptautF(char *ez, char *Trmp, char Tarpt);
int VienasVarKirc1(variantas *Variant, int variantsk);
char FrazesPabaiga(char *zod);
int auto_rules_function(variantas *variants_array, int varsk, int rules2use);

int normalize(char * szText, char ** pszNormalizedTextBuffer, int ** ppLetterPositionMap, int * pBufferSize);
int KircTranskrAlt(char *eil, int rules2use, char * stringBuffer, char * stressBuffer, int bufferSize, WordStressOptions ** ppWordStressOptions, int * pWordStressOptionCount);

}

#endif