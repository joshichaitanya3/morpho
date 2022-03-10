/** @file complex.h
 *  @author Danny Goldstein
 *
 *  @brief Veneer class over the objectcomplex type
 */

#ifndef complexobj_h
#define complexobj_h

#include <stdio.h>
#include "veneer.h"
#include <complex.h>



/* -------------------------------------------------------
 * Complex objects
 * ------------------------------------------------------- */

extern objecttype objectcomplextype;
#define OBJECT_COMPLEX objectcomplextype

typedef struct {
    object obj;
    double complex Z;
} objectcomplex;

/** Tests whether an object is a complex */
#define MORPHO_ISCOMPLEX(val) object_istype(val, OBJECT_COMPLEX)

/** Gets the object as an complex */
#define MORPHO_GETCOMPLEX(val)   ((objectcomplex *) MORPHO_GETOBJECT(val))

/** Creates a complex object */
objectcomplex *object_newcomplex(double real, double imag);

/** Creates a new complex from an existing complex */
objectcomplex *object_clonecomplex(objectcomplex *array);

/** Clones a value that holds a complex */
value object_clonecomplexvalue(value val);

bool complex_equality(objectcomplex *a, objectcomplex *b);
/* -------------------------------------------------------
 * Complex class
 * ------------------------------------------------------- */

#define COMPLEX_CLASSNAME                   "Complex"

#define COMPLEX_CONJUGATE_METHOD            "conj"
#define COMPLEX_ABS_METHOD                  "abs"
#define COMPLEX_REAL_METHOD                 "real"
#define COMPLEX_IMAG_METHOD                 "imag"
#define COMPLEX_ANGLE_METHOD                "angle"

#define COMPLEX_CONSTRUCTOR                "CmplxCns"
#define COMPLEX_CONSTRUCTOR_MSG            "Complex() constructor should be called with two floats"

#define COMPLEX_ARITHARGS                  "CmplxInvldArg"
#define COMPLEX_ARITHARGS_MSG              "Complex arithmetic methods expect a complex or number as their argument."

#define COMPLEX_INVLDNARG                  "CmpxArg"
#define COMPLEX_INVLDNARG_MSG              "Complex Operation did not exect those arguments."


/* -------------------------------------------------------
 * Complex interface
 * ------------------------------------------------------- */


void complex_copy(objectcomplex *a, objectcomplex *out);
void complex_add(objectcomplex *a, objectcomplex *b, objectcomplex *out);
void complex_sub(objectcomplex *a, objectcomplex *b, objectcomplex *out);
void complex_mul(objectcomplex *a, objectcomplex *b, objectcomplex *out);
void complex_div(objectcomplex *a, objectcomplex *b, objectcomplex *out);
void complex_conj(objectcomplex *a, objectcomplex *out);
void complex_abs(objectcomplex *a, double *out);
void complex_angle(objectcomplex *a, double *out);
void complex_print(objectcomplex *m);
void complex_initialize(void);
void complex_getreal(objectcomplex *c, double *value);
void complex_getimag(objectcomplex *c, double *value);

/* Built-in fucntions */
value complex_builtinexp(vm * v, objectcomplex* c);
value complex_builtinfabs(vm * v, objectcomplex* c);
value complex_builtinexp(vm * v, objectcomplex* c);
value complex_builtinlog(vm * v, objectcomplex* c);
value complex_builtinlog10(vm * v, objectcomplex* c);

value complex_builtinsin(vm * v, objectcomplex* c);
value complex_builtincos(vm * v, objectcomplex* c);
value complex_builtintan(vm * v, objectcomplex* c);
value complex_builtinasin(vm * v, objectcomplex* c);
value complex_builtinacos(vm * v, objectcomplex* c);

value complex_builtinsinh(vm * v, objectcomplex* c);
value complex_builtincosh(vm * v, objectcomplex* c);
value complex_builtintanh(vm * v, objectcomplex* c);
value complex_builtinsqrt(vm * v, objectcomplex* c);

value complex_builtinfloor(vm * v, objectcomplex* c);
value complex_builtinceil(vm * v, objectcomplex* c);

value complex_builtinisfinite(objectcomplex* c);
value complex_builtinisinf(objectcomplex* c);
value complex_builtinisnan(objectcomplex* c);

value complex_builtinatan(vm *v, value c);
value complex_builtinatan2(vm *v, value c1, value c2);

value Complex_getreal(vm *v, int nargs, value *args);
value Complex_getimag(vm *v, int nargs, value *args);
value Complex_angle(vm *v, int nargs, value *args);
value Complex_conj(vm *v, int nargs, value *args);

#endif /* complex_h */
