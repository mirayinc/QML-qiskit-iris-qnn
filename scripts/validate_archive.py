"""Validate the public archive without executing notebook cells or IBM jobs."""
from pathlib import Path
import ast
import csv
import json
import re
from urllib.parse import unquote

import nbformat
import numpy as np
from sklearn.datasets import load_iris


ROOT = Path(__file__).resolve().parents[1]


def check_text(text, label):
    patterns = {
        'GitHub token': r'gh[pousr]_[A-Za-z0-9]{30,}',
        'AWS access key': r'AKIA[0-9A-Z]{16}',
        'private key': r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
        'IBM instance CRN': r'crn:v1:[^\s\"\'<>]+',
        'local user path': r'/Users/[^\s\"\'<>]+',
    }
    for name, pattern in patterns.items():
        if re.search(pattern, text):
            raise ValueError(f'{label}: possible {name}; inspect locally (value withheld).')
    for match in re.finditer(r'(?i)[\"\']?(?:token|api_key|password)[\"\']?\s*[:=]\s*([\"\'])(.*?)\1', text):
        value = match.group(2)
        if not any(word in value.upper() for word in ('BURAYA', 'YOUR_', 'PLACEHOLDER', 'REDACTED_CREDENTIAL', '<API_KEY>')):
            raise ValueError(f'{label}: non-placeholder credential literal (value withheld).')


def check_links(text, base):
    for target in re.findall(r'\]\(([^\s)]+)(?:\s+[^)]*)?\)', text):
        if re.match(r'^(?:https?://|mailto:|#)', target):
            continue
        target = unquote(target.split('#')[0])
        if target and not (base / target).exists():
            raise ValueError(f'Broken local link: {base.relative_to(ROOT)} -> {target}')


def main():
    files = sorted((ROOT / 'notebooks').rglob('*.ipynb'))
    if len(files) != 11:
        raise ValueError(f'Expected 11 notebooks, found {len(files)}')
    code_cells = 0
    historical_errors = 0
    magic_cells = 0
    for path in files:
        notebook = nbformat.read(path, as_version=4)
        nbformat.validate(notebook)
        assert notebook.cells[0].id == 'publication-note'
        for index, cell in enumerate(notebook.cells):
            label = f'{path.relative_to(ROOT)} cell {index}'
            check_text(cell.source, label)
            if cell.cell_type == 'markdown':
                check_links(cell.source, path.parent)
            if cell.cell_type != 'code':
                continue
            code_cells += 1
            if any(line.lstrip().startswith(('!', '%', '?')) for line in cell.source.splitlines()):
                magic_cells += 1
            else:
                ast.parse(cell.source, filename=label)
            for output in cell.get('outputs', []):
                historical_errors += output.get('output_type') == 'error'
                check_text(output.get('text', ''), label + ' output')
                check_text('\n'.join(output.get('traceback', [])), label + ' traceback')
                for mime, value in output.get('data', {}).items():
                    if mime.startswith('text/'):
                        check_text(''.join(value) if isinstance(value, list) else value,
                                   label + ' ' + mime)
    for path in ROOT.rglob('*.md'):
        check_links(path.read_text(), path.parent)
    for path in ROOT.rglob('*.py'):
        ast.parse(path.read_text(), filename=str(path))
    with (ROOT / 'data/iris.csv').open(newline='') as handle:
        rows = list(csv.DictReader(handle))
    iris = load_iris()
    columns = ('sepal_length_cm', 'sepal_width_cm', 'petal_length_cm', 'petal_width_cm')
    np.testing.assert_allclose([[float(row[k]) for k in columns] for row in rows], iris.data)
    np.testing.assert_array_equal([int(row['target']) for row in rows], iris.target)
    assert [row['species'] for row in rows] == [iris.target_names[y] for y in iris.target]
    manifest = json.loads((ROOT / 'docs/SOURCE_MANIFEST.json').read_text())
    assert {item['path'] for item in manifest['notebooks']} == {str(p.relative_to(ROOT)) for p in files}
    assert not list(ROOT.rglob('.env'))
    print(f'PASS: {len(files)} notebook schemas, {code_cells} code cells, '
          f'{magic_cells} installation/magic cells excluded from Python AST parsing.')
    print(f'PASS: local documentation links, Python scripts, 150 Iris rows and credential-pattern checks.')
    print(f'INFO: {historical_errors} historical error outputs preserved; no notebook cells executed.')


if __name__ == '__main__':
    main()
