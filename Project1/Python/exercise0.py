
import plotting_common
from util.run_closed_loop import run_multiple
from util.rw import load_object
from simulation_parameters import SimulationParameters
import matplotlib.pyplot as plt
import os
import farms_pylog as pylog
import numpy as np
import matplotlib
matplotlib.rc('font', **{"size": 15})

num_process = 4 # number of processes to run in parallel.

def exercise0(parameters=np.array([0,0,0]),metrics=False,headless=True):
    """
    Run the simulation for Exercise 0 (Exercise 1.1) with the given parameters.
    Parameters:
        parameters: np.array of shape (n,3) with n the number of simulations to run.
                    Each row should contain [Amplitude, Frequency, Twl].
        metrics: bool, whether to print metrics or not.
        headless: bool, whether to run the simulation in headless mode or not.
    """

    pylog.info("Running Exercise 0 (Exercise 1.1)")
    log_path = './logs/exercise0/'
    os.makedirs(log_path, exist_ok=True)

    pars_list = [
        SimulationParameters(
            simulation_i=i,
            n_iterations=5001,
            controller="sine",
            amp=row[0],
            freq=row[1],
            twl=row[2],
            compute_metrics="all",
            print_metrics=metrics,
            headless=headless,
            video_record=False,
            log_path=log_path,
            return_network=True,
        )
        for i, row in enumerate(parameters)
    ]
    
    controller_multiple = run_multiple(pars_list, num_process)


def plotsExercise0(n_sim=0):
    """
    Plot the results of the simulations.
    """
    pylog.info("Plotting Exercise 0 (Exercise 1.1)")

    for i in range(n_sim):
        # Load the controller object
        controller = load_object('./logs/exercise0/controller'+str(i))

        # Load relevant parameters 
        amp = controller.pars.amp
        freq = controller.pars.freq
        twl = controller.pars.twl

        # Plot left and right motor outputs
        plt.figure('E1_1_LR_activations_[A,f,twl]='+str(np.array([amp,freq,twl])), figsize=[10, 10])
        plotting_common.plot_left_right(
            controller.times,
            controller.motor_out,
            controller.motor_l,
            controller.motor_r,
        )

        plotting_common.save_figures()

        # Plot head trajectory
        plt.figure('E1_1_Head_Traj_[A,f,twl]='+str(np.array([amp,freq,twl])), figsize=[10, 10])
        plotting_common.plot_trajectory(
            controller,
        )

        plotting_common.save_figures()

        # Plot joint angle evolution
        plt.figure('E1_1_Joint_Angles_[A,f,twl]='+str(np.array([amp,freq,twl])), figsize=[10, 10])
        plotting_common.plot_time_histories(
            controller.times,
            controller.joints_positions,
            ylabel="Joint angles [rad]",
        )
        plotting_common.save_figures()


if __name__ == '__main__':
    # Define values to be examined:
    parameters = np.array([[0.3,2,1.5],[1,4,0.5]]) # [[Amplitude, Frequency, Twl],...]

    # Define whether to print metrics and/or plot the results
    metrics = False
    plot = True

    # Run exerise0
    exercise0(parameters=parameters,metrics=True,headless=True)

    # Plot the results of the simulation if selected. 
    if plot:
        plotsExercise0(n_sim=np.size(parameters,0))


    

