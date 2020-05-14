# Hybrid flower optimisation program

Computes best way to obtain specific flower colors in Animal Crossing: New Horizons.

## Installation and usage

Python 3.8 and above.

```bash
$ python --version
Python 3.8.0
```

- (Optional) Create a virtual environment

    ```bash
    python -m venv .venv
    ```

    ```bash
    .venv/Scripts/activate
    ```

- Install require libraries

    ```bash
    python -m pip install requirements.txt
    ```

- Use the tool tool

    ```bash
    $ python flower/main.py -t roses -c blue -s
    Namespace(code=None, color='Blue', island=False, seed=True, test=True, type='__ROSES__')
    args=Namespace(code=None, color='Blue', island=False, seed=True, test=True, type='__ROSES__')
    tgt_flowers=[(__ROSES__ RR YY ww ss Blue (2, 2, 2, 0) False)]
    {'A': {'A': {'code': 'rr YY WW ss', 'color': 'Yellow'},
        'B': {'A': {'code': 'RR yy WW Ss', 'color': 'Red'},
                'B': {'A': {'code': 'rr yy Ww ss', 'color': 'White'},
                    'B': None,
                    'code': 'rr yy ww ss',
                    'color': 'Purple',
                    'prob': '0.25',
                    'test': None,
                    'total_prob': '0.25'},
                'code': 'Rr yy Ww ss',
                'color': 'Red',
                'prob': '0.5',
                'test': None,
                'total_prob': '0.125'},
        'code': 'Rr Yy Ww ss',
        'color': 'Red',
        'prob': '0.25',
        'test': None,
        'total_prob': '0.0312'},
    'B': None,
    'code': 'RR YY ww ss',
    'color': 'Blue',
    'prob': '0.0156',
    'test': None,
    'total_prob': '0.000122'}
    ```

- Contribute / report issues

## Backlog next

- [x] FEAT001: Implement color test in graph exploration.

- [x] FEAT002: Compute flower Graph and display it.

- [x] FEAT003: Add tag & attribute for island flowers

- [x] FEAT004: Fix code nomenclatura for windflowers

- [x] FEAT005: Speedup hybrid test runs

- [x] FEAT006: command line interface with argparse

- [x] FEAT007: Web interface

- [ ] FEAT008: No test for last flower right color
