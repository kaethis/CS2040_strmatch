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
    qselect.py      # implementation and data structures for string match
    util.py         # helper functions
    example1.txt    # quote from Morpheus in "The Matrix" (1999)
```

---
### Dependencies
This program requires the following modules from the Python 3.10 standard library:
```
argparse    # parser for command-line options, args and sub-commands
curser      # terminal handling for character-cell displays
dataclasses # structured classes for storing data
match       # mathematical functions (namely, ceil)
os          # misc operating system interfaces (namely, file i/o)
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

---
### Links
Here are some resources I found useful when developing this program:
- [dataclasses — Data Classes](https://docs.python.org/3/library/dataclasses.html) Data Classes (introduced in Python 3.7) are analogous to Structures (structs) in C and are especially useful for data representation that don't require their own set of functions or constructor.
