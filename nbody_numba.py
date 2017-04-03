"""
   Assignment 8

   Author: Shixin Li
   Date: 04/02/2017
   NetID: sl3368

-------------------------------------------------------

    N-body simulation.

    Author: Shixin Li
    Date: 02/11/2017
    NetID: sl3368


    Runtime = 25.1116509438s

    R = 85.08023528801277s / 25.1116509438s = 3.3881
"""

import itertools
import timeit
from numba import jit, int32, float64, char, vectorize, optional

@vectorize([float64(float64, float64)])
def vec_deltas(x, y):
    return x - y

@jit('void(float64, char[:,:], int32, optional(dict))')
def advance(dt, c, i, BODIES):
    '''
        advance the system one timestep
    '''

    # Local variables
    local_bodies = BODIES
    local_bodies_keys = BODIES.keys()

    for _ in range(i):
        for (body1, body2) in c:
            (x1, v1, m1) = local_bodies[body1]
            (x2, v2, m2) = local_bodies[body2]
            # compute deltas
            (dx, dy, dz) = vec_deltas(x1, x2)

            # update vs
            mag = dt * ((dx * dx + dy * dy + dz * dz) ** (-1.5))
            v1[0] -= dx * m2 * mag
            v1[1] -= dy * m2 * mag
            v1[2] -= dz * m2 * mag
            v2[0] += dx * m1 * mag
            v2[1] += dy * m1 * mag
            v2[2] += dz * m1 * mag
        
        for body in local_bodies_keys:
            (r, [vx, vy, vz], m) = local_bodies[body]

            # update rs
            r[0] += dt * vx
            r[1] += dt * vy
            r[2] += dt * vz

@jit(float64(char[:,:], optional(dict), float64))
def report_energy(c, BODIES, e=0.0):
    '''
        compute the energy and return it so that it can be printed
    '''

    # Local variables
    local_bodies = BODIES
    local_bodies_keys = BODIES.keys()

    for (body1, body2) in c:
        (x1, v1, m1) = local_bodies[body1]
        (x2, v2, m2) = local_bodies[body2]

        # compute deltas
        (dx, dy, dz) = vec_deltas(x1, x2)

        # compute energy
        e -= (m1 * m2) / ((dx * dx + dy * dy + dz * dz) ** 0.5)
        
    for body in local_bodies_keys:
        (r, [vx, vy, vz], m) = local_bodies[body]
        e += m * (vx * vx + vy * vy + vz * vz) / 2.
        
    return e

@jit('void(optional(tuple), optional(dict), float64, float64, float64)')
def offset_momentum(ref, BODIES, px=0.0, py=0.0, pz=0.0):
    '''
        ref is the body in the center of the system
        offset values from this reference
    '''

    # Local variables
    local_bodies = BODIES
    local_bodies_keys = BODIES.keys()

    for body in local_bodies_keys:
        (r, [vx, vy, vz], m) = local_bodies[body]
        px -= vx * m
        py -= vy * m
        pz -= vz * m
        
    (r, v, m) = ref
    v[0] = px / m
    v[1] = py / m
    v[2] = pz / m


@jit('void(int32, char, int32, optional(dict))')
def nbody(loops, reference, iterations, BODIES):
    '''
        nbody simulation
        loops - number of loops to run
        reference - body at center of system
        iterations - number of timesteps to advance
    '''
    # Set up global state
    offset_momentum(BODIES[reference], BODIES)

    # Create body pairs
    bodies_combinations = list(itertools.combinations(BODIES.keys(), 2))

    for _ in range(loops):
        advance(0.01, bodies_combinations, iterations, BODIES)
        print (report_energy(bodies_combinations, BODIES))

if __name__ == '__main__':
    #nbody(100, 'sun', 20000)
    setup = """
import numpy as np
from __main__ import nbody
PI = 3.14159265358979323
SOLAR_MASS = 4 * PI * PI
DAYS_PER_YEAR = 365.24

BODIES = {
'sun': (np.array([0.0, 0.0, 0.0]), [0.0, 0.0, 0.0], SOLAR_MASS),

'jupiter': (np.array([4.84143144246472090e+00,
             -1.16032004402742839e+00,
             -1.03622044471123109e-01]),
            [1.66007664274403694e-03 * DAYS_PER_YEAR,
             7.69901118419740425e-03 * DAYS_PER_YEAR,
             -6.90460016972063023e-05 * DAYS_PER_YEAR],
            9.54791938424326609e-04 * SOLAR_MASS),

'saturn': (np.array([8.34336671824457987e+00,
            4.12479856412430479e+00,
            -4.03523417114321381e-01]),
           [-2.76742510726862411e-03 * DAYS_PER_YEAR,
            4.99852801234917238e-03 * DAYS_PER_YEAR,
            2.30417297573763929e-05 * DAYS_PER_YEAR],
           2.85885980666130812e-04 * SOLAR_MASS),

'uranus': (np.array([1.28943695621391310e+01,
            -1.51111514016986312e+01,
            -2.23307578892655734e-01]),
           [2.96460137564761618e-03 * DAYS_PER_YEAR,
            2.37847173959480950e-03 * DAYS_PER_YEAR,
            -2.96589568540237556e-05 * DAYS_PER_YEAR],
           4.36624404335156298e-05 * SOLAR_MASS),

'neptune': (np.array([1.53796971148509165e+01,
             -2.59193146099879641e+01,
             1.79258772950371181e-01]),
            [2.68067772490389322e-03 * DAYS_PER_YEAR,
             1.62824170038242295e-03 * DAYS_PER_YEAR,
             -9.51592254519715870e-05 * DAYS_PER_YEAR],
            5.15138902046611451e-05 * SOLAR_MASS)}
    """

    # find runtime
    print (timeit.timeit("nbody(100, 'sun', 20000, BODIES)", setup=setup, number=1))

