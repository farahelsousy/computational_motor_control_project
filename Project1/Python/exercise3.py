# exercise3.py (Corrected Q3.4 Loading Path)

import numpy as np
import matplotlib.pyplot as plt
import os
import farms_pylog as pylog
import pandas as pd
import json

# Core simulation and analysis utilities
from util.run_closed_loop import run_single, pretty, NumpyEncoder # Import pretty/encoder if they are here
from util.rw import load_object # Confirmed available
from simulation_parameters import SimulationParameters
from plotting_common import plot_time_histories, plot_left_right

# Ensure ffmpeg is installed and added to your system's PATH for video recording (Q3.3).

def exercise3():
    pylog.info("Starting Exercise 3 (Q3.3 and Q3.4)")

    # =========================================================================
    #                       Part 1: Q3.3 Implementation
    # =========================================================================
    pylog.info("\n===== Running Q3.3: Default CPG Simulation and Analysis =====")

    log_path_q3_3 = './logs/exercise3/q3_3_default/'
    video_name_q3_3 = 'q3_3_cpg_swim_5s'
    os.makedirs(log_path_q3_3, exist_ok=True)

    # Set parameters for Q3.3
    pars_q3_3 = SimulationParameters(
        n_iterations=5001,
        controller='abstract oscillator',
        log_path=log_path_q3_3,
        simulation_i=0,
        compute_metrics='all',
        print_metrics=False,
        return_network=True,
        headless=False,
        video_record=True,
        video_name=video_name_q3_3,
        video_fps=50,
    )

    pylog.info("Starting simulation for Q3.3...")
    controller = None
    try:
        controller = run_single(pars_q3_3)

        if controller and hasattr(controller, 'metrics'):
            pylog.info(f"Q3.3 Simulation finished. Controller object returned.")
            pylog.info(f"Q3.3 Video saved as: {log_path_q3_3}/{video_name_q3_3}.mp4 (if ffmpeg is configured)")
            pylog.info("Q3.3 Metrics (from returned controller object):")
            try: pretty(controller.metrics)
            except NameError: print(json.dumps(controller.metrics, indent=4, cls=NumpyEncoder))

            pylog.info("Generating plots for Q3.3...")
            # Plotting code as before...
            # 1. Oscillator Phases Evolution
            plt.figure("Q3.3 Oscillator Phases")
            plot_time_histories(controller.times, controller.state[:, controller.oscillator_phase_all] % (2 * np.pi), cm="jet", offset=0.5, ylabel="Phase [rad]")
            plt.suptitle("Q3.3: Oscillator Phases Evolution"); plt.ylim(0, 2*np.pi); plt.grid(True)
            # 2. Oscillator Amplitudes Evolution
            plt.figure("Q3.3 Oscillator Amplitudes")
            plot_time_histories(controller.times, controller.state[:, controller.oscillator_amplitude_all], cm="jet", offset=0.05, ylabel="Amplitude")
            plt.suptitle("Q3.3: Oscillator Amplitudes Evolution"); plt.grid(True)
            # 3. Motor Output (Left and Right)
            plt.figure("Q3.3 Motor Output (Left/Right)")
            plot_left_right(controller.times, controller.motor_out, controller.motor_l, controller.motor_r, cm="jet", offset=0.1)
            plt.suptitle("Q3.3: Motor Output Evolution (Left/Right)"); plt.grid(True)
            # 4. Motor Output Difference (Left - Right per joint)
            motor_diff = controller.motor_out[:, controller.motor_l] - controller.motor_out[:, controller.motor_r]
            plt.figure("Q3.3 Motor Output Difference (L-R)")
            plot_time_histories(controller.times, motor_diff, cm="jet", offset=0.1, ylabel="Activation Difference (L-R)")
            plt.suptitle("Q3.3: Motor Output Difference Evolution (L-R per joint)"); plt.grid(True)
            # 5. Zebrafish Joint Angles Evolution
            if hasattr(controller, 'joints_positions'):
                if controller.joints_positions.shape[1] >= pars_q3_3.n_joints:
                    active_joint_angles = controller.joints_positions[:, :pars_q3_3.n_joints]
                    time_vector = controller.times[:active_joint_angles.shape[0]]
                    plt.figure("Q3.3 Joint Angles")
                    plot_time_histories(time_vector, active_joint_angles, cm="jet", offset=0.1, ylabel="Joint Angle [rad]")
                    plt.suptitle("Q3.3: Zebrafish Active Joint Angles Evolution"); plt.grid(True)
                else: pylog.warning(f"Q3.3 controller.joints_positions shape unexpected.")
            else: pylog.warning("Q3.3: 'joints_positions' not found in controller.")

            pylog.info("Displaying Q3.3 plots (Close them to continue to Q3.4)...")
            plt.show(block=True)
            pylog.info("Q3.3 Analysis Complete.")
        else: pylog.error("Q3.3: Failed to retrieve valid controller object from run_single.")
    except Exception as e: pylog.error(f"Q3.3 failed! Error: {e}", exc_info=True)

    # =========================================================================
    #                       Part 2: Q3.4 Implementation
    # =========================================================================
    pylog.info("\n===== Running Q3.4: Exploring Effect of Drive Parameter =====")

    base_log_path_q3_4 = './logs/exercise3/q3_4_drive_sweep/'
    # No need to create base path, run_single should handle subdirs if needed,
    # and save_object saves files directly in base path anyway.

    drive_values = np.arange(1.0, 8.1, 1.0)
    pylog.info(f"Testing drive values: {drive_values}")
    results_list_q3_4 = []

    for i, drive in enumerate(drive_values):
        pylog.info(f"\n--- Q3.4: Running simulation for drive = {drive:.1f} ---")
        # Define log path for this run, primarily for save_object's reference,
        # even though it saves the file one level up.
        # Providing the specific subdir helps keep logs potentially organized if other
        # files ARE saved there by run_single (e.g., sensors_data if not returned).
        current_log_path_for_run_single = os.path.join(base_log_path_q3_4, f'drive_{drive:.1f}')

        pars_q3_4 = SimulationParameters(
            n_iterations=5001,
            controller='abstract oscillator',
            log_path=current_log_path_for_run_single, # Pass the intended subdir path
            simulation_i=i,
            compute_metrics='all',
            print_metrics=False,
            return_network=False,
            headless=True,
            video_record=False,
            drive=drive,
        )

        try:
            run_single(pars_q3_4)

            # --- FIX: Construct the path where the file was ACTUALLY saved ---
            actual_filename = f'drive_{drive:.1f}controller{pars_q3_4.simulation_i}'
            # Join with the BASE path, not the subdir path passed to run_single
            controller_filename = os.path.join(base_log_path_q3_4, actual_filename)
            # --- End FIX ---

            pylog.info(f"Loading controller results from: {controller_filename}")
            loaded_controller = load_object(controller_filename)

            if hasattr(loaded_controller, 'metrics'):
                metrics = loaded_controller.metrics
                metrics['drive'] = drive
                results_list_q3_4.append(metrics)
                pylog.info(f"Q3.4 Drive {drive:.1f}: Success. Metrics loaded.")
            else: pylog.error(f"Q3.4 Drive {drive:.1f}: Loaded object missing 'metrics'.")

        except FileNotFoundError: pylog.error(f"Q3.4 Drive {drive:.1f}: File not found at {controller_filename}.")
        except Exception as e: pylog.error(f"Q3.4 Drive {drive:.1f}: Sim/Load failed! Error: {e}", exc_info=True)

# --- Q3.4 Analysis ---
    if not results_list_q3_4:
        pylog.error("Q3.4: No results collected. Skipping analysis plots.")
    else:
        # Convert results to DataFrame
        results_df_q3_4 = pd.DataFrame(results_list_q3_4).set_index('drive')

        print("\n--- Q3.4 Collected Metrics ---")
        pd.set_option('display.max_rows', 500); pd.set_option('display.max_columns', 500); pd.set_option('display.width', 1000)
        print(results_df_q3_4)

        # Plotting key metrics vs. drive
        metrics_to_plot = { # Define metrics to plot against drive
            'neur_frequency': 'Neural Frequency [Hz]', 'neur_amp': 'Mean Neural Amplitude',
            'neur_twl': 'Neural Total Wave Lag',
            'mech_mean_frequency': 'Mean Mech. Frequency [Hz]', 'mech_mean_amplitude': 'Mean Mech. Amplitude [rad]',
            'mech_speed_fwd': 'Forward Speed', 'mech_speed_lat': 'Lateral Speed',
            'mech_cot': 'Cost of Transport', 'mech_energy': 'Energy Consumption',
            'mech_torque': 'Sum of Torques (Effort)', 'mech_twl': 'Mechanical Total Wave Lag',
        }
        num_plots = len(metrics_to_plot)
        plt.figure("Q3.4 Metrics vs Drive", figsize=(12, max(8, 2.5 * ((num_plots + 1) // 2) ))) # Adjust figure size if needed

        # --- Define smaller font sizes ---
        axis_label_fontsize = 8
        title_fontsize = 10
        tick_label_fontsize = 8
        # --- End Define ---

        plot_idx = 1
        for metric_key, ylabel in metrics_to_plot.items():
            if metric_key in results_df_q3_4.columns:
                try:
                    plot_data = results_df_q3_4[metric_key].astype(float) # Ensure numeric type
                    plt.subplot((num_plots + 1) // 2, 2, plot_idx)
                    plt.plot(plot_data.index, plot_data.values, 'o-') # Use .values

                    # --- Apply smaller font sizes ---
                    plt.xlabel("Drive", fontsize=axis_label_fontsize)
                    plt.ylabel(ylabel, fontsize=axis_label_fontsize)
                    plt.title(f"{ylabel} vs. Drive", fontsize=title_fontsize)
                    plt.tick_params(axis='both', which='major', labelsize=tick_label_fontsize) # Adjust tick labels too
                    # --- End Apply ---

                    plt.grid(True)
                    plot_idx += 1
                except Exception as plot_err:
                     pylog.warning(f"Q3.4: Could not plot metric '{metric_key}'. Error: {plot_err}")
            else:
                pylog.warning(f"Q3.4: Metric '{metric_key}' not found in DataFrame columns. Skipping plot.")

        plt.tight_layout(pad=2.0) # Use tight_layout to adjust spacing
        pylog.info("Displaying Q3.4 plots...")
        plt.show()
    pylog.info("\nExercise 3 Complete. Analyze plots and DataFrames for your report.")

if __name__ == '__main__':
    exercise3()
