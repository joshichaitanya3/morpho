/** @file error.c
 *  @author T J Atherton
 *
 *  @brief Morpho memory management
*/

#include <stdio.h>
#include "memory.h"
#include "dictionary.h"

#ifdef MORPHO_DEBUG_STRESSGARBAGECOLLECTOR
#include "morpho.h"
void vm_collectgarbage(vm *v);
#endif

/** @brief Generic allocator function
 *  @param old      A previously allocated pointer, or NULL to allocate new memory
 *  @param oldsize  The previously allocated size
 *  @param newsize  New size to allocate
 *  @returns A pointer to allocated memory, or NULL on failure.
 */
void *morpho_allocate(void *old, size_t oldsize, size_t newsize, const char* filename, int linenum) {
// [2/27/21] TJA: Disabled because Garbage collection should be triggered on binding, not on allocation.
//#ifdef MORPHO_DEBUG_STRESSGARBAGECOLLECTOR
//    if (newsize>oldsize) {
//        vm_collectgarbage(NULL);
//    }
//#endif

    #ifdef MORPHO_DEBUG_MEMORYLEAK
            printf("File %s, line = %d \n", filename, linenum);
    #endif
    if (newsize == 0) {
        if (old != NULL) {
            #ifdef MORPHO_DEBUG_MEMORYLEAK
                printf("Freeing pointer %p with size %d \n", old, oldsize);
            #endif
        }
        free(old);
        return NULL;
    }
    void* ptr = realloc(old, newsize);
    #ifdef MORPHO_DEBUG_MEMORYLEAK
        if (old != NULL) {
            printf("Freeing pointer %p with size %d \n", old, oldsize);
        }
        printf("Allocating pointer %p with size %d \n", ptr, newsize);
    #endif
    return ptr;
}

