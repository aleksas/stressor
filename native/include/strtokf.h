#include <string.h>

/*
 * Standard C string function: tokenize a string splitting based on a
 * list of separator characters. Reentrant version.
 *
 * The "context" argument should point to a "char *" that is preserved
 * between calls to strtok_r that wish to operate on same string.
 */

extern "C" {
char* strtokf(char *string, const char *seps, char **context);
}