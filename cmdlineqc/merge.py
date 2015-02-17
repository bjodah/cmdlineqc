#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from future.builtins import *

import argh
import numpy as np

def load_xyz(path):
    with open(path, 'rt') as fh:
        natoms = int(fh.readline())
        title = fh.readline().strip()
        xyz = np.zeros((natoms, 3))
        atoms = []
        for i in range(natoms):
            atom, x, y, z = fh.readline().split()
            atoms.append(atom)
            xyz[i, :] = [float(v) for v in (x, y, z)]
    return natoms, title, atoms, xyz

def write_xyz(path, title, atoms, xyz):
    with open(path, 'wt') as fh:
        fh.write("%d\n" % len(atoms))
        fh.write(title + ('\n' if not title.endswith('\n') else ''))
        for i, atom in enumerate(atoms):
            fh.write("%s %10.5f %10.5f %10.5f\n" % (
                atom, xyz[i, 0], xyz[i, 1], xyz[i, 2]))

def main(*files):
    """
    Average positions of multiple xyz files
    """
    data = {}
    for natoms, title, atoms, xyz in map(load_xyz, files):
        if 'natoms' not in data:
            data['natoms'] = natoms
            data['title'] = title
            data['atoms'] = atoms
            data['xyz'] = xyz
        else:
            if not data['natoms'] == natoms:
                raise ValueError("Incompatible number of atoms!")
            if not data['atoms'] == atoms:
                raise ValueError("Incompatible atoms!")
            data['xyz'] += xyz
    data['xyz'] /= len(files)
    write_xyz('merged.xyz', 'merged', data['atoms'], data['xyz'])

if __name__ == '__main__':
    argh.dispatch_command(main)
