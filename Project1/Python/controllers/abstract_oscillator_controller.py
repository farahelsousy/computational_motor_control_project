"""Oscillator network ODE"""

import numpy as np
import scipy.stats as ss
from farms_core import pylog

class AbstractOscillatorController:
    """zebrafish controller for the abstract oscillator CPG (Question 3)"""

    def __init__(self, pars):
        super().__init__()

        # Simulation parameters
        self.pars = pars
        self.n_iterations = pars.n_iterations
        self.timestep = pars.timestep
        self.times = np.linspace(0, self.n_iterations * self.timestep, self.n_iterations)

        # Number of actively controlled joints (0 to 12); joints 13–14 remain passive
        self.n_actuated_joints = 13
        self.n_oscillators = 2 * self.n_actuated_joints   # 26 oscillators total

        # State dimension: phases + amplitudes for each oscillator
        self.n_eq = self.n_oscillators * 2
        self.state = np.zeros((self.n_iterations, self.n_eq))
        self.dstate = np.zeros(self.n_eq)

        # Indexing for phases and amplitudes
        self.oscillator_phase_l     = np.arange(0, self.n_actuated_joints)
        self.oscillator_phase_r     = self.n_actuated_joints + np.arange(0, self.n_actuated_joints)
        self.oscillator_phase_all   = np.arange(0, 2 * self.n_actuated_joints)
        self.oscillator_amplitude_l = 2 * self.n_actuated_joints + np.arange(0, self.n_actuated_joints)
        self.oscillator_amplitude_r = 3 * self.n_actuated_joints + np.arange(0, self.n_actuated_joints)
        self.oscillator_amplitude_all = 2 * self.n_actuated_joints + np.arange(0, 2 * self.n_actuated_joints)

        # Initial phases: linearly spaced if not provided
        if self.pars.initial_phases is None:
            self.state[0, :self.n_actuated_joints] = np.linspace(2*np.pi, 0, self.n_actuated_joints)
            self.state[0, self.n_actuated_joints:2*self.n_actuated_joints] = np.linspace(np.pi, -np.pi, self.n_actuated_joints)
        else:
            self.state[0, :2*self.n_actuated_joints] = self.pars.initial_phases

        # Start amplitudes at zero (will ramp toward R_i)
        self.state[0, self.n_oscillators:2*self.n_oscillators] = 0

        # Motor output storage and mapping to left/right muscles
        self.motor_out = np.zeros((self.n_iterations, self.n_oscillators))
        self.motor_l = 2 * np.arange(0, self.n_actuated_joints)
        self.motor_r = self.motor_l + 1

        # ODE and step functions
        self.f = self.network_ode
        self.step = self.step_euler

        # Four zeros for the two passive joints (4 muscles)
        self.zeros4 = np.zeros(4)

    def network_ode(self, state):
        """Compute derivatives of phases and amplitudes."""
        if state.ndim > 1:
            current_state = state.flatten()
        else:
            current_state = state

        n = self.n_oscillators
        dphases = np.zeros(n)
        damplitudes = np.zeros(n)

        # Parameters
        drive = self.pars.drive
        f = self.pars.cpg_frequency_gain * drive + self.pars.cpg_frequency_offset
        w_bb = self.pars.weights_body2body
        w_bbc = self.pars.weights_body2body_contralateral
        phi_lag = self.pars.phase_lag_body / (self.n_actuated_joints - 1) if self.n_actuated_joints > 1 else 0
        amp_rate = self.pars.amplitude_rates
        amp_gain = self.pars.cpg_amplitude_gain

        for i in range(n):
            θ_i = current_state[i]
            r_i = current_state[i + n]

            # coupling
            coupling = 0
            for j in range(n):
                if i == j:
                    continue
                θ_j = current_state[j]
                r_j = current_state[j + n]

                if abs(i - j) == 2:
                    w_ij, φ_ij = w_bb, np.sign(i - j) * phi_lag
                elif (j - i == 1) and (i % 2 == 0):
                    w_ij, φ_ij = w_bbc, -np.pi
                else:
                    w_ij, φ_ij = 0, 0

                if w_ij != 0:
                    coupling += w_ij * r_j * np.sin(θ_j - θ_i - φ_ij)

            dphases[i] = 2 * np.pi * f + coupling

            # nominal amplitude for oscillator i
            if isinstance(amp_gain, (list, np.ndarray)):
                joint_gain = amp_gain[i // 2]
            else:
                joint_gain = amp_gain
            R_i = joint_gain * drive

            damplitudes[i] = amp_rate * (R_i - r_i)

        return np.concatenate([dphases, damplitudes])

    def motor_output(self, iteration):
        """Compute muscle activations for active joints only."""
        out = np.zeros(self.n_oscillators)
        G = self.pars.motor_output_scaling

        for i in range(self.n_actuated_joints):
            θ_l = self.state[iteration, self.oscillator_phase_l[i]]
            θ_r = self.state[iteration, self.oscillator_phase_r[i]]

            # --- FIXED: use amplitude state directly, without extra * drive ---
            r_l = self.state[iteration, self.oscillator_amplitude_l[i]]
            r_r = self.state[iteration, self.oscillator_amplitude_r[i]]

            out[self.motor_l[i]] = G * r_l * (1 + np.cos(θ_l))
            out[self.motor_r[i]] = G * r_r * (1 + np.cos(θ_r))

        self.motor_out[iteration, :] = out
        return out

    def step_euler(self, iteration, timestep):
        """Perform one Euler integration step and return full muscle activation vector."""
        self.state[iteration+1, :] = self.state[iteration, :]
        self.dstate = self.f(self.state[iteration, :])
        self.state[iteration+1, :] += timestep * self.dstate
        self.motor_output(iteration+1)
        return np.concatenate([ self.motor_out[iteration+1, :], self.zeros4 ])
