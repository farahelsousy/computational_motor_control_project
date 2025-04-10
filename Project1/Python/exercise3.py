
from util.run_closed_loop import run_single
from simulation_parameters import SimulationParameters
import os
import numpy as np
import farms_pylog as pylog
import matplotlib.pyplot as plt
from plotting_common import plot_time_histories
import plotting_common

def exercise3():

    pylog.info("Ex 3")
    pylog.info("Implement exercise 3")
    log_path = './logs/exercise3/'  # path for logging the simulation data
    os.makedirs(log_path, exist_ok=True)

    all_pars = SimulationParameters(
        n_iterations=5001,
        controller="abstract oscillator",
        log_path=log_path,
        compute_metrics=None,
        print_metrics=False,
        return_network=True,
        headless=True,
        fast=False,
        drive = 1,  # drive to the abstract oscillator controller
        cpg_frequency_gain = 0.6,
        cpg_frequency_offset = 0.6,
        n_passive_joints = 2 ,
        cpg_amplitude_gain = 0.125 * np.ones(13),  # amplitude gain for each joint
        # Coupling weigths between neighborhood segments
        weights_body2body = 30,
        # Coupling weigths between contralateral segments
        weights_body2body_contralateral = 10,
        phase_lag_body = 2*np.pi,  # Total phase lag from body to tail along the spine
        amplitude_rates = 20 , # Convergence rates of amplitudes


        motor_output_scaling = 1  # muscle force scaling factor G

        


    )

    pylog.info("Running the simulation")
    controller = run_single(
        all_pars
    )
    plotting_common.plot_left_right(
        controller.times,
        controller.motor_out,
        controller.motor_l,
        controller.motor_r,
    )

    # Hint: Optionally you can use some helper function to generate the plots
    # such as (plot_time_histories)


if __name__ == '__main__':

    exercise3()
    plt.show()

