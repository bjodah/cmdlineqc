#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, logging
import argparse
from cclib.parser import ccopen
import quantities as pq

from pyqclib.defs import UNITLESS_IN_ELECTRONVOLT_TO_TYPED_KILOJOULE_PER_MOL, UNITLESS_IN_ELECTRONVOLT_TO_TYPED_KILOJOULE_PER_MOL

# Conversion factors
CONVERTSION_FROM_EV_TO = {'kCal_per_mole': UNITLESS_IN_ELECTRONVOLT_TO_TYPED_KILOJOULE_PER_MOL,
             'kJ_per_mole': UNITLESS_IN_ELECTRONVOLT_TO_TYPED_KILOJOULE_PER_MOL,
             'eV': 1}

def main(job_files,
         energy_unit = 'eV',
         ):
    """
    Extracts final energy from log file and prints it in Hartree
    (logfile-formats supported are those of cclib)
    """
    for job_file in job_files:
        ccfile = ccopen(job_file)
        ccfile.logger.setLevel(logging.ERROR)
        data = ccfile.parse()
        print data.scfenergies[-1] * CONVERTSION_FROM_EV_TO[energy_unit]

    return os.EX_OK

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('log_files',nargs='+',type=str,help='log-files from quantum chemical comp.')
    parser.add_argument('energy_unit', type=str, default = 'eV', help='Choose from: ' + \
                        ' '.join(CONVERTSION_FROM_EV_TO.keys()))
    args = parser.parse_args()
    sys.exit(main(**vars(args)))
