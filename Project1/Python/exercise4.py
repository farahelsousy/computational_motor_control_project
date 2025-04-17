import numpy as np
import matplotlib.pyplot as plt
import os
import farms_pylog as pylog
import json
import time

# Core simulation and analysis utilities
from util.run_closed_loop import run_single, pretty, NumpyEncoder
from util.rw import load_object
from simulation_parameters import SimulationParameters
from plotting_common import plot_time_histories

# Reference amplitudes (15 values, last 2 are passive)
REF_JOINT_AMP_RAW = np.array([
    0.06580, 0.02810, 0.02781, 0.03047, 0.03623, 0.04127, 0.04864,
    0.05398, 0.06508, 0.08945, 0.10271, 0.11789, 0.14929,
    0.0, 0.0,
])  # unit: radian

N_ACTIVE_JOINTS = 13
REF_JOINT_AMP = REF_JOINT_AMP_RAW[:N_ACTIVE_JOINTS]

MECH_AMP_KEY = "mech_joint_amplitudes"

# Helper: run one trial
def simulate(trial, gains, base_log):
    pylog.info(f"Sim Trial {trial}...")
    trial_dir = os.path.join(base_log, f"trial_{trial}") + os.sep
    os.makedirs(trial_dir, exist_ok=True)
    gains_list = gains.tolist() if isinstance(gains, np.ndarray) else gains
    assert len(gains_list)==N_ACTIVE_JOINTS
    pars = SimulationParameters(
        log_path=trial_dir,
        simulation_i=trial,
        headless=True,
        compute_metrics="all",
        print_metrics=False,
        return_network=False,
        controller="abstract oscillator",
        n_iterations=5001,
        drive=4,
        cpg_amplitude_gain=gains_list,
    )
    run_single(pars)
    path = os.path.join(trial_dir, f"controller{trial}")
    return path

# Main optimization
def exercise4():
    pylog.info("Starting Ex4 optimization...")
    base = os.path.join('.', 'logs', 'exercise4', 'opt_run')+os.sep
    os.makedirs(base, exist_ok=True)

    lr = 1e-4
    tol = 0.01
    max_it = 50

    gains = np.ones(N_ACTIVE_JOINTS)*0.125
    best_gains = gains.copy()
    err = np.inf
    errs = []
    gain_hist = []

    for it in range(1, max_it+1):
        pylog.info(f"-- Iter {it}")
        gain_hist.append(gains.copy())

        ctl_path = simulate(it, gains, base)
        try:
            ctrl = load_object(ctl_path)
            amps = np.array(ctrl.metrics[MECH_AMP_KEY])[:N_ACTIVE_JOINTS]
        except Exception as e:
            pylog.error(f"Load failed: {e}")
            break
        amps = np.maximum(amps, 1e-6)

        rel = np.abs((amps-REF_JOINT_AMP)/(REF_JOINT_AMP+1e-9))
        per_joint = np.round(rel,3)
        pylog.info(f"Per-joint rel err: {per_joint}")
        err = rel.mean()
        errs.append(err)
        pylog.info(f"Mean err: {err:.4f}")

        if err<tol:
            pylog.info("Converged!")
            best_gains = gains.copy()
            break
        if err<min(errs[:-1] or [np.inf]):
            best_gains = gains.copy()

        # standard update
        sf = REF_JOINT_AMP/amps
        gains = gains*(1 + lr*(-1+sf))
        # alternative stable (uncomment):
        # gains = gains * np.exp(lr*np.log(REF_JOINT_AMP/amps))
        gains = np.clip(gains, 0.001, 10.0)

    # Plot errors
    plt.figure(); plt.plot(range(1,len(errs)+1), errs, 'o-'); plt.yscale('log')
    plt.xlabel('Iter'); plt.ylabel('Mean rel error'); plt.title('Convergence')
    # Plot gains evolution
    plt.figure();
    for j in range(N_ACTIVE_JOINTS):
        arr = [g[j] for g in gain_hist]
        plt.plot(range(1,len(arr)+1), arr, '-o', label=f'j{j}')
    plt.xlabel('Iter'); plt.ylabel('Gain'); plt.legend(bbox_to_anchor=(1,1))
    plt.tight_layout()
    plt.show(block=False)

    np.save(os.path.join(base,'opt_gains.npy'), best_gains)
    pylog.info(f"Best gains: {np.round(best_gains,4)} saved")

    # final run
    final_dir = base+'final_run'+os.sep
    os.makedirs(final_dir, exist_ok=True)
    pars = SimulationParameters(
        n_iterations=5001, controller='abstract oscillator',
        log_path=final_dir, simulation_i='final',
        compute_metrics='all', print_metrics=True,
        return_network=True, headless=False,
        video_record=True, video_name='opt_swim',
        drive=4, cpg_amplitude_gain=best_gains.tolist(),
    )
    ctrl = run_single(pars)
    pylog.info("Final swim done. Inspect metrics and video.")
    pretty(ctrl.metrics)

if __name__=='__main__':
    exercise4()
