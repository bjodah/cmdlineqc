#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import argparse
import logging
import re

def main(xyz_path, fmtstr = '{} {}'):
    """
    Extracts CHARGE=$CHG and MULT=$MULT from
    xyz title row (as generated by mk_xyz_from_log.py)
    and prints them formated as fmtstr to stdout (default whitespace sep.)
    """
    fh = open(xyz_path, 'rt')
    num = fh.readline()
    title_line = fh.readline() # Title is second row in xyz file
    fh.close()
    logging.debug('Read title line: {}'.format(title_line))
    charge = re.search('(?<=CHARGE\=)-?\w', title_line)
    mult = re.search('(?<=MULT\=)\w', title_line)
    if charge == None or mult == None:
        sys.exit(1)
    return fmtstr.format(charge.group(0), mult.group(0))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('xyz_path', type=str, help='xyz - file')
    args = parser.parse_args()
    print main(**vars(args))
    sys.exit(os.EX_OK)
