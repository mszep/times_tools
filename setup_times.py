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
from times_inp import gen_times_inp
from matrix_io import read_square_matrix, print_matrix

def main(args):
    if args['--leadsonly']:
        fock = read_square_matrix(open('Fockout.txt', 'r'))
        overlap = read_square_matrix(open('overlap.dat', 'r'))
        num_unitcells = int(args['--leadsonly'])
        (h0, h1, s0, s1) =  gen_lead_matrices(fock, overlap, num_unitcells)
        write_lead_matrices(h0, h1, s0, s1, 'L')
        write_lead_matrices(h0, h1, s0, s1, 'R')
        num_lead_bfs = ((num_unitcells -1) / 2) * h0.shape[0]
        #(hwire, swire) = gen_wire_matrices(fock, overlap, num_lead_bfs, num_lead_bfs)
        (hwire, swire) = (h0, s0)
        write_wire_matrices(hwire, swire)
        gen_times_inp(h0, h0, hwire)
    else:
        fock = read_square_matrix(open('Fockout.txt', 'r'))
        overlap = read_square_matrix(open('overlap.dat', 'r'))
        left_h0 = read_square_matrix(open('LeftH0.dat', 'r'))
        right_h0 = read_square_matrix(open('RightH0.dat', 'r'))
        num_lead_bfs_left = left_h0.shape[0]
        num_lead_bfs_right = right_h0.shape[0]
        (hwire, swire) = gen_wire_matrices(fock, overlap,
                            num_lead_bfs_left, num_lead_bfs_right)
        write_wire_matrices(hwire, swire)
        gen_times_inp(left_h0, right_h0, hwire)


if __name__ == '__main__':
    args = docopt(__doc__)
    #print args
    main(args)
