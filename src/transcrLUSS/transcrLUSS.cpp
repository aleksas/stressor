///////////////////////////////////////////////////////////////////////////////////////////////////
//
// Projektas LIEPA (https://liepa.raðtija.lt)
// Sintezatoriaus komponentas transcrLUSS.dll
// Failas transcrLUSS.cpp
// Autorius dr. Pijus Kasparaitis (pkasparaitis@yahoo.com)
// 2015 08 11
//
///////////////////////////////////////////////////////////////////////////////////////////////////
#include "StdAfx.h"

extern "C" {
	
#include "../include/transcrLUSS.h"
#include "../include/LithUSS_Error.h"
#include "../include/TextNormalization.h"
#include "../include/strtokf.h"
#include "transcrLUSSInternal.h"

//-------------------------------------------------------------------
void TarptautF(char *ez, char *Trmp, char Tarpt)
{
	// O trumpumo nustatymas
	int i, os = 0;
	for (i = 0; i <= strlen(ez); i++)
	{
		Trmp[i] = 0;
		if (ez[i] == 'O')
		{
			if ((1 << os) & Tarpt)
				Trmp[i] = 1;
			os++;
		}
	}
}

//------------------------------------------------------------------
int VienasVarKirc1(variantas *Variant, int variantsk)
{
	int i, j, varsk, mprio;
	j = 0;
	varsk = 0;
	while ((j < variantsk) && ((Variant[j].Zodynas == 0) || (Variant[j].Zodynas == 1)))
	{
		varsk++;
		j++;
	}

	if (varsk == 0)
		mprio = 0;
	else
		mprio = 20;

	for (i = j; i < variantsk; i++)
	{
		if (mprio <= Variant[i].Prioritetas)
		{
			varsk++;
			mprio = Variant[i].Prioritetas;
		}
	}

	return varsk;
}
//---------------------------------------------------
char FrazesPabaiga(char *zod)
{
	int i = strlen(zod) - 1;
	if (i < 1)
		return ' ';
	if (zod[i] == '\r')
	{
		zod[i] = '\0';
		i--;
	}
	switch (zod[i])
	{
	case '!':
	case ',':
	case '.':
	case ':':
	case ';':
		zod[i] = 0;
		return '.';
	case '?':
		zod[i] = 0;
		return '?';
	default:
		return ' ';
	}
}
//------------------------------------------------------------
int auto_rules_function(variantas *variants_array, int varsk, int rules2use)
{
	int i, j, f, new_varsk = varsk;

	int accepted_variants[100];
	for (i = 0; i < varsk; i++)
		accepted_variants[i] = 1;

	int yra_skirtingu_var = 0;
	for (i = 1; i < varsk; i++)
	{
		if ((variants_array[i - 1].KirtRaide != variants_array[i].KirtRaide) || (variants_array[i - 1].Priegaide != variants_array[i].Priegaide))
		{
			yra_skirtingu_var = 1;
			break;
		}
	}
	if (yra_skirtingu_var == 1)
	{
		for (i = 0; i < varsk; i++)
		{
			if (accepted_variants[i] == 0)
				continue;

			int GramForma, GramForma1, KamTip, KamTip1;

			if (variants_array[i].Zodynas == 2) //daiktavardziams reikia isanalizuoti GramForma
			{
				GramForma = variants_array[i].GramForma;
				KamTip = GramForma >> 8;
				GramForma = GramForma & 0xFF;
			}
			else
			{
				GramForma = variants_array[i].GramForma;
				KamTip = -1; //nedaiktavardziams KamTip neapibreztas
			}

			for (j = 0; j < varsk; j++)
			{
				if (accepted_variants[j] == 0)
					continue;

				if ((variants_array[i].KirtRaide != variants_array[j].KirtRaide) || (variants_array[i].Priegaide != variants_array[j].Priegaide))
				{

					if (variants_array[j].Zodynas == 2) //daiktavardziams reikia isanalizuoti GramForma
					{
						GramForma1 = variants_array[j].GramForma;
						KamTip1 = GramForma1 >> 8;
						GramForma1 = GramForma1 & 0xFF;
					}
					else
					{
						GramForma1 = variants_array[j].GramForma;
						KamTip1 = -1; //nedaiktavardziams KamTip neapibreztas
					}

					for (f = 0; f < rules2use; f++)
					{
						if ((auto_rules[f][0] == variants_array[i].Zodynas) &&
							((auto_rules[f][1] == -1) || (auto_rules[f][1] == GramForma)) &&
							((auto_rules[f][2] == -1) || (auto_rules[f][2] == KamTip)) &&
							(auto_rules[f][3] == variants_array[j].Zodynas) &&
							((auto_rules[f][4] == -1) || (auto_rules[f][4] == GramForma1)) &&
							((auto_rules[f][5] == -1) || (auto_rules[f][5] == KamTip1)))

						{
							accepted_variants[j] = 0;
							new_varsk--;

							break;
						}
					}
				}
			}
		}
	}
	else
		return 1;

	j = 0;
	for (i = 0; i < varsk; i++)
	{
		if (accepted_variants[i] == 0)
			continue;

		variants_array[j] = variants_array[i];

		j++;
	}

	//Dar karta patikrinam, ar visi variantai kirciuojami vienodai.
	yra_skirtingu_var = 0;
	for (i = 1; i < new_varsk; i++)
	{
		if ((variants_array[i - 1].KirtRaide != variants_array[i].KirtRaide) || (variants_array[i - 1].Priegaide != variants_array[i].Priegaide))
		{
			yra_skirtingu_var = 1; //true;
			break;
		}
	}

	if (yra_skirtingu_var == 0)
		return 1;
	else
		return new_varsk;
}
//------------------------------------------------------------
int KircTranskr(char *eil, char *TrZodis, int TrEilIlg, unsigned short *unitsR, unsigned short *unitsRNextSep,
				int *unitsLet, int *letPos, int rules2use)
{
	char SkPb[ILGIS1], Kirt[ILGIS1], Trmp[ILGIS1], eilute[ILGIS1];
	int i, j;

	int letPos1[ILGIS1];

	char frazesPab = FrazesPabaiga(eil);

	// skiemenu pabaigu ir kircio pozymiu uzpildymas
	for (i = 0; i < ILGIS1 - 1; i++)
	{
		SkPb[i] = 1;
		Kirt[i] = -1;
		Trmp[i] = 0;
	}

	// kircio zenklu, zodziu pabaigu kodavimas, XWQ keitimas
	eilute[0] = '_';
	//ismetam visus pradzioje esancius simbolius
	i = 0;
	while (strchr("`^~- ", eil[i]) && (eil[i] != 0) && (i < ILGIS1))
		i++;
	j = 1;
	while ((eil[i] != 0) && (i < ILGIS1))
	{
		switch (eil[i])
		{
		case 'W':
			eilute[j] = 'V';
			break;
		case 'Q':
			eilute[j] = 'K';
			break;
		case 'X':
			eilute[j] = 'K';
			letPos1[j - 1] = letPos[i];
			eilute[++j] = 'S';
			break;
		case '`':
			j--;
			Kirt[j] = 0;
			Trmp[j] = 1;
			break;
		case '^':
			j--;
			Kirt[j] = 1;
			Trmp[j] = 0;
			break;
		case '~':
			j--;
			Kirt[j] = 2;
			Trmp[j] = 0;
			break;
		case '-':
			j--;
			if (SkPb[j] & 1)
				SkPb[j]++;
			break;
		case ' ':
			eilute[j] = ' ';
			while (strchr(" ", eil[i + 1]) && (eil[i + 1] != 0) && (i < ILGIS1))
				i++;
			SkPb[j - 1] += 8;
			break; //8 reiskia zodzio pabaiga
		default:
			eilute[j] = eil[i];
		}
		letPos1[j - 1] = letPos[i];
		i++;
		if (j < ILGIS1)
			j++;
	}

	while (eilute[j - 1] == ' ')
		j--;
	eilute[j] = 0;
	letPos1[j - 1] = letPos[i];
	SkPb[j] = 0;

	// skiemenavimas
	skiem(eilute, SkPb);

	// kirciavimas ir transkribavimas
	variantas Variant[VARSK1];
	int m, varsk;
	int Kirciuota;
	char *kz, *ez, *dz, *newpos;

	// kirciavimas ir nekirciuojamu zodziu paieska
	ez = "_";
	dz = strtokf(&eilute[1], " ", &newpos);
	if (dz != NULL)
		do
		{
			kz = ez;
			ez = dz;
			dz = strtokf(NULL, " ", &newpos);
			if (dz == NULL)
				dz = "_";

			Kirciuota = 0;
			j = ez - eilute;
			for (int ij = j + strlen(&eilute[j]) - 1; ij >= j; ij--)
			{
				if (Kirt[ij] != -1)
				{
					if (Kirciuota == 0)
					{
						Kirciuota = 1;
					}
					else
					{
						Kirt[ij] = -1;
					} //paliekam tik viena kircio zenkla zodyje
				}
			}

			if (Kirciuota == 0)
			{
				m = ArKirciuoti(kz, ez, dz);
				if ((m == 1) && (strlen(ez) < ZODIL1)) // bandom kirciuoti tik zodzius, trumpesnius uz 50 simb.
				{
					m = Kirciuoti(ez, &SkPb[ez - eilute - 1], Variant);
					if (m > VARSK1 - 1)
						m = VARSK1 - 1;
					varsk = VienasVarKirc1(Variant, m);

					if (varsk > 1)
						varsk = auto_rules_function(Variant, varsk, rules2use);

					//Jei keli variantai, tai atsitiktinai parenkam tik tuo atveju, jei naudojamos visos taisykles
					if ((varsk == 1) || ((varsk > 1) && (rules2use == total_auto_rules)))
					{
						i = 0;
						while ((i < varsk) && (Variant[i].Zodynas == 0))
							i++; //grazinam daiktavardi, o ne veiksmazodi
						if (i == varsk)
							i = 0;

						Kirt[ez - eilute - 1 + Variant[i].KirtRaide] = Variant[i].Priegaide;
						strncpy(&SkPb[ez - eilute - 1], Variant[i].Skiem, strlen(ez));
						TarptautF(ez, &Trmp[ez - eilute], Variant[i].Tarpt);
					}
					else
						TarptautF(ez, &Trmp[ez - eilute], 0);
				}
			}
		} while (dz[0] != '_');

	// Skiemenu pozymiu nustatymas
	j = strlen(SkPb);
	for (i = j - 2; i >= 0; i--)
		if (SkPb[i] & 2)
			if (SkPb[i + 1] & 2)
				SkPb[i + 1] += 4;
			else
				SkPb[i + 1] += 3;

	// Kircio pozymiu nustatymas
	//Kirt 1-nek,2-tr,4-des,8-gal,16-kirtis 1 s i des .
	for (i = 1; i < j; i++)
	{
		if (Kirt[i] == 2)
			Kirt[i - 1] = 16;
		Kirt[i] = (Kirt[i] == -1) ? 1 : (Kirt[i] == 0) ? 2 : (Kirt[i] == 1) ? 4 : 8;
	}

	if (eilute[1] == ' ')
		eilute[1] = 0;

	return transkr(eilute, Kirt, SkPb, Trmp, TrZodis, TrEilIlg, unitsR, unitsRNextSep, unitsLet, letPos1);
}



#define TEXTBUFSIZE 10000


//------------------------------------------------------------
int KircTranskrAlt(char *eil, int *letPos, int rules2use)
{
	char SkPb[ILGIS1], Kirt[ILGIS1], Trmp[ILGIS1], eilute[ILGIS1];
	int i, j;

	int letPos1[ILGIS1];

	char frazesPab = FrazesPabaiga(eil);

	// skiemenu pabaigu ir kircio pozymiu uzpildymas
	for (i = 0; i < ILGIS1 - 1; i++)
	{
		SkPb[i] = 1;
		Kirt[i] = -1;
		Trmp[i] = 0;
	}

	// kircio zenklu, zodziu pabaigu kodavimas, XWQ keitimas
	eilute[0] = '_';
	//ismetam visus pradzioje esancius simbolius
	i = 0;
	while (strchr("`^~- ", eil[i]) && (eil[i] != 0) && (i < ILGIS1))
		i++;
	j = 1;
	while ((eil[i] != 0) && (i < ILGIS1))
	{
		switch (eil[i])
		{
		case 'W':
			eilute[j] = 'V';
			break;
		case 'Q':
			eilute[j] = 'K';
			break;
		case 'X':
			eilute[j] = 'K';
			letPos1[j - 1] = letPos[i];
			eilute[++j] = 'S';
			break;
		case '`':
			j--;
			Kirt[j] = 0;
			Trmp[j] = 1;
			break;
		case '^':
			j--;
			Kirt[j] = 1;
			Trmp[j] = 0;
			break;
		case '~':
			j--;
			Kirt[j] = 2;
			Trmp[j] = 0;
			break;
		case '-':
			j--;
			if (SkPb[j] & 1)
				SkPb[j]++;
			break;
		case ' ':
			eilute[j] = ' ';
			while (strchr(" ", eil[i + 1]) && (eil[i + 1] != 0) && (i < ILGIS1))
				i++;
			SkPb[j - 1] += 8;
			break; //8 reiskia zodzio pabaiga
		default:
			eilute[j] = eil[i];
		}
		letPos1[j - 1] = letPos[i];
		i++;
		if (j < ILGIS1)
			j++;
	}

	while (eilute[j - 1] == ' ')
		j--;
	eilute[j] = 0;
	letPos1[j - 1] = letPos[i];
	SkPb[j] = 0;

	// skiemenavimas
	skiem(eilute, SkPb);

	// kirciavimas ir transkribavimas
	variantas Variant[VARSK1];
	int m, varsk;
	int Kirciuota;
	char *kz, *ez, *dz, *newpos;

	// kirciavimas ir nekirciuojamu zodziu paieska
	ez = "_";
	dz = strtokf(&eilute[1], " ", &newpos);
	if (dz != NULL)
		do
		{
			kz = ez;
			ez = dz;
			dz = strtokf(NULL, " ", &newpos);
			if (dz == NULL)
				dz = "_";

			Kirciuota = 0;
			j = ez - eilute;
			for (int ij = j + strlen(&eilute[j]) - 1; ij >= j; ij--)
			{
				if (Kirt[ij] != -1)
				{
					if (Kirciuota == 0)
					{
						Kirciuota = 1;
					}
					else
					{
						Kirt[ij] = -1;
					} //paliekam tik viena kircio zenkla zodyje
				}
			}

			if (Kirciuota == 0)
			{
				m = ArKirciuoti(kz, ez, dz);
				if ((m == 1) && (strlen(ez) < ZODIL1)) // bandom kirciuoti tik zodzius, trumpesnius uz 50 simb.
				{
					m = Kirciuoti(ez, &SkPb[ez - eilute - 1], Variant);
					if (m > VARSK1 - 1)
						m = VARSK1 - 1;
					varsk = VienasVarKirc1(Variant, m);

					if (varsk > 1)
						varsk = auto_rules_function(Variant, varsk, rules2use);

					//Jei keli variantai, tai atsitiktinai parenkam tik tuo atveju, jei naudojamos visos taisykles
					if ((varsk == 1) || ((varsk > 1) && (rules2use == total_auto_rules)))
					{
						i = 0;
						while ((i < varsk) && (Variant[i].Zodynas == 0))
							i++; //grazinam daiktavardi, o ne veiksmazodi
						if (i == varsk)
							i = 0;

						Kirt[ez - eilute - 1 + Variant[i].KirtRaide] = Variant[i].Priegaide;
						strncpy(&SkPb[ez - eilute - 1], Variant[i].Skiem, strlen(ez));
						TarptautF(ez, &Trmp[ez - eilute], Variant[i].Tarpt);
					}
					else
						TarptautF(ez, &Trmp[ez - eilute], 0);
				}
			}
		} while (dz[0] != '_');

	// Skiemenu pozymiu nustatymas
	j = strlen(SkPb);
	for (i = j - 2; i >= 0; i--)
		if (SkPb[i] & 2)
			if (SkPb[i + 1] & 2)
				SkPb[i + 1] += 4;
			else
				SkPb[i + 1] += 3;

	// Kircio pozymiu nustatymas
	//Kirt 1-nek,2-tr,4-des,8-gal,16-kirtis 1 s i des .
	for (i = 1; i < j; i++)
	{
		if (Kirt[i] == 2)
			Kirt[i - 1] = 16;
		Kirt[i] = (Kirt[i] == -1) ? 1 : (Kirt[i] == 0) ? 2 : (Kirt[i] == 1) ? 4 : 8;
	}

	if (eilute[1] == ' ')
		eilute[1] = 0;

	char a = eilute[0];
	char k = Kirt[0];
	char s = SkPb[0];
	char t = Trmp[0];
	int l = letPos1[0];

	return 0;
}


////////////Pagrindine sintezavimo funkcija////////////////////////////////////////////////////////////////////////////////
int synthesizeWholeTextAlt(char *tekstas)
{
	int bufsize = TEXTBUFSIZE;
	char *normtextbuf = NULL;
	int *letPos = NULL;
	int lll = strlen(tekstas) + 1;
	if (bufsize < lll)
		bufsize = lll + 1;
	unsigned int ib = 0;
	int evnr = 0;
	int hr = NO_ERR;
	
	if (hr == NO_ERR)
	{
		normtextbuf = (char *)malloc(bufsize);
		if (normtextbuf == NULL)
		{
			hr = ERROR_LITHUSS_MEMORY_ALLOCATION;
		}
	}

	if (hr == NO_ERR)
	{
		letPos = (int *)malloc(bufsize * sizeof(int));
		if (letPos == NULL)
		{
			hr = ERROR_LITHUSS_MEMORY_ALLOCATION;
		}
	}

	if (hr == NO_ERR)
	{
		int retval = -1;
		int itcount = 0;
		while ((retval != NO_ERR) && (itcount < 5) && (hr == NO_ERR))
		{
			for (int jj = 0; jj < lll; jj++)
				letPos[jj] = jj;
			letPos[lll] = 0;

			retval = normalizeText(tekstas, normtextbuf, bufsize, letPos);
			if (retval != NO_ERR)
			{
				bufsize = bufsize * 2;
				normtextbuf = (char *)realloc(normtextbuf, bufsize);
				letPos = (int *)realloc(letPos, bufsize * sizeof(int));
				if ((normtextbuf == NULL) || (letPos == NULL))
				{
					//				spausdinti_loga("Nepavyko padidinti atminties normalizuotam tekstui arba raidziu poziciju masyvui");
					hr = ERROR_LITHUSS_MEMORY_REALLOCATION;
				}
				itcount++;
			}
		}
		if (itcount >= 5)
			hr = retval;
	}

	if (hr == NO_ERR)
	{
		char *pos = normtextbuf;
		char sakinys[200], TrSakinys[500];
		int n;

		while ((pos != (void*)1) && (hr == NO_ERR))
		{
			int hr2 = 0;
			int lp = (int)(pos - normtextbuf);
			n = sscanf(pos, "%[^\n]", sakinys);
			pos = strchr(pos, '\n') + 1;
			if (n < 0)
				break;
			if (n == 0)
				sakinys[0] = 0; //arba if(n == 0) continue; apsauga nuo tusciu eiluciu \n

			unsigned short unitsRows[128];
			unsigned short unitsRowsNextSeparators[128];
			int unitsLet[128];
			for (int ii = 0; ii < 128; ii++)
			{
				unitsRows[ii] = 0;
				unitsRowsNextSeparators[ii] = 0;
				unitsLet[ii] = 0;
			}

			int rules2use = 1155 * 75 / 100; //75% total_auto_rules
			if (strcmp(sakinys, " ") == 0)
				sakinys[0] = 0; //jei eilute tuscia arba tik neskaitytini simboliai

			int unitsRowsLength = KircTranskrAlt(sakinys, &letPos[lp], rules2use);
			hr2 = (unitsRowsLength <= 2);

			//cia galim modifikuoti TrSakinys

			if (hr2 == 0)
			{
				hr = ERROR_LITHUSS_EVENTS_ARRAY_OVERFLOW;
				break;
			}
		} //while pabaiga
	}	 //if(hr == 0) pabaiga

	if (letPos != NULL)
	{
		free(letPos);
		letPos = NULL;
	}

	return hr;
}

}