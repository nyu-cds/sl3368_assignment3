# -----------------------------------------------------------------------------
# calculator.py
# ----------------------------------------------------------------------------- 

'''
For the original calculator.py:
cProfile: 1004015 function calls in 1.748 seconds

line_profiler: 
Timer unit: 1e-06 s

Total time: 3.07813 s
File: calculator.py
Function: hypotenuse at line 42

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    42                                           def hypotenuse(x,y):
    43                                               """
    44                                               Return sqrt(x**2 + y**2) for two arrays, a and b.
    45                                               x and y must be two-dimensional arrays of the same shape.
    46                                               """
    47         1       831258 831258.0     27.0      xx = multiply(x,x)
    48         1       791362 791362.0     25.7      yy = multiply(y,y)
    49         1       771306 771306.0     25.1      zz = add(xx, yy)
    50         1       684204 684204.0     22.2      return sqrt(zz)




After making changes to the code (used numpy to replace python code):

For the revised calculator.py:
cProfile: 11 function calls in 0.020 seconds

line_profiler:
Timer unit: 1e-06 s

Total time: 0.019049 s
File: calculator.py
Function: hypotenuse at line 35

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    35                                           def hypotenuse(x,y):
    36                                               """
    37                                               Return sqrt(x**2 + y**2) for two arrays, a and b.
    38                                               x and y must be two-dimensional arrays of the same shape.
    39                                               """
    40         1         5110   5110.0     26.8      xx = multiply(x,x)
    41         1         4588   4588.0     24.1      yy = multiply(y,y)
    42         1         4849   4849.0     25.5      zz = add(xx, yy)
    43         1         4502   4502.0     23.6      return sqrt(zz)




speedup = 1.748s / 0.020s = 87.4 times

'''
import numpy as np

def add(x,y):
    """
    Add two arrays.
    x and y must be two-dimensional arrays of the same shape.
    """
    m,n = x.shape
    z = np.zeros((m,n))
    z = np.add(x,y)
    return z


def multiply(x,y):
    """
    Multiply two arrays.
    x and y must be two-dimensional arrays of the same shape.
    """
    m,n = x.shape
    z = np.zeros((m,n))
    z = np.multiply(x,y)
    return z


def sqrt(x):
    """
    Take the square root of the elements of an arrays.
    """
    m,n = x.shape
    z = np.zeros((m,n))
    z = np.sqrt(x)
    return z


def hypotenuse(x,y):
    """
    Return sqrt(x**2 + y**2) for two arrays, a and b.
    x and y must be two-dimensional arrays of the same shape.
    """
    xx = multiply(x,x)
    yy = multiply(y,y)
    zz = add(xx, yy)
    return sqrt(zz)


