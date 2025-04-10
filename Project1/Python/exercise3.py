
from util.run_closed_loop import run_single
from simulation_parameters import SimulationParameters
import os
import numpy as np
import farms_pylog as pylog
import matplotlib.pyplot as plt
from plotting_common import plot_time_histories


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
        headless=False,
        fast=False,
        drive = 2.0  ,
        weights_body2body = 15  ,
        weights_body2body_contralateral = 5  
        


    )

    pylog.info("Running the simulation")
    controller = run_single(
        all_pars
    )

    # Hint: Optionally you can use some helper function to generate the plots
    # such as (plot_time_histories)


if __name__ == '__main__':

    exercise3()

