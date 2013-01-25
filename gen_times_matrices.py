#!/usr/bin/env python

from matrix_io import read_square_matrix, print_matrix
from matrix_manip import trim_matrix
from docopt import docopt
import sys

''' Generate TiMeS input for one lead (L or R) or both, based on
    Fockout.txt and overlap.dat files from fockcalcunitcellwire.
    These files should describe a system with only lead unit cells,
    stacked against each other. The script will then grab inter- and
    intra-cell interaction and overlap matrices from the middle, to
    avoid edge effects. Empirically, if the cells are big enough for
    next-nearest neighbour interactions to be negligible, taking 5
    or more cells here is enough to eliminate edge effects.'''

def gen_lead_matrices(fock, overlap, num_unitcells):

    # Determine whether num_unitcells divides the dimension of fock and
    # overlap.
    n = fock.shape[0]
    if n % num_unitcells != 0:
        exit("Erorr; num_unitcells, {0:d}, does not divide n, {1:d}"\
                .format(num_unitcells, n))
    else:
        bfs_per_cell = n / num_unitcells

    # the starting index of the intra-cell interaction; in other words,
    # the number of rows and cols to chop off the top left.
    intra_start = ((num_unitcells - 1) / 2) * bfs_per_cell
    intra_end = intra_start + bfs_per_cell

    # these two are needed to shift the first index only, to slice out
    # a nearest neighbour block.
    inter_start = intra_start + bfs_per_cell
    inter_end = intra_end + bfs_per_cell

    h0 = fock[intra_start:intra_end,intra_start:intra_end]
    h1 = fock[inter_start:inter_end,intra_start:intra_end]
    s0 = overlap[intra_start:intra_end,intra_start:intra_end]
    s1 = overlap[inter_start:inter_end,intra_start:intra_end]
    return (h0, h1, s0, s1)

def write_lead_matrices(h0, h1, s0, s1, LR):
    if LR == 'L':
        LRstring = 'Left'
    elif LR == 'R':
        LRstring = 'Right'
    else:
        raise ValueError('LR must be one of "L" or "R"')

    def write_to_file(filename, mat):
        with open(filename, 'w') as f:
            print_matrix(mat, f, compl=True)
    
    write_to_file(LRstring + 'H0.dat', h0)
    write_to_file(LRstring + 'H1.dat', h1)
    write_to_file(LRstring + 'S0.dat', s0)
    write_to_file(LRstring + 'S1.dat', s1)

def gen_wire_matrices(fock, overlap, offleft, offright):
    fock_wire = trim_matrix(fock, offleft, offright)
    overlap_wire = trim_matrix(overlap, offleft, offright)
    return (fock_wire, overlap_wire)

def write_wire_matrices(hwire, swire):
    with open('HWire.dat', 'w') as f:
        print_matrix(hwire, f)
    with open('SWire.dat', 'w') as g:
        print_matrix(swire, g)

if __name__ == '__main__':

    fock = read_square_matrix(open('Fockout.txt', 'r'))
    overlap = read_square_matrix(open('overlap.dat', 'r'))
    num_unitcells = 7
    (h0, h1, s0, s1) =  gen_lead_matrices(fock, overlap, num_unitcells)
    
