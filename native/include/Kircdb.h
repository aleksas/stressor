///////////////////////////////////////////////////////////////////////////////////////////////////
//
// Projektas LIEPA (https://liepa.ra�tija.lt)
// Sintezatoriaus komponentas transcrLUSS.dll
// Failas KircDB.h
// Autorius dr. Pijus Kasparaitis (pkasparaitis@yahoo.com)
// 2015 08 11
//
///////////////////////////////////////////////////////////////////////////////////////////////////

#ifndef KIRC_DB
#define KIRC_DB

extern "C" {

#define MAX_WORD_LENTH 136

typedef struct struct_variantas {int Zodynas;
                  int GramForma;
                  int KamNr;
                  int KirtRaide;
                  int Priegaide;
                  int Prioritetas;
                  char Skiem[MAX_WORD_LENTH];
                  char Tarpt;} variantas;

int Kirciuoti(char *Zodis, char *SkPb, variantas *Variant);
void initKircLUSS();
}

#endif // KIRC_DB