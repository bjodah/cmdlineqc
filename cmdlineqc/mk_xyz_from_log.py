#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Original inspiration of file:
#http://www.ccl.net/chemistry/resources/messages/2010/05/20.003-dir/index.html

import os, sys, logging
import argparse
from cclib.parser import ccopen
from cclib.bridge import makeopenbabel
import openbabel as ob

def main(job_files,
         at_exe = False,
         suffix = '',
         distort_normal = 0.0,
         normal_idx = -1):
    """
    Extracts xyz data from log file of QC calculation
    (output formats supported are those of cclib)
    """
    for job_file in job_files:
        ccfile = ccopen(job_file)
        ccfile.logger.setLevel(logging.ERROR)
        data = ccfile.parse()
        if distort_normal != 0.0:
            coords = data.atomcoords[-1] + distort_normal * data.vibdisps[normal_idx]
        else:
            coords = data.atomcoords[-1]
        obmol = makeopenbabel(coords, data.atomnos)
        obconv = ob.OBConversion()
        ok = obconv.SetOutFormat("XYZ")
        dirname = os.path.dirname(job_file)
        basename = os.path.basename(job_file)
        rootname, ext = os.path.splitext(basename)
        if at_exe:
            destpath = rootname + suffix + '.xyz'
        else:
            destpath = os.path.join(dirname, rootname + suffix + '.xyz')

        obconv.WriteFile(obmol, destpath)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('-a', '--at-exe', action = 'store_true',
                        help = 'Create xyz at place of execution instead of at source')
    parser.add_argument('-s', '--suffix', type = str, default = '',
                        help = 'Suffix for xyz file, e.g. `_final`')
    parser.add_argument('-d', '--distort_normal', type = float, default = 0.0,
                        help = 'Distort along normal coordinate')
    parser.add_argument('-i', '--normal_idx', type = int, default = -1,
                        help = 'Index of normal coordinate to distort along')

    parser.add_argument('job_files',nargs='+',type=str,help='com- or log-files')
    args = parser.parse_args()
    sys.exit(main(**vars(args)))
