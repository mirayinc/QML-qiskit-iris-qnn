# Quantum Machine Learning on Iris

**Qiskit QNN and VQC experiments · Internship portfolio**  
Miray İnci Başaran · [Türkçe](README.md) · [MIT](LICENSE)

This repository documents my internship experiments in quantum machine learning: building a small QNN training loop, testing it with simulators, exploring IBM Quantum hardware, and trying alternative parameter optimization strategies.

The central question is how to encode classical features into a quantum circuit, optimize its parameters, and move from simulation to hardware. This is an experimental learning archive, with unsuccessful runs and methodological limitations preserved. It does not demonstrate quantum advantage.

## What was done and why?

| Stage | Notebooks | Purpose |
|---|---|---|
| Simulation | [01–04](notebooks/01_simulation) | Understand RX encoding, ring CX connections, RY parameters, sampled probabilities, MSE and finite-difference training; reuse a transpiled parameterized circuit |
| IBM hardware | [05–07](notebooks/02_ibm_hardware) | Explore hardware SPSA training, simulator-trained parameter transfer, shot budgets and SamplerV2 result handling |
| Optimization experiments | [08–09](notebooks/03_finetuning) | Try central finite differences and a genetic algorithm; evaluate hardware on all 33 test samples |
| VQC | [10–11](notebooks/04_vqc) | Compare a manual workflow with ZZFeatureMap, RealAmplitudes and SPSA through the VQC interface; attempt hardware inference |

## Dataset and actual scope

The notebooks load Iris using `sklearn.datasets.load_iris()`. All classifier training uses **100 samples, four features and two classes: Setosa vs Versicolor**, with a 67/33 train/test split. The initial VQC exploratory plots contain all 150 samples; the later training cells filter to two classes. Some hardware evaluations use only eight test samples.

[`data/iris.csv`](data/iris.csv) is an inspection copy, not the notebooks' input file. No private internship business dataset is included.

## Interpreting the saved results

The supplied outputs include 87.9% test accuracy for the second Aer QNN, 75.8% hardware accuracy in notebooks 08–09, and 100% for the SVM baseline in notebook 01. These are historical observations from different settings, not newly reproduced benchmarks or a controlled leaderboard.

Key limitations:

- StatevectorSampler uses a statevector internally but returns finite-shot samples in these experiments.
- The Aer runs do not configure an explicit hardware noise model.
- In the single-layer manual circuit, final rotations on unmeasured qubits do not affect the ideal q0 marginal; four declared parameters do not imply four effective readout parameters.
- Thresholds in 06–07 are optimized on the evaluated test subset, so the adjusted score is exploratory.
- VQC notebooks fit the scaler before the train/test split. The AerEstimator instance is not supplied to VQC; training uses VQC's default sampler path.
- Notebook 11 trains VQC with its default `x % 2` (least-significant-bit) interpretation in QML 0.8.4 but reads the leftmost bit marginal on hardware. These represent different decision rules, so the accuracy gap cannot be attributed to hardware noise alone.
- Some notebooks contain repeated definitions, earlier errors and interrupted hardware jobs.

See the detailed Turkish [experiment guide](docs/CALISMA_REHBERI.md), [saved results](docs/SONUCLAR.md), [method review](docs/YONTEM_VE_SINIRLAR.md) and [validation scope](docs/DOGRULAMA.md).

## Setup

Python 3.12 is used for the publication checks. Start with notebook 04.

```bash
git clone https://github.com/mirayinc/qiskit-iris-qnn.git
cd qiskit-iris-qnn
python -m venv .venv
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python scripts/validate_archive.py
python scripts/smoke_simulation.py
jupyter notebook
```

Notebook 07 requires a **separate** environment using `requirements-qiskit2.txt`. Legacy hardware notebooks are not certified to run unchanged against today's IBM service. No new hardware jobs were submitted during publication. Review [setup and credential handling](docs/KURULUM.md) before executing hardware cells: jobs use your own account and may consume quota or incur account usage.

Publication changes add reading notes, accurate documentation, privacy cleanup and dependency declarations while preserving experimental code. Saved outputs are historical, not the output of the smoke check. The MIT license covers repository code; Iris provenance is documented separately in [`data/README.md`](data/README.md).
