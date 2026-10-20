# DC Optimal Power Flow & Economic Dispatch (SciPy / HiGHS)

A self-contained Python implementation of **DC Optimal Power Flow (DC-OPF)** and transmission-constrained economic dispatch solved directly using the high-performance **HiGHS** linear programming solver in `scipy.optimize`.

This repository demonstrates physics-constrained power system optimization, enforcing nodal power balance and transmission thermal limits without requiring external software dependencies or binary solvers.

## Overview
Modern smart grid architectures require fast, reliable optimization algorithms to schedule generation while guaranteeing physical security constraints. This repository formulates the linear DC-OPF problem for a 3-bus transmission benchmark, explicitly modeling line susceptances, voltage phase angles, generator operational limits, and line thermal capacities.

## Key Features
* **Zero External Dependencies:** Built strictly using `numpy` and `scipy`, ensuring 100% cross-platform reproducibility without external MILP/LP binaries.
* **Full Network Physics:** Direct matrix formulation of nodal power balance equations ($P_{gi} - P_{di} = \sum_{j} B_{ij}(\theta_i - \theta_j)$) and line flow limits.
* **Modern HiGHS Solver:** Leverages SciPy's state-of-the-art dual simplex / interior point solver (`method='highs'`).

## Mathematical Formulation

The economic dispatch optimization problem minimizes total generation cost subject to network physical constraints:

$$\min_{P_g, \theta} \sum_{g \in \mathcal{G}} C_g P_g$$

Subject to:

1. **Nodal Active Power Balance (Bus Injection Equations):**
   $$P_{gi} - P_{di} = \sum_{j \in \text{adj}(i)} B_{ij}(\theta_i - \theta_j), \quad \forall i \in \mathcal{B}$$
2. **Transmission Thermal Limits:**
   $$-F_{ij}^{\max} \le B_{ij}(\theta_i - \theta_j) \le F_{ij}^{\max}, \quad \forall (i,j) \in \mathcal{L}$$
3. **Generator Capacity Limits:**
   $$P_{g}^{\min} \le P_{g} \le P_{g}^{\max}, \quad \forall g \in \mathcal{G}$$
4. **Slack Bus Reference Angle:**
   $$\theta_1 = 0$$

## Getting Started

### Prerequisites
* Python 3.8+
* NumPy, SciPy

### Installation
```bash
pip install numpy scipy
