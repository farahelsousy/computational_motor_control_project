
import plotting_common
from util.run_closed_loop import run_single
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
    print(log_path)
    pars = SimulationParameters(
        n_iterations=10001,
        controller="sine",
        amp=0.3,
        twl=0.4,
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
    
    plotting_common.plot_trajectory(controller=controller,label='Trajectory')
    """
    plotting_common.plot_left_right(
        controller.times,
        controller.motor_out,
        controller.motor_l,
        controller.motor_r,
    )
    plotting_common.plot_time_histories(
      
    controller.times[2500:], 
    controller.joints_positions[2500:], 
    labels=[f"Joint {i+1}" for i in range(controller.joints_positions.shape[1])]
    )
    print(np.mean(controller.joints_positions, axis=0))
    """
if __name__ == '__main__':

    exercise0()
    plt.show()

