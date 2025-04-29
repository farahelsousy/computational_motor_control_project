"""
Exercise 3 – Abstract-oscillator sanity check + drive sweep
—————————————————————————————————————————
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import farms_pylog as pylog

from util.run_closed_loop import run_single, pretty, NumpyEncoder
from util.rw import load_object
from simulation_parameters import SimulationParameters


# --------------------------------------------------------------------- #
#                        small helper utilities                         #
# --------------------------------------------------------------------- #
def match(a, b):
    """truncate a & b (1-D) to the same min length"""
    lim = min(len(a), len(b))
    return a[:lim], b[:lim]


def exercise3():
    pylog.info("Starting Exercise 3 (Q3.3 and Q3.4)")

    # ───────────────────────────────────────────────────────────────── Q3.3
    pylog.info("\n===== Running Q3.3: Default CPG simulation =====")

    log_path = "./logs/exercise3/q3_3_default/"
    video_name = "q3_3_cpg_swim_5s"
    os.makedirs(log_path, exist_ok=True)

    pars = SimulationParameters(
        n_iterations=10001,
        controller="abstract oscillator",
        log_path=log_path,
        simulation_i=0,
        compute_metrics="all",
        print_metrics=False,
        return_network=True,
        headless=False,
        video_record=True,
        video_name=video_name,
        video_fps=50,
    )

    pylog.info("Starting simulation …")
    try:
        controller = run_single(pars)
    except Exception as e:
        pylog.error(f"Simulation failed: {e}", exc_info=True)
        return

    # ---------------- sanity & plots ----------------
    if controller is None:
        pylog.error("Controller object not returned – aborting.")
        return

    # row-count sanity
    expected_len = pars.n_iterations
    if controller.motor_out.shape[0] != expected_len:
        pylog.warning(
            f"motor_out rows = {controller.motor_out.shape[0]}, "
            f"expected {expected_len} → check main loop termination."
        )

    # ══ metrics printout ══
    if hasattr(controller, "metrics"):
        try:
            pretty(controller.metrics)
        except NameError:
            print(json.dumps(controller.metrics, indent=4, cls=NumpyEncoder))

    # ---------- 0) phase heat-map ----------
    plt.figure("Q3.3 – Phase heatmap", figsize=(6, 4))
    phase_mat = controller.state[:, controller.oscillator_phase_all] % (2 * np.pi)
    plt.imshow(
        phase_mat.T,
        aspect="auto",
        cmap="twilight",
        extent=[
            controller.times[0],
            controller.times[-1],
            0,
            controller.oscillator_phase_all.size,
        ],
    )
    plt.colorbar(label="Phase (rad)")
    plt.ylabel("Oscillator index (0-25)")
    plt.xlabel("Time [s]")
    plt.title("Wrapped phases – quick visual sanity")

    # ---------- 1) subset line plots ----------
    n_show = min(6, controller.oscillator_phase_all.size)

    # phases
    plt.figure("Q3.3 – Phases (subset)", figsize=(8, 4))
    for idx in range(n_show):
        t, y = match(controller.times, controller.state[:, controller.oscillator_phase_all[idx]] % (2 * np.pi))
        plt.plot(t, y, label=f"osc {idx}")
    plt.xlabel("Time [s]")
    plt.ylabel("Phase (rad)")
    plt.ylim(0, 2 * np.pi)
    plt.title("First 6 oscillator phases")
    plt.legend(fontsize="small", ncol=2)
    plt.grid(True)

    # amplitudes
    plt.figure("Q3.3 – Amplitudes (subset)", figsize=(8, 4))
    for idx in range(n_show):
        t, y = match(controller.times, controller.state[:, controller.oscillator_amplitude_all[idx]])
        plt.plot(t, y, label=f"{idx}")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.title("First 6 oscillator amplitudes")
    plt.legend(fontsize="small", ncol=2)
    plt.grid(True)

    # motor output L/R first four joints
    plt.figure("Q3.3 – Motor output joints 0-3", figsize=(8, 4))
    for i in range(4):
        t, l = match(controller.times, controller.motor_out[:, controller.motor_l[i]])
        t, r = match(controller.times, controller.motor_out[:, controller.motor_r[i]])
        plt.plot(t, l, "--", label=f"L{i}")
        plt.plot(t, r, "-", label=f"R{i}")
    plt.xlabel("Time [s]")
    plt.ylabel("Activation")
    plt.title("Motor output (first four joints)")
    plt.legend(fontsize="small", ncol=4)
    plt.grid(True)
# ──────────────────────────────────────────────────────────────
#  Travelling-wave overlay plot (like Lecture-7 slide)
# ───────────────────────────────────────────────────────────────
#  Travelling-wave overlay for JOINT ANGLES  (all 13 active joints)
# ───────────────────────────────────────────────────────────────
    if hasattr(controller, "joints_positions"):
        plt.figure("Q3.3 – Joint-angle travelling wave", figsize=(9, 4))

        # joint_positions shape: (time_steps, 15) → take first 13 (active) joints
        joint_ang = controller.joints_positions[:, :13]    # time × 13

        # optional: discard the very first 0.4 s (lock-in transient)
        mask = controller.times >= 0.4
        t_plot = controller.times[mask]
        ang_plot = joint_ang[mask]

        # GLOBAL normalisation so amplitudes stay proportional
        amp_global = np.max(np.abs(ang_plot)) + 1e-12
        wave = ang_plot / amp_global

        for j in range(wave.shape[1]):          # j = 0…12
            plt.plot(t_plot, wave[:, j] + j, lw=2)

        plt.yticks(np.arange(wave.shape[1]), [f"j{j}" for j in range(wave.shape[1])])
        plt.xlabel("Time [s]")
        plt.ylabel("Joint index (offset vertically)")
        plt.title("Travelling wave of joint angles – all 13 active joints")
        plt.grid(ls=":")
        plt.tight_layout()
    else:
        pylog.warning("controller has no 'joints_positions'; joint-angle wave plot skipped.")

    # L-R difference subset
    plt.figure("Q3.3 – Motor diff (L-R)", figsize=(8, 4))
    motor_diff = controller.motor_out[:, controller.motor_l[:n_show]] - controller.motor_out[:, controller.motor_r[:n_show]]
    for i in range(n_show):
        t, diff = match(controller.times, motor_diff[:, i])
        plt.plot(t, diff, label=f"joint {i}")
    plt.xlabel("Time [s]")
    plt.ylabel("L − R")
    plt.title("Motor output difference (joints 0-5)")
    plt.legend(fontsize="small", ncol=3)
    plt.grid(True)

    plt.tight_layout()
    pylog.info("Close figures to continue to Q3.4 …")
    plt.show(block=True)

    # ───────────────────────────────────────────────────────────────── Q3.4
    pylog.info("\n===== Running Q3.4: Drive sweep =====")

    base_log_path = "./logs/exercise3/q3_4_drive_sweep/"
    drive_values = np.arange(1.0, 8.1, 1.0)
    pylog.info(f"Testing drive values: {drive_values}")
    os.makedirs(base_log_path, exist_ok=True)

    results_list = []
    for i, drive in enumerate(drive_values):
        pylog.info(f"— drive = {drive:.1f} —")
        current_path = os.path.join(base_log_path, f"drive_{drive:.1f}")
        pars_ds = SimulationParameters(
            n_iterations=5001,
            controller="abstract oscillator",
            log_path=current_path,
            simulation_i=i,
            compute_metrics="all",
            print_metrics=False,
            return_network=False,
            headless=True,
            video_record=False,
            drive=drive,
        )

        run_single(pars_ds)

        fname = f"drive_{drive:.1f}controller{pars_ds.simulation_i}"
        try:
            obj = load_object(os.path.join(base_log_path, fname))
        except FileNotFoundError:
            pylog.error(f"Results not found for drive={drive:.1f}")
            continue

        if hasattr(obj, "metrics"):
            m = obj.metrics
            m["drive"] = drive
            results_list.append(m)
            # quick numeric sanity
            if "neur_frequency" in m:
                pylog.info(f"  neur_frequency ≈ {m['neur_frequency']:.2f} Hz")
        else:
            pylog.error(f"Loaded object missing metrics for drive={drive:.1f}")

    if not results_list:
        pylog.error("No metrics collected – skipping plot.")
        return

    df = pd.DataFrame(results_list).set_index("drive")
    print("\nCollected metrics:\n", df)

    metrics_to_plot = {
        "neur_frequency": "Neural Frequency [Hz]",
        "neur_amp": "Mean Neural Amplitude",
        "mech_speed_fwd": "Forward Speed",
        "mech_cot": "Cost of Transport",
        "mech_energy": "Energy Consumption",
    }

    plt.figure("Drive-sweep metrics", figsize=(10, 6))
    for idx, (key, label) in enumerate(metrics_to_plot.items(), 1):
        if key not in df.columns:
            pylog.warning(f"Metric '{key}' missing – skip plot.")
            continue
        plt.subplot(3, 2, idx)
        plt.plot(df.index, df[key], "o-")
        plt.xlabel("Drive")
        plt.ylabel(label)
        plt.title(label + " vs Drive")
        plt.grid(True)
    plt.tight_layout()
    plt.show()

    pylog.info("Exercise 3 complete.")


if __name__ == "__main__":
    exercise3()
