/** @file memory.h
 *  @author T J Atherton
 *
 *  @brief Morpho memory management
*/

#ifndef memory_h
#define memory_h

#include <stdio.h>
#include <stdlib.h>
#include "build.h"

/** Macro to redirect malloc through our memory management */
#define MORPHO_MALLOC(size) morpho_allocate(NULL, 0, size, __FILE__, __LINE__)

/** Macro to redirect free through our memory management */
#define MORPHO_FREE(x) morpho_allocate(x, 0, 0, __FILE__, __LINE__)

/** Macro to redirect realloc through our memory management */
#define MORPHO_REALLOC(x, size) morpho_allocate(x, 0, size, __FILE__, __LINE__)

void *morpho_allocate(void *old, size_t oldsize, size_t newsize, const char* filename, int linenum);

#endif /* memory_h */
