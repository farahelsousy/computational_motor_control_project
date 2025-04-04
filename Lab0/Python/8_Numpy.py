#!/usr/bin/env python3
# pylint: disable=invalid-name

"""Numpy

This script introduces you to the usage of Numpy module in Python.
It is the most important scientific module in Python.
We will only go over some of the very basic functionalities of numpy here.
It can do a lot more!!!

"""

import farms_pylog as pylog  # import pylog for log messages
import numpy as np

pylog.info('%s', 3*'\t' + 20*'#' + ' NUMPY ' + 20*'#')

pylog.info('It is a common standard to use the Numpy module as np!')

# Numpy is the fundamental scientific computing package in Python
# N-dimensional array object

# Create an array using np

A = np.array([[1, 2, 3], [4, 5, 6]])

pylog.info('Array created using numpy, A : %s', A)

pylog.info('Type of numpy array A : %s', type(A))

pylog.info('You can also explicity mention the type of data in the array')

A = np.array([[1, 2, 3], [4, 5, 6]], np.float64)

# Basic numpy methods similar to the ones in MATLAB
# arange, linspace, zeros, shape

pylog.info(
    'Array of integers between 0 and 10 using arange method in numpy : \n%s',
    np.arange(0, 10, 1)
)

pylog.info(
    'Array of integers between 0 and 10 using linspace method in numpy : \n%s',
    np.linspace(0, 10, 11)
)

pylog.info(
    'Array of zeros using zeros method in numpy :\n%s',
    np.zeros((2, 3))
)

pylog.info(
    'Shape of an array using shape method in numpy :\n%s',
    np.zeros((2, 3)).shape,
)

pylog.warning('Numpy arrays are not matrices!!!')

# Math operations
# As mentioned numpy array's are not matrices
# Math operations operate element-wise by default

a = np.arange(4)

pylog.info('Array a : \n%s', a)

b = np.array([2, 3, 2, 4])

pylog.info('Array b : \n%s', b)

pylog.info('Element wise multiplication of numpy arrays a*b : \n%s', a*b)

pylog.info('Element wise subtraction of numpy arrays b-a :\n%s', b-a)

pylog.info(
    """Have a look at Array broadcasting to understand how numpy
    compares two arrays for math operations""")

# Create a random numpy array using random method
A = np.ones((2, 3))
pylog.info('Numpy array  A of size (2,3) using ones method :\n%s', A)

# Create a random numpy array using random method
B = np.ones((3, 2))
pylog.info('Numpy array B of size (3,2) using ones method :\n%s', B)

pylog.info(
    'Matrix multiplication A*B using numpy dot method :\n%s', np.dot(A, B))

pylog.info(
    'Matrix multiplication B*A using numpy dot method :\n%s', np.dot(B, A))

try:
    pylog.info(
        'Matrix multiplication transpose(A)*B using numpy dot method:%s',
        np.dot(A.T, B)
    )
except ValueError:
    pylog.error(
        'ValueError: shapes (3,2) and (3,2) not aligned:'
        ' 2 (dim 1) != 3 (dim 0)'
    )

pylog.info('Have a look at numpy matrices method!')
pylog.warning('Numpy matrices are not very often used, arrays are more common')

