from collections.abc import Callable
from collections.abc import Iterator
from difflib import SequenceMatcher
from logging import INFO
from logging import basicConfig
from logging import error
from logging import info
from shutil import move
from sys import argv
from typing import Final

from movs.estrattoconto import read_estrattoconto
from movs.model import KV
from movs.model import Row
from movs.movs import read_txt
from movs.movs import write_txt
from movs.postepay import read_postepay
from movs.scansioni import read_scansioni


def _merge_rows_helper(acc: list[Row], new: list[Row]) -> Iterator[Row]:
    sequence_matcher = SequenceMatcher(None, acc, new, autojunk=False)
    for tag, _i1, _i2, j1, j2 in sequence_matcher.get_opcodes():
        if tag in ('insert', 'replace'):
            yield from new[j1:j2]
    yield from acc


def merge_rows(acc: list[Row], new: list[Row]) -> list[Row]:
    return list(_merge_rows_helper(acc, new))


C = Callable[[str], tuple[KV, list[Row]]]

RULES: Final[dict[str, C]] = {
    '.txt': read_txt,
    'ListaMovimenti.pdf': read_postepay,
    '.pdf': read_estrattoconto,
    '.scan': read_scansioni,
}


class UnknownError(Exception):
    def __init__(self, mov_fn: str) -> None:
        super().__init__(f'unknown {mov_fn=}')


def read(mov_fn: str) -> tuple[KV, list[Row]]:
    for suffix, r in RULES.items():
        reader = r
        if mov_fn.endswith(suffix):
            break
    else:
        raise UnknownError(mov_fn)

    return reader(mov_fn)


def merge_files(acc_fn: str, *mov_fns: str) -> None:
    kv, csv = read(acc_fn)
    for mov_fn in mov_fns:
        kv, mov_csv = read(mov_fn)
        csv = merge_rows(csv, mov_csv)

    move(acc_fn, f'{acc_fn}~')
    write_txt(acc_fn, kv, csv)


def main() -> None:
    basicConfig(level=INFO, format='%(message)s')

    if not argv[1:] or '-h' in argv[1:] or '--help' in argv[1:]:
        error('uso: %s ACCUMULATOR [MOVIMENTI...]', argv[0])
        error('\trules for [MOVIMENTI...]:')
        for k, v in RULES.items():
            error('\t*%-15s\t->\t%s', k, v.__name__)
        raise SystemExit

    accumulator, *movimentis = argv[1:]
    merge_files(accumulator, *movimentis)

    info('overridden %s', accumulator)
    info('backupd at %s~', accumulator)
    for movimenti in movimentis:
        info('and merged %s', movimenti)
