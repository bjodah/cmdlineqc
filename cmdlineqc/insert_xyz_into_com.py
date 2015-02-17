#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from future.builtins import *

import argh


def main(xyz, com):
    new_coords = []
    with open(xyz, 'rt') as ifh:
        for l_idx, line in enumerate(ifh):
            if l_idx >= 2:
                new_coords.append(line)

    old_com = open(com, 'rt').readlines()
    with open(com, 'wt') as ofh:
        reached_root = False
        reached_title = False
        reached_charge_mult = False
        passed_coords = False
        for line in old_com:
            if not reached_root:
                if line.startswith('#'):
                    reached_root = True
                ofh.write(line)
                continue
            if not reached_title:
                if line.strip() != '':
                    reached_title = True
                ofh.write(line)
                continue
            if not reached_charge_mult:
                if len(line.split()) == 2:
                    reached_charge_mult = True
                ofh.write(line)
                continue
            if not passed_coords:
                if line.strip() == '':
                    passed_coords = True
                    for coord in new_coords:
                        ofh.write(coord)
                    ofh.write(line)
                continue
            ofh.write(line)


if __name__ == '__main__':
    argh.dispatch_command(main)
