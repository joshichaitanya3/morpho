# Release notes for 0.6.3

We're pleased to announce Morpho 0.6.3, which contains a number of improvements and represents the first steps towards cross-platform compatibility.

## Additional finite elements

Morpho now provides finite element types beyond the linear Lagrangian elements (CG1) used previously. Quadratic Lagrangian elements (CG2) are implemented for fields on 1, 2 and 3D elements, and we will provide additional elements in future releases. Interpolated gradients are available for all element types.

## Preliminary Windows build

The Morpho library and terminal app now can be natively built on Windows using Clang. To enable this, Morpho has been significantly refactored to isolate platform-specific code in a single location.

We will provide a Windows installer and binaries in future releases once morphoview has also been ported.

## Self is not longer necessary for invocations

It is no longer required to use the `self` keyword to invoke a method call, i.e.

    self.foo() 

can be replaced with:

    foo() 

Local variables take precedence over method labels, so that

    var foo = "hi"
    foo() 

raises an error even if foo is a method in the same class. 

## Minor fixes

* Improvements to the adaptive quadrature routines, which now use better rules by default and report clearer error messages.
* Many improvements to the test suite, with tests more clearly structured.
* String parsing now unicode aware.
* AreaIntegral now supports an experimental option weightByReference, which weights the integral by a reference mesh, rather than the target mesh (this is useful for some elasticity problems).