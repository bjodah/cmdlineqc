#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from future.builtins import *

import argh

class Listener:

    def __init__(self, token, skip=0):
        self.token = token
        self.skip = skip
        self.recording = -1
        self.block = []
        self.blocks = []

    def __call__(self, line):
        if line.startswith(self.token):
            self.recording = self.skip

        if self.recording < 0:
            return

        if self.recording == 0:
            if len(line.strip()) == 0:
                self.blocks.append(self.block)
                self.block = []
                self.recording = -1
            else:
                self.block.append(line)
        else: # recoding > 0
            self.recording -= 1


class SingleLineListener:

    def __init__(self, token):
        self.token = token
        self.blocks = []

    def __call__(self, line):
        if line.startswith(self.token):
            self.blocks.append(line.split(self.token)[1])


def main(logfile, output="output.xyz", verbose=False):
    cart = Listener(token="CARTESIAN COORDINATES (ANGSTROEM)", skip=2)
    fspe = SingleLineListener("FINAL SINGLE POINT ENERGY")
    warn = SingleLineListener("WARNING")

    listeners = [cart, fspe, warn]
    for line in open(logfile, 'rt'):
        for listener in listeners:
            listener(line)
    if verbose:
        print(len(cart.blocks), len(fspe.blocks))
        for w in warn.blocks:
            print("WARNING" + w, end='')
    with open(output, 'wt') as ofh:
        for xyz, ener in zip(cart.blocks, fspe.blocks):
            ofh.write(str(len(xyz))+'\n')
            ofh.write('scf done: {}'.format(ener))
            for line in xyz:
                ofh.write(line)


if __name__ == '__main__':
    argh.dispatch_command(main)
