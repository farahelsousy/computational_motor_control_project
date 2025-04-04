""" Lab 4 : System Parameters """

from typing import Callable
import numpy as np
import farms_pylog as pylog

# pylint: disable=invalid-name,too-many-instance-attributes
# ,too-many-arguments


class SystemParameters:
    """System parameters

    Parent class providing main attributes for other sub system parameters.

    """

    def __init__(self, name: str = 'System'):
        super().__init__()
        self.name: str = name

    def show_parameters(self):
        """Show parameters"""
        raise NotImplementedError()

    def msg(self, parameters, units, endl='\n' + 4 * ' '):
        """ Message """
        to_print = f'{self.name} parameters:'
        for param in parameters:
            to_print += f'{endl}{param}: {parameters[param]} [{units[param]}]'
        return to_print


class PendulumParameters(SystemParameters):
    """ Pendulum parameters
    Note:
    This is a generic class for a pair of spring-dampers with two stiffness and
    damping paramters (defined below). To model a single spring-damper just set
    the reference angle to be equal (s_theta_ref1=s_theta_ref2) and the spring/damping
    coefficients also equal (k1=k2, b1=b2).

    with:
        Pendulum Parameters:
            - g: Gravity constant [m/s**2]
            - m: Mass [kg]
            - L: Length [m]
            - I: Inerita [kg-m**2]
            - sin: Sine function
            - dry: Use dry friction (bool: True or False)

        Spring Parameters:
            - k1 : Spring constant of spring 1 [N/rad]
            - k2 : Spring constant of spring 2 [N/rad]

            - s_theta_ref1 : Spring 1 reference angle [rad]
            - s_theta_ref2 : Spring 2 reference angle [rad]

         Damper Parameters:
            - b1 : Damping constant damper 1 [N-s/rad]
            - b2 : Damping constant damper 2 [N-s/rad]

    Examples:

        >>> pendulum_parameters = PendulumParameters(g=9.81, L=0.1)
        >>> pendulum_parameters = PendulumParameters(d=0.3, dry=True)

    Note that not giving arguments to instanciate the object will result in the
    following default values:
        # Pendulum Parameters
        - g = 9.81
        - m = 1.
        - L = 1.
        - I = 1.
        - sin = np.sin
        - dry = False

        # Spring Parameters
        - k1 = 10.
        - k2 = 10.
        - s_theta_ref1 =  0.0
        - s_theta_ref2 =  0.0

        # Damping Parameters
        - b1 = 0.5
        - b2 = 0.5



    These parameter variables can then be called from within the class using
    for example:

        To assign a new value to the object variable from within the class:

        >>> self.g = 9.81 # Reassign gravity constant

        To assign to another variable from within the class:

        >>> example_g = self.g

    To call the parameters from outside the class, such as after instatiation
    similarly to the example above:

        To assign a new value to the object variable from outside the class:

        >>> pendulum_parameters = SystemParameters(L=1.0)
        >>> pendulum_parameters.L = 0.3 # Reassign length

        To assign to another variable from outside the class:

        >>> pendulum_parameters = SystemParameters()
        >>> example_g = pendulum_parameters.g # example_g = 9.81

    You can display the parameters using:

    >>> pendulum_parameters = SystemParameters()
    >>> print(pendulum_parameters.show_parameters())
    Pendulum parameters:
        g: 9.81 [m/s**2]
        m: 1. [kg]
        L: 1.0 [m]
        I: 1.0 [kg-m**2]
        sin: <ufunc 'sin'>
        dry: False

    Spring parameters:
        k1: 0.0 [N/rad]
        k2: 0.0 [N/rad]
        s_theta_ref1: 0.0 [rad]
        s_theta_ref2: 0.0 [rad]

    Damping parameters:
        b1: 0.0 [N-s/rad]
        b2: 0.0 [N-s/rad]

    Or using pylog:

    >>> pendulum_parameters = SystemParameters()
    >>> pylog.info(system_parameters.show_parameters())
    """

    def __init__(self, **kwargs):
        super().__init__('Pendulum')

        self.parameters = {}
        self.units = {}

        self.units['g'] = 'm / s**2'
        self.units['m'] = 'kg'
        self.units['L'] = 'm'
        self.units['I'] = 'kg m**2'
        self.units['sin'] = ''
        self.units['k1'] = 'N m / rad'
        self.units['k2'] = 'N m / rad'
        self.units['s_theta_ref1'] = 'rad'
        self.units['s_theta_ref2'] = 'rad'
        self.units['b1'] = 'N m s / rad'
        self.units['b2'] = 'N m s / rad'

        # Initialize parameters
        self.parameters = {
            'g': 9.81, 'm': 1., 'L': 1., 'I': 0.0, 'sin': np.sin, 'k1': 0.,
            'k2': 0., 's_theta_ref1': 0., 's_theta_ref2': 0.,
            'b1': 0., 'b2': 0.}

        # Pendulum parameters
        self.g = kwargs.pop('g', 9.81)  # Gravity constant
        self.m = kwargs.pop('m', 1.)  # Mass
        self.L = kwargs.pop('L', 1.)  # Length
        self.sin = kwargs.pop('sin', np.sin)  # Sine function
        self.dry: bool = kwargs.pop('dry', False)  # Use dry friction
        # Spring parameters
        self.k1 = kwargs.pop(
            'k1', 0.)  # Spring constant of Spring 1
        self.k2 = kwargs.pop(
            'k2', 0.)  # Spring constant of Spring 2
        self.s_theta_ref1 = kwargs.pop(
            's_theta_ref1', 0.0)  # Spring 1 reference angle
        self.s_theta_ref2 = kwargs.pop(
            's_theta_ref2', 0.0)  # Spring 2 reference angle
        # Damping parameters
        self.b1 = kwargs.pop(
            'b1', 0.)  # Damping constant of Damper 1
        self.b2 = kwargs.pop(
            'b2', 0.)  # Damping constant of Damper 2

        pylog.info(self)

    @property
    def g(self):
        """ Get the value of gravity in the system. [N-m/s2]
        Default is 9.81 """
        return self.parameters['g']

    @g.setter
    def g(self, value: float):
        """ Keyword Arguments:
        value -- Set the value of gravity [N-m/s2] """
        self.parameters['g'] = value
        pylog.info(
            'Changed gravity to %s [N-m/s2]',
            self.parameters['g'],
        )

    @property
    def m(self):
        """ Get the mass of the pendulum."""
        return self.parameters['m']

    @m.setter
    def m(self, value: float):
        """
        Set the mass of the pendulum.
        Setting/Changing mass will automatically recompute the inertia.
        """
        self.parameters['m'] = value
        # ReCompute inertia
        # Inertia = m*l**2
        self.I = self.parameters['m']*self.L**2
        pylog.debug(
            'Changed pendulum mass to %s [kg]',
            self.m,
        )

    @property
    def I(self):
        """ Get the inertia of the pendulum [kg-m**2]  """
        return self.parameters['I']

    @I.setter
    def I(self, value: float):
        """ Set the value of the pendulum inertia """
        self.parameters['I'] = value

    @property
    def L(self):
        """ Get the value of pendulum length. [m]
        Default is 1.0"""
        return self.parameters['L']

    @L.setter
    def L(self, value: float):
        """ Keyword Arguments:
        value -- Set the value of pendulum's length [m] """
        self.parameters['L'] = value
        # ReCompute inertia
        # Inertia = m*l**2
        self.I = self.m*self.parameters['L']**2
        pylog.debug(
            'Changed pendulum length to %s [m]',
            self.L,
        )

    @property
    def sin(self):
        """ Get the sine function."""
        return self.parameters['sin']

    @sin.setter
    def sin(self, value: Callable):
        """ Set the sine function to be used. """
        self.parameters['sin'] = value

    @property
    def k1(self):
        """ Get the value of spring constant for spring 1. [N/rad]
        Default is -10.0"""
        return self.parameters['k1']

    @k1.setter
    def k1(self, value: float):
        """ Keyword Arguments:
        value -- Set the value of spring constant for spring 1 [N/rad] """
        if value < 0.0:
            pylog.warning('Setting bad spring constant. Should be positive!')
        else:
            self.parameters['k1'] = value
        pylog.info(
            'Changed spring constant of spring 1 to %s [N/rad]',
            self.parameters["k1"],
        )

    @property
    def k2(self):
        """ Get the value of spring constant for spring 2. [N/rad]
        Default is -10.0"""
        return self.parameters['k2']

    @k2.setter
    def k2(self, value: float):
        """ Keyword Arguments:
        value -- Set the value of spring constant for spring 2[N/rad] """
        if value < 0.0:
            pylog.warning('Setting bad spring constant. Should be positive!')
        else:
            self.parameters['k2'] = value
        pylog.info(
            'Changed spring constant of spring 1 to %s [N/rad]',
            self.parameters['k2'],
        )

    @property
    def s_theta_ref1(self):
        """ Get the value of spring 1 reference angle. [rad]
        Default is 0.0"""
        return self.parameters['s_theta_ref1']

    @s_theta_ref1.setter
    def s_theta_ref1(self, value):
        """ Keyword Arguments:
        value -- Set the value of spring 1 reference angle [rad] """
        self.parameters['s_theta_ref1'] = value
        pylog.info(
            'Changed spring 1 reference angle to %s [rad]',
            self.parameters['s_theta_ref1'],
        )

    @property
    def s_theta_ref2(self):
        """ Get the value of spring 2 reference angle. [rad]
        Default is 0.0"""
        return self.parameters['s_theta_ref2']

    @s_theta_ref2.setter
    def s_theta_ref2(self, value: float):
        """ Keyword Arguments:
        value -- Set the value of spring 2 reference angle [rad] """
        self.parameters['s_theta_ref2'] = value
        pylog.info(
            'Changed spring 2 reference angle to %s [rad]',
            self.parameters['s_theta_ref2'],
        )

    @property
    def b1(self):
        """ Get the value of damping constant for damper 1. [N-s/rad]
        Default is 0.5"""
        return self.parameters['b1']

    @b1.setter
    def b1(self, value: float):
        """ Keyword Arguments:
        value -- Set the value of damping constant for damper 1. [N-s/rad] """
        if value < 0.0:
            pylog.warning('Setting bad damping values. Should be positive!')
        else:
            self.parameters['b1'] = value
        pylog.info(
            'Changed damping constant for damper 1 to %s [N-s/rad]',
            self.parameters['b1'],
        )

    @property
    def b2(self):
        """ Get the value of damping constant for damper 2. [N-s/rad]
        Default is 0.5"""
        return self.parameters['b2']

    @b2.setter
    def b2(self, value: float):
        """ Keyword Arguments:
        value -- Set the value of damping constant for damper 2. [N-s/rad] """
        if value < 0.0:
            pylog.warning('Setting bad damping values. Should be positive!')
        else:
            self.parameters['b2'] = value
        pylog.info(
            'Changed damping constant for damper 2 to %s [N-s/rad]',
            self.parameters['b2'],
        )

    def show_parameters(self):
        return self.msg(self.parameters, self.units)


if __name__ == '__main__':
    P = PendulumParameters(g=9.81, L=1.)
    pylog.debug(P.show_parameters())