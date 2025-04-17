
from plotting_common import plot_time_histories, plot_1d, save_figures
from util.run_closed_loop import run_single, run_multiple
from util.rw import load_object
from simulation_parameters import SimulationParameters
import matplotlib.pyplot as plt
import os
import farms_pylog as pylog
import numpy as np
import matplotlib
matplotlib.rc('font', **{"size": 15})


num_process = 4 # number of processes to run in parallel, it seems, that it shouldn't be higher than 6
ylim_amp = [0, 0.01]


def exercise1(subexercise=2, n_freq_se_3=1):
    pylog.info("Ex 1")

    if subexercise == 2:
        pylog.info("Exercise 1.2")
        log_path = './logs/exercise1/exercise1_2/'
        os.makedirs(log_path, exist_ok=True)

        # Run exercise 2.2 (1.2)
        pars = SimulationParameters(
            n_iterations=5001,
            controller="sine",
            amp=0,
            twl=0,
            freq=3,
            gravity = [0, 0, 0],
            compute_metrics="all",
            headless=True,
            video_record=False,
            log_path=log_path,
            return_network=True,
            joint_poses = 0.3*np.ones(15) ,
            animal_pose = [0.0, 0.0, 0.1, 0.0, 0, -1.570796327],
            damping_factor = 1.0
        )

        controller = run_single(
            pars
        )
    elif subexercise == 3:
        # Exercise 1.3
        pylog.info("Exercise 1.3")
        log_path = './logs/exercise1/exercise1_3/'
        os.makedirs(log_path, exist_ok=True)

        # Number of frequencies to simulate
        nsim_freq = n_freq_se_3 #10
        nsim_DR = 3
        nsim_TWL = 2 

        pars_list = [
            SimulationParameters(
                simulation_i=((p*nsim_TWL+k)*nsim_DR+j)*nsim_freq+i, #simulation_i=((nsim_DR*i+j)*nsim_env+k)*nsim_TWL+p
                controller="sine",
                n_iterations=5001,
                amp=0.01,
                twl=TWL,
                freq=freq,
                gravity = [0, 0, 0],
                compute_metrics="all",
                headless=True,
                video_record=False,
                log_path=log_path,
                return_network=True,
                joint_poses = 0.3*np.ones(15) ,
                animal_pose = [0.0, 0.0, 0.01*env, 0.0, 0, -1.570796327],
                damping_factor = DR,
                print_metrics=False
            )
            for i, freq in enumerate(np.linspace(0, 20, nsim_freq))      
            for j, DR in enumerate(np.array([1,0.3,0.1]))
            for p, env in enumerate(np.array([10,-1])) 
            for k, TWL in enumerate(np.array([0,0.5]))
        ]

        controller_multiple=run_multiple(pars_list, num_process)

    elif subexercise == 4:
        # Exercise 1.4
        pylog.info("Exercise 1.4")
        log_path = './logs/exercise1/exercise1_4/'
        os.makedirs(log_path, exist_ok=True)
        
        # Number of frequencies to simulate
        nsim_freq = 37
        nsim_TWL = 10
        nsim_muscle = 3 #2 

        pars_list_E14 = [
            SimulationParameters(
                simulation_i=(nsim_TWL*i+j)*nsim_muscle+k,
                controller="sine",
                n_iterations=5001,
                amp=0.5,
                twl=TWL,
                freq=freq,
                compute_metrics="all",
                headless=True,
                video_record=False,
                log_path=log_path,
                return_network=True,
                joint_poses = 0.3*np.ones(15) ,
                print_metrics=False,
                muscle_parameters_tag=muscle,
            )
            for i, freq in enumerate(np.linspace(3, 40, nsim_freq))
            for j, TWL in enumerate(np.linspace(0, 2, nsim_TWL))      #enumerate(np.array([1,-1]))
            for k, muscle in enumerate(np.array(["FN_5000_ZC_1000_G0_419","FN_7500_ZC_1000_G0_419","FN_10000_ZC_1000_G0_419"]))      #enumerate(np.array([0,0.5]))
        ]
        
        controller_multiple=run_multiple(pars_list_E14, num_process)
        return
    else:
        pylog.info("No subexercise selected")
        return

def plot_amplitudes_E1_3(n_freq, start_idx, logdir, title):
    """
    Example showing how to load a simulation file and use the plot2d function
    """
    pylog.info(
        "Example showing how to load the simulation file and use the plot2d function")
    # n_freq = number of frequnecies
    # start_idx = index of the first controller to load
    # logdir = directory where the simulation files are stored
    # title = title of the plot

    n_DR = 3    # Number of damping ratios

    # Step 1, for each damping ratio make a matrix with the mean amplitudes as a function of frequnecies
    mat_freq = np.zeros((n_freq,n_DR))
    mat_amp = np.zeros((n_freq,n_DR))
    DR = np.zeros((n_DR))

    for i in range(n_DR):
        for j in range(n_freq):
            # load controller
            controller = load_object(logdir+"controller"+str(i*n_freq+j+start_idx))
            # get the mean amplitude for each frequency
            mat_freq[j,i] = controller.pars.freq
            mat_amp[j,i] = np.mean(controller.metrics["mech_joint_amplitudes"])
        # Example vector
        DR[i] = controller.pars.damping_factor

    # Create an array of text containing legends for the damping ratios
    DR_legends = [f"DR = {value}" for value in DR]

    # Step 2, plot each of the matrices in the same plot. Set x-axis as frequency and y-axis as mean amplitude. and y-axis as mean amplitude.
    plt.figure(title, figsize=[10, 10])
    plt.plot(mat_freq, mat_amp, marker='o', markersize=5, label=DR_legends)

    # Add legends designating the damping ratio.
    plt.figure(title, figsize=[10, 10])
    plt.title(title)
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Mean amplitude [m]")
    plt.legend(loc='upper right')
    plt.grid()
    plt.xlim([np.min(mat_freq), np.max(mat_freq)])

    save_figures()


if __name__ == '__main__':
    # Chosen subexercise:
    subexercise = 4 # 2, 3, 4, 31, 41
    n_freq_se_3 = 100 # Number of frequencies to simulate in exercise 1.3
    exercise1(subexercise=subexercise,n_freq_se_3=n_freq_se_3)

    # Plotting
    
    if subexercise == 31:
        plot_amplitudes_E1_3(n_freq_se_3, 0, './logs/exercise1/exercise1_3/', "E2.3, TWL = 0, Env = air")
        plot_amplitudes_E1_3(n_freq_se_3, n_freq_se_3*3, './logs/exercise1/exercise1_3/', "E2.3, TWL = 0.5, Env = air")
        plot_amplitudes_E1_3(n_freq_se_3, n_freq_se_3*6, './logs/exercise1/exercise1_3/', "E2.3, TWL = 0, Env = water")
        plot_amplitudes_E1_3(n_freq_se_3, n_freq_se_3*9, './logs/exercise1/exercise1_3/', "E2.3, TWL = 0.5, Env = water")