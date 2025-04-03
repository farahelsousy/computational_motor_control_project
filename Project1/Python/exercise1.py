
from plotting_common import plot_time_histories, save_figures
import plotting_common
from util.run_closed_loop import run_single, run_multiple
from simulation_parameters import SimulationParameters
import matplotlib.pyplot as plt
import os
import farms_pylog as pylog
import numpy as np
import matplotlib
matplotlib.rc('font', **{"size": 15})
from util.rw import load_object
num_process = 24  # number of processes to run in parallel
ylim_amp = [0, 0.01]


def exercise1():

    pylog.info("Ex 1")
    pylog.info("Implement exercise 1")
    prepath = './logs/exercise1/'
    pars =[ SimulationParameters(
        simulation_i= i*num_process  + j,
        gravity=[0, 0, 0],
        joint_poses=0.3*np.ones(15),
        animal_pose=[0, 0, -0.01, 0, 0, -1.570796327],
        headless=True,
        n_iterations=5001,
        video_record=False,
        log_path=prepath,
        controller="sine",
        amp=0.01,
        freq=f,
        twl=0,
        damping_factor=d,
        compute_metrics='mechanical',
        print_metrics=True,
        return_network=True,
        )for i,f in enumerate(np.linspace(0, 20, 2))
        for j ,d in enumerate([1.0,0.3,0.1])
    
        
        ]
    #test
    
    controller = run_multiple(pars, num_process=num_process)
    figure_labels = []
    
    # Generate and save plots for each controller
    for p in pars:
        # Load the controller for the current simulation
        c = load_object(prepath + "controller" + str(p.simulation_i))
        
        # Create a unique label for the plot
        label = f"Trajectory_{p.simulation_i}"
        
        # Plot the trajectory using the label
        plotting_common.plot_trajectory(controller=c)
        plt.figure(label)
    plotting_common.save_figures()
        
    
    # Save the generated figures using save_figures
    print(figure_labels)
    plotting_common.save_figures(figures=figure_labels, folder='results', extensions=['png'])

if __name__ == '__main__':

    exercise1()
    plt.show()
