#!/usr/bin/env python3


# -----------------------------------------------------------------------------
""" ...
""" # -------------------------------------------------------------------------

__author__ = '@kaethis'

__version__ = '1.1'


import argparse

import curses

import util

from strmatch import StringMatcher


def prog(stdscr): # -----------------------------------------------------------
    """ This FUNCTION ...
    """ # ---------------------------------------------------------------------

    global sm


    # NOTE: This program presumes the terminal is capable of displaying color.

    # TODO: Check to see whether or not the terminal is capable of displaying
    #       colors.  If it cannot, skip over color pair initialization and
    #       opt for basic color palette instead.

    color_pairs = {\
        1 : (curses.COLOR_WHITE, curses.COLOR_BLACK),\
        2 : (curses.COLOR_BLACK, curses.COLOR_WHITE),\
        3 : (curses.COLOR_WHITE, curses.COLOR_GREEN),\
        4 : (curses.COLOR_WHITE, curses.COLOR_BLUE),\
    }

    for p in color_pairs.keys():

        curses.init_pair(p, color_pairs[p][0], color_pairs[p][1])


    # Capture maximum dimensions of terminal screen.  The dimensions of each
    # window generated below are calculated depending on the terminal screen's
    # current maximum y-position (or height) and maximum x-position (or width).

    scr_ymax, scr_xmax = stdscr.getmaxyx()


    if (sm.algm == StringMatcher.ALGM_HORSPOOL)\
        or (sm.algm == StringMatcher.ALGM_BOYERMOORE):

        # If chosen algorithm for string matching problem is Horspool or
        # Boyer-Moore, calculate dimensions and create window for displaying
        # bad-symbol table:

        win_y, win_x = 1, 2         # Position bad-symbol table top of screen.

        cell_n = len(sm.bsyms)      # Number of elements in bad-symbol table.


        wbsym = util.Window(\
            stdscr,\
            scr_ymax,\
            scr_xmax,\
            win_y,\
            win_x,\
            cell_n,\
            "BAD-SYMBOL TABLE",\
            cell_width=max(2, len(str(sm.m)))\
        )


        if (sm.algm == StringMatcher.ALGM_BOYERMOORE):

            # If chosen algorithm is Boyer-Moore, also calculate dimensions and
            # create window for displaying good-suffix table:

            win_y = (wbsym.wdim.y + wbsym.wdim.height + wbsym.wdim.margin)

            win_x = wbsym.wdim.x    # Position good-suffix window directly
                                    # below bad-symbol table.

            cell_n = (sm.m - 1)     # Number of elements in good-suffix table.


            wgsuf = util.Window(\
                stdscr,\
                scr_ymax,\
                scr_xmax,\
                win_y,\
                win_x,\
                cell_n,\
                "GOOD-SUFFIX TABLE",\
                cell_width=max(2, len(str(sm.m)))\
            )

    
    # Calculate dimensions and create window for displaying char sequence and
    # pattern. The position of window depends on which algorithm was chosen for
    # the string matching problem:

    if (sm.algm == StringMatcher.ALGM_BRUTEFORCE):

        win_title = "BRUTEFORCE"

        win_y, win_x = 1, 2         # If chosen algorithm is bruteforce,
                                    # position window top of screen.

    elif (sm.algm == StringMatcher.ALGM_HORSPOOL):

        win_title = "HORSPOOL"

        win_y = (wbsym.wdim.y + wbsym.wdim.height + wbsym.wdim.margin)

        win_x = wbsym.wdim.x        # If chosen algorithm is Horspool,
                                    # position window directly below bad-
                                    # symbol table.

    else:

        win_title = "BOYER-MOORE"

        win_y = (wgsuf.wdim.y + wgsuf.wdim.height + wgsuf.wdim.margin)

        win_x = wgsuf.wdim.x        # If chosen algorithm is Boyer-Moore,
                                    # position window directly below good-
                                    # suffix table.

    cell_n = (sm.n + sm.m)      # Number of elements in window (w/ additional
                                # buffer in case index of char comparison
                                # exceeds number of chars in sequence).

    walgm = util.Window(\
        stdscr,\
        scr_ymax,\
        scr_xmax,\
        win_y,\
        win_x,\
        cell_n,\
        win_title,\
        cell_width=max(2, len(str(sm.m))),\
        cell_margin=0,\
        is_flscr=True
    )


    while True:

        if (sm.algm == StringMatcher.ALGM_HORSPOOL)\
            or (sm.algm == StringMatcher.ALGM_BOYERMOORE):

            # If chosen algorithm was Horspool or Boyer-Moore, populate window
            # for bad-symbol table:

            for i in range(wbsym.cdim.col_n):

                for j in range(wbsym.cdim.row_n):

                    cell_i = ((i * wbsym.cdim.row_n) + j)


                    if (0 <= cell_i < wbsym.wdim.cell_n):

                        char = list(sm.bsyms)[cell_i]

                        d = sm.bsyms[char]\
                            if (sm.algm == StringMatcher.ALGM_HORSPOOL)\
                                else max((sm.bsyms[char] - sm.k), 1)


                        if (sm.i < sm.n):

                            if (sm.algm == StringMatcher.ALGM_HORSPOOL):

                                p = curses.color_pair(4)\
                                    if (sm.seq[sm.i] == char)\
                                        else curses.color_pair(2)

                            else:

                                p = curses.color_pair(4)\
                                    if (sm.seq[sm.i - sm.k] == char)\
                                        else curses.color_pair(2)
                        else:

                            p = curses.color_pair(2)


                        y = ((i * wbsym.cdim.height) + wbsym.wdim.padding)

                        x = ((j * wbsym.cdim.width) + wbsym.wdim.padding)

                        s = repr(char)[1:-1]\
                            .rjust(wbsym.cdim.width - wbsym.cdim.margin)


                        wbsym.win.addstr(y, x, s, p)


                        p = curses.color_pair(1)

                        y = ((i * wbsym.cdim.height) + wbsym.wdim.padding)

                        y += 1

                        x = ((j * wbsym.cdim.width) + wbsym.wdim.padding)

                        s = str(d)\
                            .rjust(wbsym.cdim.width - wbsym.cdim.margin)


                        wbsym.win.addstr(y, x, s, p)


            wbsym.win.refresh()


            if (sm.algm == StringMatcher.ALGM_BOYERMOORE):

                # If chosen algorithm was Boyer-Moore, also populate window for
                # good-suffix table:

                for i in range(wgsuf.cdim.col_n):

                    for j in range(wgsuf.cdim.row_n):

                        cell_i = ((i * wgsuf.cdim.row_n) + j)


                        if (0 <= cell_i < wgsuf.wdim.cell_n):

                            k = list(sm.gsufs)[cell_i]

                            d = sm.gsufs[k]


                            p = curses.color_pair(4)\
                                if (sm.k == k)\
                                    else curses.color_pair(2)


                            y = ((i * wgsuf.cdim.height) + wgsuf.wdim.padding)

                            x = ((j * wgsuf.cdim.width) + wgsuf.wdim.padding)

                            s = str(k)\
                                .rjust(wgsuf.cdim.width - wgsuf.cdim.margin)


                            wgsuf.win.addstr(y, x, s, p)


                            p = curses.color_pair(1)

                            y = ((i * wgsuf.cdim.height) + wgsuf.wdim.padding)

                            y += 1

                            x = ((j * wgsuf.cdim.width) + wgsuf.wdim.padding)

                            s = str(d)\
                                .rjust(wgsuf.cdim.width - wgsuf.cdim.margin)


                            wgsuf.win.addstr(y, x, s, p)


                wgsuf.win.refresh()


        # Populate window for display char sequence and pattern:

        for i in range(walgm.cdim.col_n):

            for j in range(walgm.cdim.row_n):

                cell_i = ((i * walgm.cdim.row_n) + j)


                if (0 <= cell_i < walgm.wdim.cell_n):

                    if (cell_i < sm.n):

                        char = sm.seq[cell_i]


                        if (sm.algm == StringMatcher.ALGM_BRUTEFORCE):

                            p = curses.color_pair(3)\
                                if (sm.i <= cell_i < (sm.i + sm.k))\
                                    else curses.color_pair(2)

                        else:

                            p = curses.color_pair(3)\
                                if ((sm.i - sm.k + 1) <= cell_i < (sm.i + 1))\
                                    else curses.color_pair(2)
                    else:

                        char = " "

                        p = curses.color_pair(1)


                    y = ((i * walgm.cdim.height) + walgm.wdim.padding)

                    x = ((j * walgm.cdim.width) + walgm.wdim.padding)

                    s = repr(char)[1:-1]\
                        .rjust(walgm.cdim.width - walgm.cdim.margin)


                    walgm.win.addstr(y, x, s, p)

                    
                    if (sm.algm == StringMatcher.ALGM_BRUTEFORCE):
                    
                        char = sm.ptn[cell_i - sm.i]\
                            if (sm.i <= cell_i < (sm.i + sm.m))\
                                else " "

                    else:

                        char = sm.ptn[cell_i - sm.i - 1]\
                            if (sm.i <= (cell_i + sm.m - 1) < (sm.i + sm.m))\
                                else " "


                    p = curses.color_pair(1)

                    y = ((i * walgm.cdim.height) + walgm.wdim.padding)

                    y += 1

                    x = ((j * walgm.cdim.width) + walgm.wdim.padding)

                    s = repr(char)[1:-1]\
                        .rjust(walgm.cdim.width - walgm.cdim.margin)


                    walgm.win.addstr(y, x, s, p)


        walgm.win.refresh()


        stdscr.move(0, 0)       # Move cursor somewhere inconsequential.

        match stdscr.getch():

            # In case key code match with keypad constant for screen resize ...

            case curses.KEY_RESIZE:

                # NOTE: This program does not account for terminal screen
                #       resize; changing screen dimensions during runtime may
                #       cause curses to throw an exception.

                # TODO: Recalculate only those dimensions affected and resize
                #       window(s) according to new dimensions.

                ...


            # In case key code match with any other keypad constant ...

            case _:

                if sm.step():

                    # If ensued iteration indicates algorithm complete, break
                    # out of loop.

                    break


def exit(): # -----------------------------------------------------------------
    """ This FUNCTION exits the program.
    """ # ---------------------------------------------------------------------

    global sm


    msg_nomatch = "no occurrence of pattern in sequence"

    msg_match = "first occurrence of pattern '{}' at i={} in sequence"\
        .format(sm.ptn, sm.match_i)


    # If no match occurred, print no occurrence msg; otherwise, print msg w/
    # index of first occurrence of pattern in sequence of chars.

    print(msg_nomatch if (sm.match_i == -1) else msg_match)
        

    quit()


def main(): # -----------------------------------------------------------------
    """ This MAIN FUNCTION ...
    """ # ---------------------------------------------------------------------

    global sm


    parser = argparse.ArgumentParser(\
        description= "This PROGRAM features an implementation for string match\
                      using bruteforce, Horspool or Boyer-Moore as its string\
                      matching algorithm.",\
        epilog=      "~created by " + __author__\
    )

    parser.add_argument(\
        'file',\
        metavar= 'PATH',\
        type=    util.validateFile,\
        help=    "path to file containing sequence of n chars"\
    )

    parser.add_argument(\
        'ptn',\
        metavar= 'PATTERN',\
        type=    str,\
        help=    "pattern of m chars to attempt match with first occurrence in\
                  sequence"\
    )

    parser.add_argument(\
        '--algm',\
        metavar= 'ALGORITHM',\
        type=    util.validateAlgorithm,\
        help=    "chosen algorithm for string matching problem (BRUTEFORCE,\
                  HORSPOOL or BOYERMOORE) (default is BRUTEFORCE algorithm)"
    )


    args = parser.parse_args()


    seq = args.file

    ptn = args.ptn

    algm = StringMatcher.ALGM_BRUTEFORCE\
        if args.algm is None\
            else args.algm


    sm = StringMatcher(seq, ptn, algm)


    curses.wrapper(prog)


    exit()  # Exit the program formally.


if __name__ == '__main__': main()
