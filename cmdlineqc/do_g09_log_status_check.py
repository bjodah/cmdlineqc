#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse, sys, os
from jobhoc.naming import splitnum

def tail(f, window=20):
    """
    from: http://stackoverflow.com/questions/136168/get-last-n-lines-of-a-file-with-python-similar-to-tail
    """
    bufsize = 1024
    f.seek(0, 2)
    bytes = f.tell()
    size = window
    block = -1
    data = []
    while size > 0 and bytes > 0:
        if (bytes - bufsize > 0):
            # Seek back one whole bufsize
            f.seek(block*bufsize, 2)
            # read BUFFER
            data.append(f.read(bufsize))
        else:
            # file too small, start from begining
            f.seek(0,0)
            # only read what was not read
            data.append(f.read(bytes))
        linesFound = data[-1].count('\n')
        size -= linesFound
        bytes -= bufsize
        block -= 1
    return '\n'.join(''.join(data).splitlines()[-window:])


def main(dirpath, verbose=False, no_status=False):
    """
    Check g09 log files of highest trailing number
    in name for successful exit of job.
    """
    logfilenum = {}
    for fname in os.listdir(dirpath):
        if fname.endswith('.log'):
            rootname, ext = os.path.splitext(fname)
            unnumname, num = splitnum(rootname)
            if unnumname in logfilenum:
                logfilenum[unnumname] = max(num, logfilenum[unnumname])
            else:
                logfilenum[unnumname] = num

    for unnumname, num in logfilenum.iteritems():
        fname = os.path.join(dirpath, unnumname + str(num) + '.log')
        if not os.path.exists(fname):
            fname2 = os.path.join(dirpath, unnumname + '.log')
            if os.path.exists(fname2): fname = fname2
        lastline = tail(open(fname, 'rt'), 1)
        if lastline.startswith(' Normal termination'):
            if verbose:
                if no_status:
                    print fname
                else:
                    print fname, ': ok.'
        elif lastline.startswith(' File lengths'):
            if no_status:
                print fname
            else:
                print fname, ': error.'
        else:
            if no_status:
                print fname
            else:
                print fname, ': running?'
    return os.EX_OK

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('-v', '--verbose', action='store_true', help='Also print what jobs finished ok.')
    parser.add_argument('-n', '--no-status', action='store_true', help='Print no staus at all, only list logs with highest ending number.')
    parser.add_argument('dirpath',type=str,help='path to dir for which to check log files')
    args = parser.parse_args()
    sys.exit(main(**vars(args)))
