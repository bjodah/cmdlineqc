#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse, sys, os
from jobhoc.naming import splitnum

def main(job_files,
         from_log = False,
         from_check = False,
         at_exe = False):
    """
    Create extension jobs from prematurely
    ended com files (Typical Link 9999 error)
    """

    if not from_check: assert from_log

    if from_log:
        assert all([x.endswith('.log') for x in job_files])

    for job in job_files:
        basename = os.path.basename(job)
        rootname, ext = os.path.splitext(basename)

        if from_log:
            com = os.path.splitext(job)[0] + '.com'
        else:
            com = job

        unnumname, num = splitnum(rootname)

        if at_exe:
            new_com = unnumname + str(num + 1) + '.com'
        else:
            new_com = os.path.join(os.path.dirname(com), unnumname + str(num + 1) + '.com')

        found_root_card = False
        n_after_rc = 0
        for line in open(com, 'rt'):
            if found_root_card: n_after_rc += 1
            if line.startswith(r'#'):
                rootcard = line[1:].strip('\n').split()
                if from_check: break
                found_root_card = 1
            if n_after_rc == 2:
                title = line.strip('\n')
            if n_after_rc == 4:
                spin_mult = line

        assert not os.path.exists(new_com)
        ofh = open(new_com, 'wt')

        if from_check:
            # Let's use old check file
            src_check = os.path.splitext(job)[0] + '.chk'
            assert os.path.isfile(src_check)

            has_geom_check = False
            has_guess_read = False
            for entry in rootcard:
                if entry.lower().startswith('geometry'):
                    assert entry.split('=')[1].lower().startswith('allcheck')
                    has_geom_check = True
                if entry.lower().startswith('guess'):
                    assert entry.split('=')[1].lower().startswith('read')
                    has_guess_read = True

            if not has_geom_check:
                rootcard += ['geom=allcheck']
            if not has_guess_read:
                rootcard += ['guess=read']

            new_chk = os.path.join(os.path.dirname(job), unnumname + str(num + 1) + '.chk')
            assert not os.path.exists(new_chk)
            shutil.copy(src_check, new_chk)
            # Write new com-file (let other script set % variables)
            assert not os.path.exists(new_com)
            ofh.write('#' + ' '.join(rootcard) + '\n\n')
        else:
            from qcparse import get_last_coord_block_str
            ofh.write('#' + ' '.join(rootcard) + '\n\n')
            ofh.write(title + '.  CONTINUING FROM: ' + job + '\n\n')
            ofh.write(spin_mult)
            ofh.write(get_last_coord_block_str(job) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('-l', '--from-log', action = 'store_true',
                        help = 'Grab the com with same name as provided log-file(s)')
    parser.add_argument('-a', '--at-exe', action = 'store_true',
                        help = 'Create new com at place of execution')
    parser.add_argument('-c', '--from-check', action = 'store_true',
                        help = 'Start from checkpoint file instead of reading geometry')

    parser.add_argument('job_files',nargs='+',type=str,help='com- or log-files')
    args = parser.parse_args()
    sys.exit(main(**vars(args)))
