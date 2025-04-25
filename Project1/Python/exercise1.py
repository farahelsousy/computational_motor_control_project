
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


num_process = 4 # number of processes to run in parallel.
ylim_amp = [0, 0.01]


def exercise1(subexercise=2, n_freq_se_3=1,n_freq_se_4=1,n_TWL_se_4=1):
    pylog.info("Ex 1")

    if subexercise == 2:
        pylog.info("Exercise 1.2")
        log_path = './logs/exercise1/exercise1_2/'
        os.makedirs(log_path, exist_ok=True)

        # Run exercise 2.2 (1.2)
        pars_list = [
            SimulationParameters(
                simulation_i=i,
                n_iterations=301,
                controller="sine",
                amp=0,
                twl=0,
                freq=0,
                gravity = [0, 0, 0],
                compute_metrics="all",
                headless=True,
                video_record=False,
                log_path=log_path,
                return_network=True,
                joint_poses = 0.3*np.ones(15) ,
                animal_pose = [0.0, 0.0, 0.1, 0.0, 0, -1.570796327],
                damping_factor = DR
            )
            for i, DR in enumerate(np.array([1,0.3,0.1]))
        ]

        controller_multiple=run_multiple(pars_list, num_process)

    elif subexercise == 3:
        # Exercise 1.3
        pylog.info("Exercise 1.3")
        log_path = './logs/exercise1/exercise1_3/'
        os.makedirs(log_path, exist_ok=True)

        # Number of the individual parameters to simulate
        nsim_freq = n_freq_se_3 
        nsim_DR = 3
        nsim_TWL = 2 

        pars_list = [
            SimulationParameters(
                simulation_i=((p*nsim_TWL+k)*nsim_DR+j)*nsim_freq+i,
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
                return_network=False,
                joint_poses = 0.3*np.ones(15),
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
        nsim_freq = n_freq_se_4
        nsim_TWL = n_TWL_se_4

        pars_list_E14 = [
            SimulationParameters(
                simulation_i= (k*nsim_TWL+j)*nsim_freq+i,
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
            for j, TWL in enumerate(np.linspace(0, 2, nsim_TWL))  
            for k, muscle in enumerate(np.array(["FN_5000_ZC_1000_G0_419","FN_7500_ZC_1000_G0_419","FN_10000_ZC_1000_G0_419"]))      #enumerate(np.array([0,0.5]))
        ]
        
        controller_multiple=run_multiple(pars_list_E14, num_process)
        return
    else:
        pylog.info("No subexercise selected")
        return

def plot_E1_2(logdir):
    n_DR = 3    # Number of damping ratios

    for i in range(n_DR):
        # Load the controller object
        controller = load_object(logdir+"controller"+str(i))
        DR = controller.pars.damping_factor


        plt.figure('E2_2_Joint_Angles_DR_'+str(DR), figsize=[10, 10])
        plot_time_histories(
            controller.times,
            controller.joints_positions,
            ylabel="Joint angles [rad]"
        )

        # Add grid
        plt.minorticks_on()
        plt.grid(which='major', color='darkgrey', linestyle='-', linewidth=0.75)
        plt.grid(which='minor', color='gray', linestyle=':', linewidth=0.5)

        # Save figure
        save_figures()

def plot_amplitudes_E1_3(n_freq, start_idx, logdir, title):
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
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Mean amplitude")
    plt.legend(loc='upper right')
    plt.minorticks_on()
    plt.grid(which='major', color='darkgrey', linestyle='-', linewidth=0.75)
    plt.grid(which='minor', color='gray', linestyle=':', linewidth=0.5)
    plt.xlim([np.min(mat_freq), np.max(mat_freq)])

    save_figures()

def plot_E1_4(n_freq, n_twl, start_idx, logdir, title):
    # n_freq = number of frequnecies¨
    # n_twl = number of TWL
    # start_idx = index of the first controller to load
    # logdir = directory where the simulation files are stored
    # title = title of the plot

    # Step 1, for each damping ratio make a matrix with the mean amplitudes as a function of frequnecies
    mat_freq = np.zeros((n_freq,n_twl))
    mat_speed = np.zeros((n_freq,n_twl))
    mat_cot = np.zeros((n_freq,n_twl))
    TWL = np.zeros((n_twl))

    for i in range(n_twl):
        for j in range(n_freq):
            # load controller
            controller = load_object(logdir+"controller"+str(i*n_freq+j+start_idx))
            # get the mean amplitude for each frequency
            mat_freq[j,i] = controller.pars.freq
            mat_speed[j,i] = np.mean(controller.metrics["mech_speed_fwd"])
            mat_cot[j,i] = np.mean(controller.metrics["mech_cot"])
        # Example vector
        TWL[i] = controller.pars.twl

    # Create an array of text containing legends for the damping ratios
    TWL_legends = [f"TWL = {value:.2f}" for value in TWL]

    # Step 2, plot each of the matrices in the same plot. Set x-axis as frequency and y-axis as mean amplitude. and y-axis as mean amplitude.
    plt.figure(title+"_speed", figsize=[10, 10])
    plt.plot(mat_freq, mat_speed, marker='o', markersize=5, label=TWL_legends)

    # Add legends designating the damping ratio.
    plt.figure(title+"_speed", figsize=[10, 10])
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Forward speed")
    plt.legend(loc='upper right')
    plt.minorticks_on()
    plt.grid(which='major', color='darkgrey', linestyle='-', linewidth=0.75)
    plt.grid(which='minor', color='gray', linestyle=':', linewidth=0.5)
    plt.xlim([np.min(mat_freq), np.max(mat_freq)])

    save_figures()

    # Step 2, plot each of the matrices in the same plot. Set x-axis as frequency and y-axis as mean amplitude. and y-axis as mean amplitude.
    plt.figure(title+"_CoT", figsize=[10, 10])
    plt.plot(mat_freq, mat_cot, marker='o', markersize=5, label=TWL_legends)

    # Add legends designating the damping ratio.
    plt.figure(title+"_CoT", figsize=[10, 10])
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Cost of Transport")
    plt.legend(loc='upper right')
    plt.minorticks_on()
    plt.grid(which='major', color='darkgrey', linestyle='-', linewidth=0.75)
    plt.grid(which='minor', color='gray', linestyle=':', linewidth=0.5)
    plt.xlim([np.min(mat_freq), np.max(mat_freq)])

    save_figures()


if __name__ == '__main__':
    # Chosen subexercise:
    subexercise = 21 # 2, 3, 4, 21, 31, 41

    n_freq_se_3 = 80    # Number of frequencies to simulate in exercise 1.3
    n_freq_se_4 = 15    # Number of frequencies to simulate in exercise 1.4
    n_TWL_se_4 = 10     # Number of TWL to simulate in exercise 1.4

    exercise1(subexercise=subexercise,n_freq_se_3=n_freq_se_3,n_freq_se_4=n_freq_se_4,n_TWL_se_4=n_TWL_se_4)

    # Plotting
    if subexercise == 21:
        plot_E1_2('./logs/exercise1/exercise1_2/')
    
    if subexercise == 31:
        plot_amplitudes_E1_3(n_freq_se_3, 0, './logs/exercise1/exercise1_3/', "E2_3_TWL_0_Env_air")
        plot_amplitudes_E1_3(n_freq_se_3, n_freq_se_3*3, './logs/exercise1/exercise1_3/', "E2_3_TWL_0.5_Env_air")
        plot_amplitudes_E1_3(n_freq_se_3, n_freq_se_3*6, './logs/exercise1/exercise1_3/', "E2_3_TWL_0_Env_water")
        plot_amplitudes_E1_3(n_freq_se_3, n_freq_se_3*9, './logs/exercise1/exercise1_3/', "E2_3_TWL_0.5_Env_water")

    if subexercise == 41:
        plot_E1_4(n_freq_se_4, n_TWL_se_4, 0, './logs/exercise1/exercise1_4/', "E2_4_FN_5000_ZC_1000_G0_419")
        plot_E1_4(n_freq_se_4, n_TWL_se_4, n_freq_se_4*n_TWL_se_4, './logs/exercise1/exercise1_4/', "E2_4_FN_7500_ZC_1000_G0_419")
        plot_E1_4(n_freq_se_4, n_TWL_se_4, 2*n_freq_se_4*n_TWL_se_4, './logs/exercise1/exercise1_4/', "E2_4_FN_10000_ZC_1000_G0_419")