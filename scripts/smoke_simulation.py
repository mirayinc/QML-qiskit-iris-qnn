"""Exercise reviewed notebook-04 cells on tiny data; never connects to IBM.

This checks selected historical functions, not full notebook reproducibility
and not the historical benchmark scores. Original cell indices exclude the
publication note added as the first cell.
"""
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import ast
import json

import numpy as np
from qiskit.quantum_info import Statevector
from qiskit_machine_learning.algorithms.classifiers import VQC


ROOT = Path(__file__).resolve().parents[1]


def main():
    path = ROOT / 'notebooks/01_simulation/04_qnn_aer_v2.ipynb'
    cells = json.loads(path.read_text())['cells'][1:]
    namespace = {'__name__': '__smoke__'}

    def run_cell(original_index, definitions_only=False):
        source = ''.join(cells[original_index]['source'])
        tree = ast.parse(source)
        if definitions_only:
            tree.body = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.Import, ast.ImportFrom))]
        exec(compile(tree, f'{path.name}:original-cell-{original_index}', 'exec'), namespace)

    np.random.seed(42)
    for index in (2, 4, 6, 8, 13):
        run_cell(index)
    # Cell 18 also runs a demonstration. Load only its import, then build the
    # reusable parameterized circuit from cell 22.
    run_cell(18, definitions_only=True)
    run_cell(22)
    for index in (26, 27, 28, 29):
        run_cell(index, definitions_only=True)

    assert namespace['X_train_s'].shape == (67, 4)
    assert namespace['X_test_s'].shape == (33, 4)
    x = namespace['X_train_s'][0]
    weights = np.array([0.3, 0.7, 1.1, 1.4])
    p1 = namespace['quantum_nn'](x, weights, shots=256)
    assert 0 <= p1 <= 1
    gradient = namespace['gradient'](x, int(namespace['Y_train'][0]), weights)
    assert gradient.shape == (4,) and np.isfinite(gradient).all()
    capture = StringIO()
    with redirect_stdout(capture):
        trained, losses, train_acc, test_acc = namespace['train_simple_qnn'](
            namespace['X_train_s'][:4], namespace['Y_train'][:4],
            namespace['X_test_s'][:4], namespace['Y_test'][:4],
            epochs=1, eta=0.05, theta_init='random')
    assert trained.shape == (4,) and np.isfinite(trained).all()
    assert len(losses) == len(train_acc) == len(test_acc) == 1
    assert np.isfinite(losses).all()
    assert 0 <= train_acc[0] <= 1 and 0 <= test_acc[0] <= 1

    def exact_p1(values):
        qc, _ = namespace['feature_map'](x)
        qc = namespace['variational_circuit'](qc, values)
        return float(Statevector.from_instruction(qc).probabilities([0])[1])

    base = exact_p1(weights)
    sensitivity = []
    for i in range(4):
        changed = weights.copy()
        changed[i] += 0.4
        sensitivity.append(abs(exact_p1(changed) - base))
    assert sensitivity[0] > 1e-6
    np.testing.assert_allclose(sensitivity[1:], 0, atol=1e-12)

    # Verify the installed historical VQC's default interpretation without
    # fitting a new model or sending jobs. Version 0.8.4 uses integer x % 2,
    # i.e. the least significant bit, not bit-count parity over all qubits.
    interpret = VQC(num_qubits=4)._get_interpret(2)
    assert interpret(1) == 1 and interpret(3) == 1
    assert interpret(1) != int(format(1, '04b')[0])

    print('PASS: notebook 04 data split, parameter binding, Aer sampling, finite gradient and one tiny training epoch.')
    print('PASS: ideal q0 readout depends on the final theta[0], not final theta[1:4].')
    print('PASS: VQC 0.8.4 default x % 2 (rightmost bit) differs from notebook 11 leftmost-bit interpretation.')
    print('INFO: no IBM account access or hardware jobs; historical scores were not reproduced.')


if __name__ == '__main__':
    main()
