## CS 2040 - Algorithms I
**Assignment #5:** String Matching; Bruteforce, Horspool and Boyer-Moore

**Author:** Matt W. Martin

### About

This program ...

---
### Contents
The contents of this repository include the following files:
```
./
    README.md       # this file
    driver.py       # for executing the program
    example1.txt    # quote from Morpheus in "The Matrix" (1999)
    file1.txt       # sequence provided by professor (pattern is "abracadabra")
    file2.txt       # sequence provided by professor (pattern is "hat_that")
    file3.txt       # sequence provided by professor (pattern is "ABCABAB")
    strmatch.py     # implementation and data structures for string match
    util.py         # helper functions
```

---
### Dependencies
This program requires the following modules from the Python 3.10 standard library:
```
argparse    # parser for command-line options, args and sub-commands
curser      # terminal handling for character-cell displays
dataclasses # structured classes for storing data
math        # mathematical functions (namely, ceil)
os          # misc operating system interfaces (namely, file i/o)
time        # time access and conversions (namely, sleep)
typing      # support for type hints
```

---
### Instructions
Program execution instructions can be found by entering `python3 driver.py --help`:
```
usage: driver.py [-h] [--algm ALGORITHM] PATH PATTERN

This PROGRAM features an implementation for string match using bruteforce,
Horspool or Boyer-Moore as its string matching algorithm.

positional arguments:
  PATH              path to file containing sequence of n chars
  PATTERN           pattern of m chars to attempt match with first occurrence
                    in sequence

options:
  -h, --help        show this help message and exit
  --algm ALGORITHM  chosen algorithm for string matching problem (BRUTEFORCE,
                    HORSPOOL or BOYERMOORE) (default is BRUTEFORCE algorithm)

~created by @kaethis
```
A path to a file containing a sequence of chars is provided as first positional command-line argument `PATH` followed by a pattern of chars as second positional argument `PATTERN` (if `PATTERN` contains whitespace characters, use quotation marks surrounding argument).  The algorithm chosen for the string matching problem is specified using the `--algm ALGORITHM` option, whereby `ALGORITHM` can be `BRUTEFORCE`, `HORSPOOL` or `BOYERMOORE` (`BRUTEFORCE` is used by default if no algorithm specified).

---
### Links
Here are some resources I found useful when developing this program:
- [dataclasses — Data Classes](https://docs.python.org/3/library/dataclasses.html) Data Classes (introduced in Python 3.7) are analogous to Structures (structs) in C; especially useful for data representations that don't require their own set of functions or constructor.
