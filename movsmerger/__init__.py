from collections.abc import Iterator
from difflib import SequenceMatcher
from shutil import move
from sys import argv
from sys import stderr
from typing import Callable

from movs import read_txt
from movs import write_txt
from movs.estrattoconto import read_estrattoconto
from movs.model import KV
from movs.model import Row
from movs.postepay import read_postepay


def _merge_rows_helper(acc: list[Row], new: list[Row]) -> Iterator[Row]:
    sequence_matcher = SequenceMatcher(None, acc, new, False)
    for tag, _i1, _i2, j1, j2 in sequence_matcher.get_opcodes():
        if tag in ('insert', 'replace'):
            yield from new[j1:j2]
    yield from acc


def merge_rows(acc: list[Row], new: list[Row]) -> list[Row]:
    return list(_merge_rows_helper(acc, new))


def read(mov_fn: str) -> tuple[KV, list[Row]]:
    reader: Callable[[str], tuple[KV, list[Row]]] | None = None
    if mov_fn.endswith('.txt'):
        reader = read_txt
    elif mov_fn == 'ListaMovimenti.pdf':
        reader = read_postepay
    elif mov_fn.endswith('.pdf'):
        reader = read_estrattoconto
    if reader is None:
        raise Exception(f'unknown {mov_fn=}')

    return reader(mov_fn)


def merge_files(acc_fn: str, *mov_fns: str) -> None:
    kv, csv = read(acc_fn)
    for mov_fn in mov_fns:
        kv, mov_csv = read(mov_fn)
        csv = merge_rows(csv, mov_csv)

    move(acc_fn, f'{acc_fn}~')
    write_txt(acc_fn, kv, csv)


def main() -> None:
    if not argv[1:]:
        raise SystemExit(f'uso: {argv[0]} ACCUMULATOR [MOVIMENTI...]')

    if '-h' in argv[1:] or '--help' in argv[1:]:
        raise SystemExit('''rules for [MOVIMENTI...]:
        *.txt              -> bpol reader
        ListaMovimenti.pdf -> postepay
        *.pdf              -> estrattoconto''')

    accumulator, *movimentis = argv[1:]
    merge_files(accumulator, *movimentis)

    print(f'overridden {accumulator}', file=stderr)
    print(f'backupd at {accumulator}~', file=stderr)
    for movimenti in movimentis:
        print(f'and merged {movimenti}', file=stderr)
