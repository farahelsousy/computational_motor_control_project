
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
        n_iterations=5001,
        controller="sine",
        amp=0.3,
        twl=0.4,
        freq=3,
        compute_metrics="all",
        headless=False,
        video_record=False,
        log_path=log_path,
        return_network=True,
        
    )

    controller = run_single(
        pars
    )
    for i in range(0, 5001):
        controller.step(i, pars.timestep)
    #make 2 list of right and left indexes
    left = []    
    right = []    
    for i in range(0, pars.n_total_joints, 2):
        left.append(i)
        right.append(i+1)

    plotting_common.plot_left_right(times=controller.times,
                                        state=controller.motor_out,left_idx=left,right_idx=right)
if __name__ == '__main__':

    exercise0()
    plt.show()

