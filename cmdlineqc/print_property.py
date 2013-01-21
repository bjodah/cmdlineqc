#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import argparse
import inspect

from functools import reduce
from operator import add

from pyqclib.parsing import QCResult
from pyqclib import defs

def unitperserving_sum(iterable):
    return reduce(add, iterable)

def main(log_files,
         property = 'scfenergy',
         arguments = '',
         unit = '',
         supress_unit = False,
         with_filename = False,
         difference = False,
         ):
    """
    Extracts a property from quantum chemical log file
    and prints it (logfile-formats supported are those of cclib)
    """
    results = []
    for i, log_file in enumerate(log_files):
        qcres = QCResult(log_file)
        prop_getter = getattr(qcres, property)
        args = arguments.split(',')
        if args == ['']: args = []
        val = prop_getter(*args)
        if unit != '':
            val = val.rescale(defs.UNITS[prop_getter.unit_type][unit])
        if supress_unit:
            val = float(val)

        results.append(val)

        if not difference:
            if with_filename:
                print log_file +': ',
            print val

    if difference:
        assert with_filename == False
        print results[0] - unitperserving_sum(results[1:])
    return os.EX_OK

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('-p', '--property', type=str, default = 'scfenergy', help='Choose from: ' + \
                        ' '.join([x.func_name for x in QCResult.qc_properties]))
    parser.add_argument('-a', '--arguments', type=str, default = '',
                        help='Arguments for calculation of desired property: ' + \
                        ' '.join([prop_getter.func_name + ': ' + ', '.join(inspect.getargspec(prop_getter)[0]) for \
                                  prop_getter in QCResult.qc_properties]))
    parser.add_argument('-u', '--unit', type=str, default = '', help='Choose from: ' + \
                        ' '.join([prop_getter.func_name + ': ' + ', '.join(defs.UNITS[prop_getter.unit_type].keys()) + '(default: {})'.format(QCResult.default_units[prop_getter.unit_type]) for prop_getter in \
                                  QCResult.qc_properties]))
    parser.add_argument('-s', '--supress_unit', action = 'store_true', default = False, help='Supress explicit printing of unit')
    parser.add_argument('-w', '--with_filename', action = 'store_true', default = False, help='Print logfile name before each property value.')
    parser.add_argument('-d', '--difference', action = 'store_true', default = False, help='Calculate the difference between the first and the sum of the other logfiles.')
    parser.add_argument('log_files',nargs='+',type=str,help='log-files from quantum chemical comp.')
    args = parser.parse_args()
    sys.exit(main(**vars(args)))

