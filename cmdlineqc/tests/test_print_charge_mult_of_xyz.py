from cmdlineqc.print_charge_mult_of_xyz import main

assert main('reactant.xyz').startswith('-1 1')

