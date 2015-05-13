"""Riemann Theta Tests

References
----------

.. [CRTF] B. Deconinck, M.  Heil, A. Bobenko, M. van Hoeij and M. Schmies,
   Computing Riemann Theta Functions, Mathematics of Computation, 73, (2004),
   1417-1442.

.. [DLMF] B. Deconinck, Digital Library of Mathematics Functions - Riemann Theta
   Functions, http://dlmf.nist.gov/21

.. [SAGE] Computing Riemann theta functions in Sage with applications.
   C. Swierczewski and B. Deconinck.Submitted for publication.  Available online
   at http://depts.washington.edu/bdecon/papers/pdfs/Swierczewski_Deconinck1.pdf

"""


import unittest
import numpy

from numpy.linalg import norm, cholesky
from abelfunctions.riemann_theta.radius import radius
from abelfunctions.riemann_theta.riemann_theta import RiemannTheta


class TestRiemannThetaValues(unittest.TestCase):
    def setup(self):
        pass

    def test_issue84_value(self):
        z = [0.5-1.10093687j, -0.11723434j]
        Omega = [[0.5+2j, 0.5+1j],
                 [0.5+1j, 1+1.5j]]

        theta_actual = 0.963179246467 - 6.2286820685j
        for _ in range(1000):
            theta = RiemannTheta(z,Omega)
            error = abs(theta - theta_actual)
            self.assertLess(error, 1e-5,
                            '%s not less than %s'
                            '\ntheta:  %s\nactual: %s'%(
                                error,1e-5,theta, theta_actual))

    def test_issue84_radius(self):
        Omega = [[0.5+2j, 0.5+1j],
                 [0.5+1j, 1+1.5j]]
        Omega = numpy.array(Omega)
        Y = Omega.imag
        T = cholesky(Y).T

        R_actual = 5.01708695504
        for _ in range(1000):
            R = radius(1e-8,T)
            error = abs(R - R_actual)
            self.assertLess(error, 1e-8)

    def test_gradient(self):
        Omega = [[1.j, 0.5, 0.5],
                 [0.5, 1.j, 0.5],
                 [0.5, 0.5, 1.j]]

        # generate random test z-values
        N = 32
        u = numpy.random.rand(N,3)
        v = numpy.random.rand(N,3)
        W = u + 1.0j*v

        # manually compute gradients
        dz0 = RiemannTheta(W,Omega,derivs=[[1,0,0]])
        dz1 = RiemannTheta(W,Omega,derivs=[[0,1,0]])
        dz2 = RiemannTheta(W,Omega,derivs=[[0,0,1]])
        grad1 = numpy.zeros_like(W, dtype=numpy.complex)
        grad1[:,0] = dz0
        grad1[:,1] = dz1
        grad1[:,2] = dz2

        # compute using "gradient"
        grad2 = RiemannTheta.gradient(W,Omega)
        self.assertLess(numpy.linalg.norm(grad1-grad2), 1e-14)


    # def test_value_at_point(self):
    #     Omega = np.array([[1.0 + 1.15700539j, -1.0 - 0.5773502693j],
    #                       [-1.0 - 0.5773502693j, 1.0 + 1.154700539j]],
    #                      dtype=numpy.complex)

    #     # first z-value
    #     z = np.array([1.0 - 1.0j, 1.0 + 1.0j])
    #     u = RiemannTheta.exponential_part(z, Omega)
    #     u_actual = 0
    #     u_delta = abs(u - u_actual)
    #     self.assertAlmostEqual(u_delta, 0)

    #     v = RiemannTheta.oscillatory_part(z, Omega)
    #     v_actual = 0
    #     v_delta = abs(v - v_actual)
    #     self.assertAlmostEqual(v_delta, 0)

    #     # second z-value
    #     z = np.array([1.0 - 1.0j, 1.0 + 1.0j])
    #     u = RiemannTheta.exponential_part(z, Omega)
    #     u_actual = 0
    #     u_delta = abs(u - u_actual)
    #     self.assertAlmostEqual(u_delta, 0)

    #     v = RiemannTheta.oscillatory_part(z, Omega)
    #     v_actual = 0
    #     v_delta = abs(v - v_actual)
    #     self.assertAlmostEqual(v_delta, 0)

    #     # same tests, different Omega
    #     Omega = np.array([[1.0 + 1.15700539j, -1.0 - 0.5773502693j],
    #                       [-1.0 - 0.5773502693j, 1.0 + 1.154700539j]],
    #                      dtype=numpy.complex)

    #     # first z-value
    #     z = np.array([1.0 - 1.0j, 1.0 + 1.0j])
    #     u = RiemannTheta.exponential_part(z, Omega)
    #     u_actual = 0
    #     u_delta = abs(u - u_actual)
    #     self.assertAlmostEqual(u_delta, 0)

    #     v = RiemannTheta.oscillatory_part(z, Omega)
    #     v_actual = 0
    #     v_delta = abs(v - v_actual)
    #     self.assertAlmostEqual(v_delta, 0)

    #     # second z-value
    #     z = np.array([1.0 - 1.0j, 1.0 + 1.0j])
    #     u = RiemannTheta.exponential_part(z, Omega)
    #     u_actual = 0
    #     u_delta = abs(u - u_actual)
    #     self.assertAlmostEqual(u_delta, 0)

    #     v = RiemannTheta.oscillatory_part(z, Omega)
    #     v_actual = 0
    #     v_delta = abs(v - v_actual)
    #     self.assertAlmostEqual(v_delta, 0)


    # def test_value_at_point_1_derivs(self):
    #     Omega = np.array([[1.0 + 1.15700539j, -1.0 - 0.5773502693j],
    #                       [-1.0 - 0.5773502693j, 1.0 + 1.154700539j]],
    #                      dtype=numpy.complex)

    #     # test 1
    #     derivs = [[1,0]]
    #     z = np.array([1.0 - 1.0j, 1.0 + 1.0j])
    #     u = RiemannTheta.exponential_part(z, Omega, derivs=derivs)
    #     u_actual = 0
    #     u_delta = abs(u - u_actual)
    #     self.assertAlmostEqual(u_delta, 0)

    #     v = RiemannTheta.oscillatory_part(z, Omega, derivs=derivs)
    #     v_actual = 0
    #     v_delta = abs(v - v_actual)
    #     self.assertAlmostEqual(v_delta, 0)

    #     # test 2
    #     derivs = [[0,1]]
    #     z = np.array([1.0 - 1.0j, 1.0 + 1.0j])
    #     u = RiemannTheta.exponential_part(z, Omega, derivs=derivs)
    #     u_actual = 0
    #     u_delta = abs(u - u_actual)
    #     self.assertAlmostEqual(u_delta, 0)

    #     v = RiemannTheta.oscillatory_part(z, Omega, derivs=derivs)
    #     v_actual = 0
    #     v_delta = abs(v - v_actual)
    #     self.assertAlmostEqual(v_delta, 0)


    # def test_value_at_point_2_derivs(self):
    #     Omega = np.array([[1.0 + 1.15700539j, -1.0 - 0.5773502693j],
    #                       [-1.0 - 0.5773502693j, 1.0 + 1.154700539j]],
    #                      dtype=numpy.complex)

    #     # test 1
    #     derivs = [[1,0]]
    #     z = np.array([1.0 - 1.0j, 1.0 + 1.0j])
    #     u = RiemannTheta.exponential_part(z, Omega, derivs=derivs)
    #     u_actual = 0
    #     u_delta = abs(u - u_actual)
    #     self.assertAlmostEqual(u_delta, 0)

    #     v = RiemannTheta.oscillatory_part(z, Omega, derivs=derivs)
    #     v_actual = 0
    #     v_delta = abs(v - v_actual)
    #     self.assertAlmostEqual(v_delta, 0)

    #     # test 2
    #     derivs = [[0,1]]
    #     z = np.array([1.0 - 1.0j, 1.0 + 1.0j])
    #     u = RiemannTheta.exponential_part(z, Omega, derivs=derivs)
    #     u_actual = 0
    #     u_delta = abs(u - u_actual)
    #     self.assertAlmostEqual(u_delta, 0)

    #     v = RiemannTheta.oscillatory_part(z, Omega, derivs=derivs)
    #     v_actual = 0
    #     v_delta = abs(v - v_actual)
    #     self.assertAlmostEqual(v_delta, 0)


    # def test_zeroCharacteristic(self):
    #     #Replace with random z, omega, or set of such
    #     z = np.array([1.0j, 0])
    #     omega = np.matrix(
    #         [[1.0j, -0.5],
    #         [-0.5, 1.0j]]
    #         )
    #     char = [[0,0],[0,0]]
    #     thetaValue = theta.value_at_point(z, omega, batch = False)
    #     thetaCharValue = theta.characteristic(char, z, omega)
    #     delta = scipy.linalg.norm(thetaValue - thetaCharValue, np.inf)
    #     self.assertAlmostEqual(delta,0)

    # def test_jacobiTheta1(self):
    #     #Test against sympy mpmath.jtheta(1,z)
    #     z = 1.0j
    #     q_omega = .1
    #     char = [[.5],[.5]]
    #     jTheta1 = jtheta(1, np.pi * z, q_omega)
    #     thetaValue = theta.characteristic(char, z, q_omega)
    #     self.assertAlmostEqual(jTheta1, -thetaValue)


    # def test_jacobiTheta2(self):
    #     #Test against sympy mpmath.jtheta(2,z)
    #     z = 1.0j
    #     q_omega = .1
    #     char = [[.5],[0]]
    #     jTheta2 = jtheta(2, np.pi * z, q_omega)
    #     thetaValue = theta.characteristic(char, z, q_omega)
    #     self.assertAlmostEqual(jTheta2, thetaValue)

    # def test_jacobiTheta3(self):
    #     #Test against sympy mpmath.jtheta(3,z)
    #     z = 1.0j
    #     q_omega = .1
    #     char = [[0],[0]]
    #     jTheta3 = jtheta(3, np.pi * z, q_omega)
    #     thetaValue = theta.characteristic(char, z, q_omega)
    #     self.assertAlmostEqual(jTheta3, thetaValue)

    # def test_jacobiTheta4(self):
    #     #Test against sympy mpmath.jtheta(4,z)
    #     z = 1.0j
    #     q_omega = .1
    #     char = [[0],[.5]]
    #     jTheta3 = jtheta(4, np.pi * z, q_omega)
    #     thetaValue = theta.characteristic(char, z, q_omega)
    #     self.assertAlmostEqual(jTheta3, thetaValue)

    # def test_zParity(self):
    #     z = np.array([1.0j, 0])
    #     omega = np.matrix(
    #         [[1.0j, -0.5],
    #         [-0.5, 1.0j]]
    #         )
    #     theta1 = theta.value_at_point(z, omega, batch = False)
    #     theta2 = theta.value_at_point(-z, omega, batch = False)
    #     self.assertAlmostEqual(theta1,theta2)

    # def test_zIntShift(self):
    #     z = np.array([1.0j, 0])
    #     omega = np.matrix(
    #         [[1.0j, -0.5],
    #         [-0.5, 1.0j]]
    #         )
    #     m = np.array([1, 1])
    #     theta1 = theta.value_at_point(z, omega, batch = False)
    #     theta2 = theta.value_at_point(z + m, omega, batch = False)
    #     self.assertAlmostEqual(theta1,theta2)

    # def test_quasiPeriodic(self):
    #     #Test for DLMF 21.3.3
    #     pass

    # def test_characteristicShift(self):
    #     #Test for DLMF 21.3.4
    #     pass

    # def test_halfperiodCharacteristic(self):
    #     #Test for DLMF 21.3.6
