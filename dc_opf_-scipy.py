"""
DC Optimal Power Flow (DC-OPF) Optimization Pipeline (Self-Contained SciPy Solver)
Solves the economic dispatch and transmission line constraints directly in Python.
"""

import numpy as np
from scipy.optimize import linprog


def solve_dc_opf():
    print("Initializing and solving DC Optimal Power Flow using SciPy...")

    # --- 1. System Parameters ---
    # Generators: G1, G2, G3
    # Costs ($/MW): [20, 30, 40]
    c = np.array([20.0, 30.0, 40.0, 0.0, 0.0])  # [P_g1, P_g2, P_g3, Theta_2, Theta_3]
    # Note: Theta_1 is fixed to 0 (slack bus), so we optimize 3 generators + 2 voltages = 5 variables

    # Generator bounds (P_min, P_max) and voltage phase angle bounds (unconstrained roughly)
    bounds = [
        (0.0, 150.0),  # G1
        (0.0, 100.0),  # G2
        (0.0, 75.0),  # G3
        (-np.inf, np.inf),  # Theta_2
        (-np.inf, np.inf),  # Theta_3
    ]

    # --- 2. Equality Constraints (Power Balance at Buses 1, 2, and 3) ---
    # Net injection equations derived from DC power flow susceptances:
    # B values: (1-2): 10, (2-3): 12, (1-3): 8
    #
    # Bus 1: P_g1 - Load(40) = 10*(0 - Th2) + 8*(0 - Th3)  ==> P_g1 + 10*Th2 + 8*Th3 = 40
    # Bus 2: P_g2 - Load(90) = 10*(Th2 - 0) + 12*(Th2 - Th3) ==> P_g2 - 22*Th2 + 12*Th3 = 90
    # Bus 3: P_g3 - Load(70) = 8*(Th3 - 0) + 12*(Th3 - Th2)  ==> P_g3 + 12*Th2 - 20*Th3 = 70

    A_eq = np.array([
        [1.0, 0.0, 0.0, 10.0, 8.0],  # Bus 1 power balance
        [0.0, 1.0, 0.0, -22.0, 12.0],  # Bus 2 power balance
        [0.0, 0.0, 1.0, 12.0, -20.0],  # Bus 3 power balance
    ])
    b_eq = np.array([40.0, 90.0, 70.0])

    # --- 3. Inequality Constraints (Transmission Line Thermal Limits) ---
    # Line 1-2 flow: 10 * (0 - Th2) <= 6ency0  => -10*Th2 <= 60  and  10*Th2 <= 60
    # Line 2-3 flow: 12 * (Th2 - Th3) <= 50    => 12*Th2 - 12*Th3 <= 50 and -12*Th2 + 12*Th3 <= 50
    # Line 1-3 flow: 8 * (0 - Th3) <= 80     => -8*Th3 <= 80 and 8*Th3 <= 80

    A_ub = np.array([
        [0, 0, 0, -10.0, 0.0],  # Line 1-2 upper limit
        [0, 0, 0, 10.0, 0.0],  # Line 1-2 lower limit
        [0, 0, 0, 12.0, -12.0],  # Line 2-3 upper limit
        [0, 0, 0, -12.0, 12.0],  # Line 2-3 lower limit
        [0, 0, 0, 0.0, -8.0],  # Line 1-3 upper limit
        [0, 0, 0, 0.0, 8.0],  # Line 1-3 lower limit
    ])
    b_ub = np.array([60.0, 60.0, 50.0, 50.0, 80.0, 80.0])

    # --- 4. Run Optimization ---
    res = linprog(
        c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs"
    )

    if res.success:
        print("\n--- Optimal Dispatch Results ---")
        p_g1, p_g2, p_g3, th2, th3 = res.x[:5]

        print(
            f"Generator G1 Active Power: {p_g1:.2f} MW (Cost: ${p_g1 * 20.0:.2f}/h)"
        )
        print(
            f"Generator G2 Active Power: {p_g2:.2f} MW (Cost: ${p_g2 * 30.0:.2f}/h)"
        )
        print(
            f"Generator G3 Active Power: {p_g3:.2f} MW (Cost: ${p_g3 * 40.0:.2f}/h)"
        )

        total_cost = res.fun
        print(f"\nTotal System Generation Cost: ${total_cost:.2f}/h")
        print(f"Bus Voltage Angles -> Bus 1: 0.00 rad, Bus 2: {th2:.3f} rad, Bus 3: {th3:.3f} rad")
    else:
        print("Optimization failed to find a solution.")


if __name__ == "__main__":
    solve_dc_opf()
