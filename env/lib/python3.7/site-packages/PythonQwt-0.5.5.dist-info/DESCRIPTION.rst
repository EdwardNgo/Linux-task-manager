The ``PythonQwt`` package is a 2D-data plotting library using Qt graphical 
user interfaces for the Python programming language. It is compatible with 
both ``PyQt4`` and ``PyQt5`` (``PySide`` is currently not supported but it
could be in the near future as it would "only" requires testing to support 
it as a stable alternative to PyQt).

The ``PythonQwt`` project was initiated to solve -at least temporarily- the 
obsolescence issue of `PyQwt` (the Python-Qwt C++ bindings library) which is 
no longer maintained. The idea was to translate the original Qwt C++ code to 
Python and then to optimize some parts of the code by writing new modules 
based on NumPy and other libraries.

The ``PythonQwt`` package consists of a single Python package named `qwt` 
which is a pure Python implementation of Qwt C++ library with some 
limitations: efforts were concentrated on basic plotting features, leaving 
higher level features to the `guiqwt` library.

