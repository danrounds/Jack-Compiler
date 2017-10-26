backEnd/ is the part of the compiler that outputs code and does syntax/semantic
checks.

Files here:
--------------------------------------------------------------------------------
* _functionTableDataAndTypes.py
  Internal data structures for the functionsInfo portion of our SymbolTable

* doesFunctionReturn.py
  A heuristic that does a decent job of telling us whether a function is likely
  to return (no, I didn't solve the halting problem)

* OutputSetup.py
  Class that defines our file output object

* processCode.py
  The set of functions we call during our second parse to actually output VM
  code

* returnSemantics.py
  Does limited semantic checking on function returns. Makes sure void functions
  don't return values, non-void functions /do/ return values, that constructors
  return a `this`. Doesn't go as far as type-checking returned expressions.

* setGlobals.py
  Dispatches variable changes to the modules that need them. Sets "context"
  variables, for our parse: `parseNum`, `currentClass`, `currentFn`,
  `currentFnType`.

* SymbolTable
  Two Classes, defining two objects that we use to get info on variables and
  functions. The function table relies on the variable one. They could be
  split into multiple modules, but for now they're together.
