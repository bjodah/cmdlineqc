#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, logging
import argparse
from cclib.parser import ccopen

def main(job_files,
         at_exe = False,
         suffix = ''):
    """
    Extracts final energy from log file and prints it in Hartree
    (output formats supported are those of cclib)
    """
    for job_file in job_files:
        ccfile = ccopen(job_file)
        ccfile.logger.setLevel(logging.ERROR)
        data = ccfile.parse()
        print data.scfenergies[-1]

    return os.EX_OK

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('job_files',nargs='+',type=str,help='or log-files')
    args = parser.parse_args()
    sys.exit(main(**vars(args)))
