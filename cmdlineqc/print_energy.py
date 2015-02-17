#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse

from functools import reduce
from operator import add

from pyqclib.parsing import get_scfenergy


def unitperserving_sum(iterable):
    return reduce(add, iterable)


def main(log_files,
         unit='eV',
         supress_unit=False,
         print_log=False,
         index=-1,
         difference=False,
         ):
    """
    Extracts energy from quantum chemical log file
    and prints it (logfile-formats supported are those of cclib)
    """
    results = []
    for i, log_file in enumerate(log_files):
        ener = get_scfenergy(log_file, unit, index)

        if supress_unit:
            ener = float(ener)

        results.append(ener)

        if not difference:
            if print_log:
                print log_file + ': ',
            print results[i]

    if difference:
        assert print_log is False
        print results[0] - unitperserving_sum(results[1:])
    return os.EX_OK


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument(
        '-u', '--unit', type=str, default='eV', help='Choose from: ' +
        ' '.join(get_scfenergy.units))
    parser.add_argument(
        '-s', '--supress_unit', action='store_true', default=False,
        help='Supress explicit printing of unit')
    parser.add_argument(
        '-p', '--print_log', action='store_true', default=False,
        help='Print logfile name before each energy.')
    parser.add_argument(
        '-i', '--index', type=int, default=-1,
        help='Index of optimization step (default: last)')
    parser.add_argument(
        '-d', '--difference', action='store_true', default=False,
        help='Calculate the difference between the first and the'
        ' sum of the other logfiles.')
    parser.add_argument(
        'log_files', nargs='+', type=str,
        help='log-files from quantum chemical comp.')
    args = parser.parse_args()
    sys.exit(main(**vars(args)))
