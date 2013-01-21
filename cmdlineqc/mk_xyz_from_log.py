#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Original inspiration of file:
#http://www.ccl.net/chemistry/resources/messages/2010/05/20.003-dir/index.html

import os, sys, logging
import argparse
from cclib.parser import ccopen
from cclib.bridge import makeopenbabel
import openbabel as ob

def get_open_babel_conv(outformat = 'XYZ'):
    obconv = ob.OBConversion()
    ok = obconv.SetOutFormat(outformat)
    return obconv

def main(job_files,
         at_src = False,
         suffix = '',
         distort_normal = 0.0,
         normal_idx = -1,
         geom_idx = -1):
    """
    Extracts xyz data from log file of QC calculation
    (output formats supported are those of cclib)
    """

    obconv = get_open_babel_conv()

    for job_file in job_files:
        ccfile = ccopen(job_file)
        ccfile.logger.setLevel(logging.ERROR)
        data = ccfile.parse()
        if distort_normal != 0.0:
            coords = data.atomcoords[geom_idx] + distort_normal * data.vibdisps[normal_idx]
        else:
            coords = data.atomcoords[geom_idx]
        obmol = makeopenbabel(coords, data.atomnos, charge = data.charge, mult = data.mult)
        obmol.SetTitle('SRC={}, CHARGE={}, MULT={}'.format(job_file,
                                                           data.charge,
                                                           data.mult))
        dirname = os.path.dirname(job_file)
        basename = os.path.basename(job_file)
        rootname, ext = os.path.splitext(basename)
        if at_src:
            destpath = os.path.join(dirname, rootname + suffix + '.xyz')
        else:
            destpath = rootname + suffix + '.xyz'

        obconv.WriteFile(obmol, destpath)
        return os.EX_OK

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('-a', '--at-src', action = 'store_true',
                        help = 'Create xyz in directory of source instead of at source')
    parser.add_argument('-s', '--suffix', type = str, default = '',
                        help = 'Suffix for xyz file, e.g. `_final`')
    parser.add_argument('-d', '--distort_normal', type = float, default = 0.0,
                        help = 'Distort along normal coordinate')
    parser.add_argument('-n', '--normal_idx', type = int, default = -1,
                        help = 'Index of normal coordinate to distort along')
    parser.add_argument('-g', '--geom_idx', type = int, default = -1,
                        help = 'Index of geometry to extract. Default: -1 (last)')

    parser.add_argument('job_files',nargs='+',type=str,help='com- or log-files')
    args = parser.parse_args()
    sys.exit(main(**vars(args)))

