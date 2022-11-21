#!/usr/bin/env python3


# -----------------------------------------------------------------------------
""" This MODULE contains helper functions and data structures outside the scope
    of the problem domain.
""" # -------------------------------------------------------------------------

__author__ = '@kaethis'

__version__ = '1.0'


import curses

import os

from argparse import ArgumentTypeError

from dataclasses import dataclass

from math import ceil

from strmatch import StringMatcher


@dataclass
class CellDimensions: # -------------------------------------------------------
    """ This DATA CLASS ...
    """ # ---------------------------------------------------------------------

    height: int

    width: int

    margin: int = 0         # Number of ws chars b/w cells.

    col_max: int = 0        # Max possible number of cells per col.

    row_max: int = 0        # Max possible number of cells per row.

    col_n: int = 0          # Number of cells per column.

    row_n: int = 0          # Number of cells per row.


@dataclass
class WindowDimensions: # -----------------------------------------------------
    """ This DATA CLASS ...
    """ # ---------------------------------------------------------------------

    y: int

    x: int

    padding: int            # Number of ws chars b/w window border and cells.

    margin: int             # Number of ws chars outside window border.

    cell_n: int             # Total number of cells in window.

    title: str

    height: int = 0       

    width: int = 0 

    y_max: int = 0          # Max possible y-position of window.

    x_max: int = 0          # Max possible x-position of window.


class Window(): # -------------------------------------------------------------
    """ This CLASS ...
    """ # ---------------------------------------------------------------------

    def __init__(\
            self,\
            stdscr,\
            scr_ymax: int,\
            scr_xmax: int,\
            win_y: int,\
            win_x: int,\
            cell_n: int,\
            win_title: str,\
            win_padding: int = 2,\
            win_margin: int = 1,\
            cell_height: int = 2,\
            cell_width: int = 2,\
            cell_margin: int = 1,\
            is_flscr: bool = False\
        ): # ------------------------------------------------------------------
        """ This CONSTRUCTOR ...
        """ # -----------------------------------------------------------------
        
        self.wdim = WindowDimensions(\
            win_y,\
            win_x,\
            win_padding,\
            win_margin,\
            cell_n,\
            win_title\
        )

        self.wdim.y_max = (scr_ymax - self.wdim.y - (self.wdim.padding * 2))

        self.wdim.x_max = (scr_xmax - self.wdim.x - (self.wdim.padding * 2))


        self.is_flscr = is_flscr


        self.cdim = CellDimensions(cell_height, cell_width, cell_margin)

        self.cdim.height += self.cdim.margin

        self.cdim.width += self.cdim.margin

        self.cdim.col_max = int(\
            self.wdim.y_max / (self.cdim.height + self.cdim.margin)\
        )

        self.cdim.row_max = int(\
            self.wdim.x_max / (self.cdim.width + self.cdim.margin)\
        )

        self.cdim.row_n = self.cdim.row_max\
            if self.is_flscr\
                else min(self.wdim.cell_n, self.cdim.row_max)

        self.cdim.col_n = self.cdim.col_max\
            if self.is_flscr\
                else ceil(self.wdim.cell_n / self.cdim.row_n)


        # Validate window dimensions sufficient for displaying cells according
        # to cell dimensions calculated above:

        if ((self.cdim.col_n * self.cdim.row_n) < cell_n):

            raise BufferError("screen size insufficient")


        self.wdim.height = (\
            (self.cdim.height * self.cdim.col_n)
            + (self.wdim.padding * 2)
            - self.cdim.margin\
        )   

        self.wdim.width = (\
            (self.cdim.width * self.cdim.row_n)
            + (self.wdim.padding * 2)
            - self.cdim.margin\
        )

        if not self.is_flscr:

            self.wdim.width = max(\
                (len(self.wdim.title) + (self.wdim.padding * 2)),\
                self.wdim.width\
            )


        # Validate screen dimensions sufficient for displaying window according
        # to window dimensions calculated above:

        if (scr_ymax < (self.wdim.y + self.wdim.height))\
            or (scr_xmax < (self.wdim.x + self.wdim.width)):

            raise BufferError("screen size insufficient")

        
        self.win = stdscr.subwin(\
            self.wdim.height,\
            self.wdim.width,\
            self.wdim.y,\
            self.wdim.x,\
        )

        self.win.box()

        self.win.addstr(0, self.wdim.padding, self.wdim.title)


def validateAlgorithm(algm: str) -> int: # ------------------------------------
    """ This FUNCTION validates the provided name for the chosen algorithm for
        the string matching algorithm is known and returns its integer value.
    """ # ---------------------------------------------------------------------

    algms = {\
        StringMatcher.ALGM_BRUTEFORCE : "BRUTEFORCE",\
        StringMatcher.ALGM_HORSPOOL   : "HORSPOOL",\
        StringMatcher.ALGM_BOYERMOORE : "BOYERMOORE",\
    }


    for a in algms:

        if (algm.casefold() == algms[a].casefold()):

            return a


    raise ArgumentTypeError("chosen algorithm is invalid: {}".format(algm))


def validateFile(path: str) -> str: # -----------------------------------------
    """ This FUNCTION validates a file, specified by its path, contains one or
        more sequence of chars and returns the sequence as a string.
    """ # ---------------------------------------------------------------------

    if os.path.isdir(path):

        raise ArgumentTypeError("is a directory: '{}'".format(path))


    try:

        fd = os.open(path, os.O_RDONLY)

        data = os.read(fd, os.path.getsize(path))


        seq = data.decode("utf-8")

        assert (len(seq) > 0)


        os.close(fd)

    except FileNotFoundError:

        raise ArgumentTypeError("not found: '{}'".format(path))

    except IOError:

        raise ArgumentTypeError("cannot read: '{}'".format(path))

    except AssertionError:

        raise ArgumentTypeError("contains no chars: '{}'".format(path))


    return seq
