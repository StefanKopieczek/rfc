RFC
===

Useful Python tool for viewing RFCs from the terminal.
Users can also store RFCs offline to view later,
or browse the RFC index to find the RFC they're interested in.

RFC is fully-featured and usable now.
However, there are still some rough edges to iron out -
in particular error cases are not very cleanly handled yet,
so they mostly just stacktrace :)

Platforms
---------
 * Windows
 * Linux
 * Mac
 
Installation
------------ 
1. Check out git@github.com:StefanKopieczek/rfc.git
2. Open a terminal or command prompt, and cd to the rfc directory.
3. Get [pip](https://pip.pypa.io/en/latest/installing.html) if you don't already have it.
4. Install `setuptools` with `pip install setuptools`.
5. Run `python setup.py install`.

You will now be able to call RFC from the command line in any folder, e.g. by typing `rfc 3261`.

Usage
-----

    rfc [view] RFC  - Display the specified RFC.
    rfc save   RFC  - Store the specified RFC so it can be viewed offline.
    rfc list        - Display all published RFCs in a table. Useful for grepping.
    rfc search TERM - Show all RFCs whose summary text contains the given term.
    rfc help        - Print this message.
