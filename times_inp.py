#!/usr/bin/env python

param_defaults = [('NL_Ini', None),
                  ('NR_Ini', None),
                  ('NW_Ini', None),
                  ('L_Ini', 3),
                  ('Length', 1),
                  ('Emin', -0.1),   # These three defaults
                  ('Emax',  0.0),   # are somewhat
                  ('NEsteps', 200), # arbitrary...
                  ('LeadsOnly', False),
                  ('identical', True),
                  ('SystemRun', 'clock'),
                  ('Workmode', 'I'),
                  ('ChanTol', 1e-4),
                  ('DegChanTol', 1e-7),
                  ('InvTol', 1e-10),
                  ('SVDTol', 1e-10),
                  ('UniTol', 5e-4)]

def write_times_inp(params):
    with open('TIMES.inp', 'w') as times_inp:
        def write_line(key, defval):
            val = params.get(key, defval) # sets val to params[key] if
                                          # that exists, otherwise sets
                                          # to defval.
            if type(val) == bool and val == True:
                val = '.True.'
            elif type(val) == bool and val == False:
                val = '.False.'
            else:
                val = str(val)
            line = "{0:16}=        {1:16}".format(key, val)
            times_inp.write(line.strip() + '\n')

        for param, default in param_defaults:
            write_line(param, default)
        


def gen_times_inp(hleft, hright, hwire):
    params = {}
    params['NL_Ini'] = hleft.shape[0]
    params['NR_Ini'] = hright.shape[0]
    params['NW_Ini'] = hwire.shape[0]
    # numpy's array.all() returns a value of type numpy.bool_, which we
    # need to convert to a normal python bool.
    params['identical'] = bool((hleft == hright).all())

    write_times_inp(params)

if __name__ == '__main__':
    from matrix_io import read_square_matrix
    hleft = read_square_matrix(open('LeftH0.dat', 'r'))
    hright = read_square_matrix(open('RightH0.dat', 'r'))
    hwire = read_square_matrix(open('HWire.dat', 'r'))
    gen_times_inp(hleft, hright, hwire)
