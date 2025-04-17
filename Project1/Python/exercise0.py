
import plotting_common
from util.run_closed_loop import run_single, run_multiple
from simulation_parameters import SimulationParameters
import matplotlib.pyplot as plt
import os
import farms_pylog as pylog
import numpy as np
import matplotlib
matplotlib.rc('font', **{"size": 15})


def exercise0():

    pylog.info("Implement ex 0")
    log_path = './logs/exercise0/'
    os.makedirs(log_path, exist_ok=True)

    pars = SimulationParameters(
        n_iterations=5001,
        controller="sine",
        amp=0.3,
        twl=1,
        freq=3,
        compute_metrics="all",
        headless=True,
        video_record=False,
        log_path=log_path,
        return_network=True,
    )

    controller = run_single(
        pars
    )

    # Plot left and right motor outputs
    plt.figure('Exercise0_Left_Right_activations', figsize=[10, 10])
    plotting_common.plot_left_right(
        controller.times,
        controller.motor_out,
        controller.motor_l,
        controller.motor_r
    )

    # Plot head trajectory
    plt.figure('Exercise0_Head_Trajectory', figsize=[10, 10])
    plotting_common.plot_trajectory(
        controller,
        )
    
    # Plot 

    
    # # Run multiple simulations
    # nsim = 2
    # pars_list = [
    #     SimulationParameters(
    #         simulation_i=(nsim*i+j)*nsim+k,
    #         n_iterations=5001,
    #         controller="sine",
    #         amp=A,
    #         twl=eps,
    #         freq=f,
    #         compute_metrics="all",
    #         headless=True,
    #         video_record=False,
    #         log_path=log_path,
    #         return_network=True,
    #         print_metrics=False,
    #     )
    #     for i, A in enumerate(np.linspace(0, 2, nsim))
    #     for j, eps in enumerate(np.linspace(0, 2, nsim))
    #     for k, f in enumerate(np.linspace(1, 5, nsim))
    # ]

    # controllermultiple = run_multiple(
    #     pars_list
    # )




if __name__ == '__main__':
    exercise0()
    plt.show()

    

