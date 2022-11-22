#!/usr/bin/env python3


# -----------------------------------------------------------------------------
""" This MODULE contains the data structures and implementation for the string
    matching problem (i.e. finding the first occurrence of a pattern in a
    sequence of chars).
""" # -------------------------------------------------------------------------

__author__ = '@kaethis'

__version__ = '1.0'


from typing import Dict


class AlgorithmInvalidError(Exception): # -------------------------------------
    """ This EXCEPTION is RAISED when a chosen algorithm is invalid.
    """ # ---------------------------------------------------------------------

    def __init__(self, algm: int):

        super().__init__("chosen algorithm is invalid: '{}'".format(algm))


class StringMatcher(): # ------------------------------------------------------
    """ This CLASS represents an implementation for string match, whereby its
        behavior depends on the algorithm chosen for the string matching
        problem.

        Each iteration of the algorithm ensues by calling its step() function.
    """ # ---------------------------------------------------------------------

    ALGM_BRUTEFORCE = 1

    ALGM_HORSPOOL = 2

    ALGM_BOYERMOORE = 3


    def __init__(self, seq: str, ptn: str, algm: int): # ----------------------
        """ This CONSTRUCTOR ...
        """ # -----------------------------------------------------------------

        self.seq = seq              # Sequence of n chars.

        self.n = len(seq)           # Number of chars in sequence.

        self.ptn = ptn              # Pattern of m chars to attempt match with
                                    # first occurrence in sequence.

        self.m = len(ptn)           # Number of chars in pattern.

        self.k = 0                  # Number of chars matched.

        self.bsyms = {}             # Bad-symbol table containing char c (as
                                    # key) and corresponding shift distance (as
                                    # value).

        self.gsufs = {}             # Good-suffix table containing length of
                                    # suffix (as key) and corresponding shift
                                    # distance (as value).

        self.i = 0                  # Index of char comparison in sequence.

        self.match_i = -1           # Index of first occurrence of pattern
                                    # matched in sequence (or -1 if no match).

        self.step_n = 0             # Number of steps ensued by algorithm. 

        self.algm = algm            # Algorithm chosen for the string matching
                                    # problem.


        self.algms = {\
            StringMatcher.ALGM_BRUTEFORCE : self.bruteforce,\
            StringMatcher.ALGM_HORSPOOL   : self.horspool,\
            StringMatcher.ALGM_BOYERMOORE : self.boyermoore\
        }

        # Validate algorithm chosen for string matching problem is defined:

        if self.algm not in self.algms.keys():

            raise AlgorithmInvalidError(algm)


        if (self.algm == StringMatcher.ALGM_HORSPOOL)\
            or (self.algm == StringMatcher.ALGM_BOYERMOORE):

            # If string match algorithm is Horspool or Boyer-Moore, index of
            # char comparison in sequence is end of pattern.  Also, precompute
            # bad-symbol shift distances and store them in table:

            self.i = (self.m - 1)

            self.bsyms = generateBadSymbolTable(self.seq, self.ptn)

            if (self.algm == StringMatcher.ALGM_BOYERMOORE):

                # If string match algorithm is Boyer-Moore, precompute good-
                # suffix shift distances and store them in table.

                self.gsufs = generateGoodSuffixTable(self.ptn)


    def step(self) -> bool: # -------------------------------------------------
        """ This FUNCTION ensues a single step performed by algorithm chosen
            for string matching problem and returns whether or not algorithm is
            complete.

            NOTE: If pattern matched in sequence, match_i contains index of
                  first occurrence matched in sequence (or -1 if no match).
        """ # -----------------------------------------------------------------

        is_done = self.algms[self.algm]()   # Ensue single step.

        self.step_n += 1                    # Increment number of steps ensued
                                            # by algorithm.


        return is_done


    def bruteforce(self) -> bool: # -------------------------------------------
        """ This FUNCTION ensues a single step performed by bruteforce string
            match algorithm and returns whether or not algorithm is complete.
            
            NOTE: If pattern matched in sequence, match_i contains index of
                  first occurrence matched in sequence (or -1 if no match).
        """ # -----------------------------------------------------------------

        if (self.i <= (self.n - self.m - 1)):


            seq_i, ptn_i = (self.i + self.k), self.k

            if (self.k < self.m) and (self.seq[seq_i] == self.ptn[ptn_i]):

                # If number of chars matched less than length of pattern and
                # char at (i + k) in sequence matches char at k in pattern,
                # increment number of chars matched.

                self.k += 1

            else:

                if (self.k == self.m):

                    # If number of chars matched equals number of chars in
                    # pattern, pattern matched in sequence; capture index of
                    # first occurrence.

                    self.match_i = self.i


                    return True     # Indicate algorithm complete (w/ match).

                else:

                    # Otherwise, mismatch occurred; reset number of chars
                    # matched and increment index of char comparison.

                    self.k = 0

                    self.i += 1


            return False        # Indicate algorithm incomplete.

        else:

            return True         # Indicate algorithm complete (w/ no match).


    def horspool(self) -> bool: # ---------------------------------------------
        """ This FUNCTION ensues a single step performed by Horspool string
            match algorithm and returns whether or not algorithm is complete.
            
            NOTE: If pattern matched in sequence, match_i contains index of
                  first occurrence matched in sequence (or -1 if no match).
        """ # -----------------------------------------------------------------
            
        if (self.i <= (self.n - 1)):


            seq_i, ptn_i = (self.i - self.k), (self.m - 1 - self.k) 

            if (self.k < self.m) and (self.seq[seq_i] == self.ptn[ptn_i]):

                # If number of chars matched less than length of pattern and
                # char at (i - k) in sequence matches char at (m - 1 - k) in
                # pattern, increment number of chars matched.

                self.k += 1

            else:

                if (self.k == self.m):

                    # If number of chars matched equals number of chars in
                    # pattern, pattern matched in sequence; capture index of
                    # first occurrence.

                    self.match_i = (self.i - self.m + 1)

 
                    return True;    # Indicate algorithm complete (w/ match).

                else:

                    # Otherwise, mismatch occurred; reset number of chars
                    # matched and increment index of char comparison by
                    # corresponding shift distance of char comparison from bad-
                    # symbol table:

                    self.k = 0

                    self.i += self.bsyms[self.seq[self.i]]


            return False        # Indicate algorithm incomplete.
            
        else:

            return True         # Indicate algorithm complete (w/ no match).


    def boyermoore(self) -> bool: # -------------------------------------------
        """ This FUNCTION ensues a single step performed by Boyer-Moore string
            match algorithm and returns whether or not algorithm is complete.
            
            NOTE: If pattern matched in sequence, match_i contains index of
                  first occurrence matched in sequence (or -1 if no match).
        """ # -----------------------------------------------------------------
        
        if (self.i <= (self.n - 1)):


            seq_i, ptn_i = (self.i - self.k), (self.m - 1 - self.k) 

            if (self.k < self.m) and (self.seq[seq_i] == self.ptn[ptn_i]):

                # If number of chars matched less than length of pattern and
                # char at (i - k) in sequence matches char at (m - 1 - k) in
                # pattern, increment number of chars matched.

                self.k += 1

            else:

                if (self.k == self.m):

                    # If number of chars matched equals number of chars in
                    # pattern, pattern matched in sequence; capture index of
                    # first occurrence.

                    self.match_i = (self.i - self.m + 1)

 
                    return True;    # Indicate algorithm complete (w/ match).

                else:

                    # Otherwise, mismatch occurred ...

                    if (self.k == 0):

                        # If no chars matched, increment index of char
                        # comparison by corresponding shift distance of char
                        # comparison from bad-symbol table.

                        d = self.bsyms[self.seq[self.i]]

                    else:

                        # If (0 < k < m) chars matched, retrieve corresponding
                        # shift distance t1 of mismarch char c from bad-symbol
                        # table and corresponding shift distance d2 of length
                        # of suffix k from good-suffix table:

                        t1 = self.bsyms[self.seq[self.i - self.k]]

                        d2 = self.gsufs[self.k]

                        # Increment index of char comparison by max(d1, d2),
                        # where d1 = max((t1 - k), 1):

                        d1 = max((t1 - self.k), 1)

                        d = max(d1, d2)


                    # Reset number of chars matched and increment index of char
                    # comparison by shift distance determined by conditionals:

                    self.k = 0

                    self.i += d


            return False        # Indicate algorithm incomplete.
            
        else:

            return True         # Indicate algorithm complete (w/ no match).


def generateBadSymbolTable(seq: str, ptn: str) -> Dict[str, int]: # ----------
    """ This FUNCTION generates bad-symbol table for the alphabet of a sequence
        of n chars and a pattern of m chars containing char c (as key) and
        corresponding shift distance (as value) utilized by Horspool and
        Boyer-More string matching algorithms.
    """ # ---------------------------------------------------------------------

    bsyms = {}

    n, m = len(seq), len(ptn)


    # Any char c not among the first (m-1) chars in pattern has shift distance
    # of pattern length:

    for i in range(n):

        c = seq[i]

        bsyms[c] = m


    # Otherwise, char c has shift distance from rightmost occurrence of c among
    # the first (m-1) chars in pattern to last char in pattern:

    # NOTE: A char in pattern that does not exist in sequence guarantees match
    #       will not occur.  For the purpose of this exercise, we will ignore
    #       this fact and include non-existing chars from pattern to alphabet
    #       in bad-symbol table.

    for j in range(m - 1):

        c = ptn[j]

        bsyms[c] = (m - 1 - j)


    return bsyms


def generateGoodSuffixTable(ptn: str) -> Dict[int, int]: # --------------------
    """ This FUNCTION generates good-suffix table for a pattern of m chars
        containing length of suffix (as key) and corresponding shift distance
        (as value) utilized by Boyer-Moore string matching algorithm.
    """ # ---------------------------------------------------------------------

    gsufs = {}

    m = len(ptn)


    for k in range(1, m):

        d = -1      # Distance b/w suffix and occurrence in prefix.
        

        # Scan chars in pattern prefix preceeding suffix at (m - k) from right
        # to left for rightmost occurrence of suffix not preceeded by the same
        # char as suffix:

        for i in range((m - k - 1), -1, -1):

            t = 0       # Number of chars matching suffix in prefix.

            for j in range(k):

                if (ptn[i + j] == ptn[m - k + j]):

                    t += 1


            if (t == k):

                # If occurrence of suffix found in prefix...
           
                if (i == 0) or (ptn[i - 1] != ptn[m - k - 1]):

                    # If occurrence of suffix not preceeded by any char (i.e.
                    # occurs at beginning of prefix) or not same exact char as
                    # suffix, calculate distance b/w suffix and occurrence in
                    # prefix and break:
            
                    d = (m - k - i)

                    break


        if (d == -1):

            # If no occurrence of suffix not preceeded by same char, scan chars
            # at beginning of prefix from left to right for largest occurrence
            # of suffix:

            t_max = 0   # Largest number of chars matching suffix in prefix.

            for i in range(k):
            
                t = 0

                is_mismatch = False     # Whether or not mismatch occurred.

                for j in range(i + 1):

                    if (ptn[m - 1 - i + j] == ptn[j]):

                        t += 1

                    else:

                        # If mismatch occurs, no futher evaluation; break.

                        is_mismatch = True

                        break


                if not is_mismatch and (t > t_max):
                    
                    # If at least partial occurrence of suffix at beginning of
                    # prefix and number of matching chars is greater than known
                    # largest, capture new largest number of matching chars.

                    t_max = t


            # Calculate distance b/w suffix and largest occurrence in prefix.
            # Note that if no match occurred, shift distance is pattern length.

            d = (m - t_max)


        gsufs[k] = d


    return gsufs
