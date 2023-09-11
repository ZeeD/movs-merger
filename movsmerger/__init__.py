from collections.abc import Iterator
from difflib import SequenceMatcher
from shutil import move
from sys import argv
from sys import stderr
from typing import Callable
from typing import Final

from movs import read_txt
from movs import write_txt
from movs.estrattoconto import read_estrattoconto
from movs.model import KV
from movs.model import Row
from movs.postepay import read_postepay
from movs.scansioni import read_scansioni


def _merge_rows_helper(acc: list[Row], new: list[Row]) -> Iterator[Row]:
    sequence_matcher = SequenceMatcher(None, acc, new, False)
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
    '.scan': read_scansioni
}


def read(mov_fn: str) -> tuple[KV, list[Row]]:
    for suffix, reader in RULES.items():
        if mov_fn.endswith(suffix):
            break
    else:
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
    if not argv[1:] or '-h' in argv[1:] or '--help' in argv[1:]:
        raise SystemExit(f'''uso: {argv[0]} ACCUMULATOR [MOVIMENTI...]
rules for [MOVIMENTI...]:
''' + '\n'.join(f'*{k: <15}\t->\t{v.__name__}' for k, v in RULES.items()))

    accumulator, *movimentis = argv[1:]
    merge_files(accumulator, *movimentis)

    print(f'overridden {accumulator}', file=stderr)
    print(f'backupd at {accumulator}~', file=stderr)
    for movimenti in movimentis:
        print(f'and merged {movimenti}', file=stderr)
