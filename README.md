## CS 2040 - Algorithms I
**Assignment #5:** String Matching; Bruteforce, Horspool and Boyer-Moore

**Author:** Matt W. Martin

### About

This program features several implementations for [string-searching](https://en.wikipedia.org/wiki/String-searching_algorithmhttps://en.wikipedia.org/wiki/String-searching_algorithm) using a naive bruteforce approach, [Horspool's algorithm](https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore%E2%80%93Horspool_algorithm) or the [Boyer-Moore string matching algorithm](https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore_string-search_algorithm) in attempt to match a pattern with its first occurrence in a sequence of characters.

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
This program was developed using Python 3.10.6 and requires the following modules from the Python 3.10 standard library:
```
argparse        # parser for command-line options, args and sub-commands
curser          # terminal handling for character-cell displays
dataclasses     # structured classes for storing data
math            # mathematical functions (namely, ceil)
os              # misc operating system interfaces (namely, file i/o)
time            # time access and conversions (namely, sleep)
typing          # support for type hints
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
A path to a file containing a sequence of chars is provided as first positional command-line argument `PATH` followed by a pattern of chars as second positional argument `PATTERN` (if `PATTERN` contains whitespace characters, use quotation marks surrounding argument).  The algorithm chosen for the string matching problem is specified using the `--algm ALGORITHM` option, whereby `ALGORITHM` can be `BRUTEFORCE`, `HORSPOOL` or `BOYERMOORE` (`BRUTEFORCE` is used by default if no algorithm specified).  Proceed with each ensuing step in the algorithm by pressing any key on the keyboard.

For example, the program will attempt to match with the first occurrence of the pattern *and, and* in a sequence of chars from file *example1.txt* using the *default algorithm* by entering `python3 driver.py example1.txt "and, and"`.

Each char in the pattern will be aligned below the sequence of chars at the beginning of the sequence.  If a char in the pattern matches with a corresponding char in the sequence, that char will be highlighted green before proceeding with the next comparison.  If the pattern matches with an occurrence in the sequence, a match has been found and the program will terminate; otherwise, the pattern will shift by a single character and resume comparisons until no remaining chars are left in the sequence.

https://user-images.githubusercontent.com/8784297/203253076-d0aa7696-bab3-4806-a500-764882ab1cbf.mp4

Alternatively, the program will attempt to match the pattern *and, and* in a sequence of chars from file *example1.txt* using *Horspool's string matching algorithm* by entering `python3 driver.py example1.txt "and, and" --algm HORSPOOL`.

A shift table of distances and corresponding chars from the alphabet used by the pattern and sequence is displayed above the sequence of chars.  The char in the sequence aligned with the end of the pattern is highlighted blue in the shift table.  If a mismatch occurs, the pattern is shifted by the distance of the corresponding char aligned with the end of the pattern.  Comparisons resume after each time the pattern is shifted until the pattern matches with an occurrence or no more remaining chars are left in the sequence.

https://user-images.githubusercontent.com/8784297/203253144-271cc296-3f2b-48d1-a291-a23e6d624e56.mp4

Finally, the program will attempt to match the pattern *and, and* in a sequence of chars from file *example1.txt* using the *Boyer-Moore string matching algorithm* by entering `python3 driver.py example1.txt "and, and" --algm BOYERMOORE`.

Similar to Horspool's algorithm, a bad-symbol table of shift distances and corresponding chars from the alphabet, in addition to a good-suffix table of shift distances and corresponding length of the suffix, are displayed above the sequence of chars.  One or more chars in the pattern that match with chars in the sequence, called the suffix, are highlighted green and its length is highlighted blue in the good-suffix table.  The char undergoing comparison in the sequence is highlighted blue in the bad-symbol table.  If a mismatch occurs with no suffix, the pattern is shifted by the distance of the corresponding char aligned with the end of the pattern from the bad-symbol table (same as Horspool's algorithm).

If a mismatch occurs and `0 < k < m` chars matched, whereby `k` is the length of the suffix and `m` is the length of the pattern, the pattern is shifted by `d` chars, whereby `d = max(d1, d2)`, `d1 = max((t1 - k), 1)`, `t1` is the shift distance of the corresponding char that caused the mismatch from the bad-symbol table and `d2` is the shift distance of the corresponding suffix length from the good-suffix table.  The distances in the bad-symbol table are displayed as `d1` to reflect these values in such cases.  Comparisons resume after each time the pattern is shifted until the pattern matches with an occurrence or no more remaining chars are left in the sequence.

https://user-images.githubusercontent.com/8784297/203253197-570d77e5-db83-4b7b-a1d7-cb7f9501eaa5.mp4

Upon terminating, the program will output `no occurrence of pattern in sequence` to the console if no match occurred.  Otherwise, the program outputs the index of the first occurrence of the pattern in the sequence of chars.  Regardless of the algorithm chosen or whether a match occurred, the program also outputs the number of steps ensued by the chosen algorithm as well as the steps enused by the other algorithms for the same pattern and sequence:
```
first occurrence of pattern 'and, and' at i=148 in sequence
BOYERMOORE  : 39 steps
BRUTEFORCE  : 167 steps
HORSPOOL    : 38 steps
```

---
### Links
Here are some resources I found useful when developing this program:
- [dataclasses — Data Classes](https://docs.python.org/3/library/dataclasses.html) Data Classes (introduced in Python 3.7) are analogous to Structures (structs) in C; especially useful for data representations that don't require their own set of functions or constructor.
