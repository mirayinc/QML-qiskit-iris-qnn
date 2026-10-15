"""Exercise notebook-07 local Aer cells in its separate Qiskit 2 environment.

No service is instantiated and no IBM jobs are submitted. Saved benchmark
outputs are not reproduced by this small compatibility check.
"""
from pathlib import Path
import ast
import json

import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main():
    path = ROOT / 'notebooks/02_ibm_hardware/07_qnn_aer_train_ibm_test_tuning.ipynb'
    cells = json.loads(path.read_text())['cells'][1:]
    namespace = {'__name__': '__smoke_qiskit2__'}
    for index in (2, 5, 6, 7, 8):
        tree = ast.parse(''.join(cells[index]['source']))
        # Skip only the circuit drawing expression; preserve circuit creation.
        tree.body = [node for node in tree.body if not (
            isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Attribute)
            and node.value.func.attr == 'draw')]
        exec(compile(tree, f'{path.name}:original-cell-{index}', 'exec'), namespace)
    assert namespace['X_train_s'].shape == (67, 4)
    assert namespace['X_test_s'].shape == (33, 4)
    weights = np.array([0.3, 0.7, 1.1, 1.4])
    p1 = namespace['quantum_nn_sim'](namespace['X_test_s'][0], weights, shots=256)
    assert np.isfinite(p1) and 0 <= p1 <= 1
    accuracy = namespace['accuracy_sim'](
        namespace['X_test_s'][:4], namespace['Y_test'][:4], weights, shots=256)
    assert np.isfinite(accuracy) and 0 <= accuracy <= 1
    print('PASS: notebook 07 imports, split, parameter binding and local Aer inference.')
    print('INFO: no IBM credentials, service connection or hardware jobs.')


if __name__ == '__main__':
    main()
