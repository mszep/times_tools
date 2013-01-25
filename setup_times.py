#!/usr/bin/env python
''' Usage: setup_times [--leadsonly N] [--identical-leads]

    Options:
      --leadsonly N       HWire=LeftH0=RightH0. Implies --identical-leads.
                          The system is taken to contain N unit cells, from
                          which the middle one will be extracted and used as
                          H0.
      --identical-leads   Lead unit cells on either side are invariant wrt
                          translation (not inversion).
'''

from docopt import docopt
from gen_times_matrices import *
from matrix_io import read_square_matrix, print_matrix

def main(args):
    if args['--leadsonly'] == False:
        raise ValueError('only --leadsonly supported for now!')

    fock = read_square_matrix(open('Fockout.txt', 'r'))
    overlap = read_square_matrix(open('overlap.dat', 'r'))
    num_unitcells = int(args['--leadsonly'])
    (h0, h1, s0, s1) =  gen_lead_matrices(fock, overlap, num_unitcells)
    write_lead_matrices(h0, h1, s0, s1, 'L')
    write_lead_matrices(h0, h1, s0, s1, 'R')
    num_lead_bfs = ((num_unitcells -1) / 2) * h0.shape[0]
    (hwire, swire) = gen_wire_matrices(fock, overlap, num_lead_bfs, num_lead_bfs)
    write_wire_matrices(hwire, swire)

if __name__ == '__main__':
    args = docopt(__doc__)
    #print args
    main(args)
