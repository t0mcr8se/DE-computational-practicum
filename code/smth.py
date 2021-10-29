import numpy as np
from numpy import exp

class NumericalMethod:
    """
    This class is abstract.
    It will be inherited by inherited by 'Euler', 'Heun', 'Runge' classes,
        and 'method' will be overridden for each of them.
    It was decided to make each method a classmethod ~ static methods,
        since there is no need to create an object of the class,
        and all calculations can be done using only input value.
    """

    @classmethod
    def exact_solution(cls, args):
        """
        Provides the exact solution for the equation
        with high precision.
        Calculations are made via NumPy.
        :param args: This dictionary must contain keys 'x0', 'y0', 'xn'
        :return:     'x' and exact 'y' values as arrays
        """
        x0 = args.get('x0')
        y0 = args.get('y0')
        xn = args.get('xn')

        x = np.linspace(x0, xn, 10 ** 3)
        y = cls.y(x, x0, y0)

        return x, y

    @classmethod
    def valid_input(cls, args) -> bool:
        """
        Here we can check that the input is valid:
        [x0, xn] is a subset of either (-inf, 0) or (0, +inf),
        number of steps has to be positive integer, and n0 < N.
        x0:    must be real number
        y0:    must be real number
        xn:    must be real number
        N:     must be positive integer
        n0:    must be positive integer
        steps: must be positive integer
        """
        x0 = args.get('x0')
        y0 = args.get('y0')
        xn = args.get('xn')
        steps = args.get('steps')
        n0 = args.get('n0')
        N = args.get('N')

        # Regular expressions for extracting integers and real numbers from the input
        import re
        is_int = lambda s: re.fullmatch(r"^([1-9]\d*|0)$", s) is not None
        is_real = lambda s: re.fullmatch(r"^([-+]?\d*\.?\d+)$", s) is not None

        if is_int(steps) and is_int(n0) and is_int(N):
            if is_real(x0) and is_real(y0) and is_real(xn):
                if (float(x0) < float(xn)) and (int(n0) < int(N)):
                    return 0 < float(x0) or float(xn) < 0

        return False

    @classmethod
    def f(cls, x, y):
        """
        It is given that y'(x,y) = f(x,y).
        This method is called only after valid_input().
        So that we dont need to check input.
        :param x: 'x' coordinate of (x, y)
        :param y: 'y' coordinate of (x, y)
        :return:  value of the derivative at a point (x,y)
        """
        return 3*y - x * (y ** (1/3))

    @classmethod
    def y(cls, x, x0, y0):
        """
        Since initial conditions are provided, we have y = y(x, x0, y0).
        :param x:  just 'x' coordinate
        :param x0: initial value
        :param y0: initial value
        :return:   value of the function at a point 'x'
        """
        C3 = (y0 ** (2/3) - x0/3 - 1/6) / exp(2*x0)
        return (x/3 + 1/6 + exp(2*x) * C3) ** (3/2)
        # return x*np.sin(x) + x*(y0 - x0*np.sin(x0))/x0

    @classmethod
    def apply(cls, args):
        """
        Here we calculate 'x' points, approximation points and truncation errors.
        :param args: A dictionary that is provided by user
        :return: 'x' points, approximation points and truncation errors
        """
        x0 = args.get('x0')
        y0 = args.get('y0')
        xn = args.get('xn')
        steps = args.get('steps')

        x = np.linspace(x0, xn, steps)
        y = cls.get_y_approx(x, y0)
        LTE = cls.get_lte(x, x0, y0)
        GTE = cls.get_gte(x, y, x0, y0)

        return x, y, LTE, GTE

    @classmethod
    def get_y_approx(cls, x: np.array, y0: float) -> np.array:
        """
        Here we calculate approximate function values at each 'x' point.
        We apply a certain numerical method iteratively.
        :param x:   an array of 'x' points
        :param y0:  initial condition for 'y0'. We can retrieve 'x0' from 'x'
        :return:    'y' approximations
        """
        y_approx = np.full(x.shape[0], y0, dtype = float)

        for i in range(1, x.shape[0]):
            y_approx[i] = cls.method(x[i - 1], y_approx[i - 1], x[1] - x[0])

        return y_approx

    @classmethod
    def get_lte(cls, x: np.array, x0: float, y0: float) -> np.array:
        """
        Here we calculate LTE at each 'x' point iteratively.
        :param x:   an array of 'x' points
        :param x0:  initial condition for 'x0'
        :param y0:  initial condition for 'y0'
        :return:    array of local truncations
        """
        lte = np.zeros(x.shape[0], dtype = float)

        for i in range(1, x.shape[0]):
            lte[i] = np.abs(cls.y(x[i], x0, y0) - cls.method(x[i - 1], cls.y(x[i - 1], x0, y0), x[1] - x[0]))

        return lte

    @classmethod
    def get_gte(cls, x: np.array, y_approx: np.array, x0: float, y0: float) -> np.array:
        """
        GTE[i] = |y[i] - y_approx[i]|
        :param x:        an array of 'x' coordinates
        :param y_approx: an array of approximations for a certain method
        :param x0:       initial value
        :param y0:       initial value
        :return:         an array of GTE for a certain method
        """
        return np.abs(cls.y(x, x0, y0) - y_approx)

    @classmethod
    def method(cls, x: float, y: float, h: float):
        """
        y_approx[i] = method(x[i-1], y[i-1], h)
        This function can be treated,for instance,
        as the Euler's method or Heun's method.
        It will be overridden for each numerical method.
        :param x: 'x' coordinate
        :param y: 'y' coordinate
        :param h: step size
        :return:  approximate value of a function at a point 'x + h'
        """
        pass


class Euler(NumericalMethod):
    @classmethod
    def method(cls, x: float, y: float, h: float):
        return y + h*cls.f(x, y)


class Heun(NumericalMethod):
    @classmethod
    def method(cls, x: float, y: float, h: float):
        k1 = cls.f(x, y)
        k2 = cls.f(x + h, y + k1*h)

        return y + (k1 + k2)*h/2


class Runge(NumericalMethod):
    @classmethod
    def method(cls, x: float, y: float, h: float):
        k1 = cls.f(x, y)
        k2 = cls.f(x + h/2, y + k1*h/2)
        k3 = cls.f(x + h/2, y + k2*h/2)
        k4 = cls.f(x + h, y + k3*h)

        return y + (k1 + 2*k2 + 2*k3 + k4)*h/6