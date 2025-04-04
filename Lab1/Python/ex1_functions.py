""" System functions """

import numpy as np

# pylint: disable=invalid-name


def analytic_function(t: float) -> float:
    """ Analytic funtion x(t) (To be written)

    Notes:
    - To write exponential(x) in Python with numpy: np.exp(x)
    Example:
    >>> np.exp(0.0)
    1.0

    This function should simply return the state
    """
    # COMPLETE CODE
    state = 5-4*np.exp(-2*t)
    return state


def function(x: float, *_) -> float:
    """ Exercise 1 ODE equation

    Second argument is only required for use with odeint format and can be
    ignored

    Output expected:
    >>> function(0.)
    10.0
    >>> function(5.)
    0.0

    This function should return the derivative x_dot
    """
    # COMPLETE CODE
    dxdt = -2*(x-5)
    if dxdt is None:
        raise NotImplementedError("ODE has not been implemented")
    return dxdt


def function_rk(t: float = None, x: float = None) -> float:
    """ Exercise 1 ODE equation for Runge-Kutta """
    return function(x, t)

