
from plotting_common import plot_time_histories, save_figures
from util.run_closed_loop import run_single, run_multiple
from simulation_parameters import SimulationParameters
import matplotlib.pyplot as plt
import os
import farms_pylog as pylog
import numpy as np
import matplotlib
matplotlib.rc('font', **{"size": 15})


num_process = 24  # number of processes to run in parallel
ylim_amp = [0, 0.01]


def exercise1():

    pylog.info("Ex 1")
    pylog.info("Implement exercise 1")
    prepath = './logs/exercise1/'
    pars = SimulationParameters(
        gravity=[0, 0, 0],
        joint_poses=0.3*np.ones(15),
        animal_pose=[0, 0, -0.01, 0, 0, -1.570796327],
        
        n_iterations=5001,
        video_record=False,
        log_path=prepath,

        compute_metrics='mechanical',
        print_metrics=False,
        return_network=True,headless=True,
        )
    #test
    
    controller = run_single(pars)
    for i in range(0, 5001):
        controller.step(i, pars.timestep)
    # make 2 list of right and left indexes
    left = []
    right = []
    for i in range(0, pars.n_total_joints, 2):
        left.append(i)
        right.append(i + 1)
    # plot the left and right muscle activations
    plot_time_histories(
        times=controller.times,
        state=controller.motor_out,
        left_idx=left,
        right_idx=right,
        ylim=ylim_amp,
        title='Muscle activations',
        xlabel='Time (s)',
        ylabel='Activation',
        save_path=os.path.join(prepath, 'activations.png'))
    
if __name__ == '__main__':

    exercise1()
    plt.show()
