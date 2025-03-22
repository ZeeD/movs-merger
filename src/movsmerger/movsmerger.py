from difflib import SequenceMatcher
from logging import INFO
from logging import basicConfig
from logging import getLogger
from pathlib import Path
from shutil import move
from sys import argv
from typing import TYPE_CHECKING

from movslib.movs import write_txt
from movslib.reader import read

if TYPE_CHECKING:
    from collections.abc import Iterator

    from movslib.model import KV
    from movslib.model import Row

logger = getLogger(__name__)


def _merge_rows_helper(acc: 'list[Row]', new: 'list[Row]') -> 'Iterator[Row]':
    sequence_matcher = SequenceMatcher(None, acc, new, autojunk=False)
    for tag, i1, i2, j1, j2 in sequence_matcher.get_opcodes():
        if tag == 'insert':
            yield from new[j1:j2]
        elif tag in {'equal', 'delete'}:
            yield from acc[i1:i2]
        elif tag == 'replace':  # take from both
            i = i1
            j = j1
            while i < i2 and j < j2:
                a = acc[i]
                n = new[j]
                if a.date > n.date:
                    yield a
                    i += 1
                else:
                    yield n
                    j += 1
            yield from new[j:j2]
            yield from acc[i:i2]


def merge_rows(acc: 'list[Row]', new: 'list[Row]') -> 'list[Row]':
    return list(_merge_rows_helper(acc, new))


def merge_files(acc_fn: str, *mov_fns: str) -> 'tuple[KV, list[Row]]':
    kv, csv = read(acc_fn)
    for mov_fn in mov_fns:
        kv, mov_csv = read(mov_fn)
        csv = merge_rows(csv, mov_csv)
    return kv, csv


def _main_txt(accumulator: str, movimentis: list[str]) -> None:
    kv, csv = merge_files(accumulator, *movimentis)

    move(accumulator, f'{accumulator}~')
    logger.info('backupd at %s~', accumulator)

    write_txt(accumulator, kv, csv)
    logger.info('overridden %s', accumulator)

    for movimenti in movimentis:
        logger.info('and merged %s', movimenti)


def _main_binary(binary_accumulator: str, movimentis: list[str]) -> None:
    logger.info('kept %s', binary_accumulator)
    accumulator_orig = str(Path(binary_accumulator).with_suffix('.txt~'))
    kv_orig, csv_orig = merge_files(binary_accumulator)
    write_txt(accumulator_orig, kv_orig, csv_orig)
    logger.info('backupd at %s', accumulator_orig)

    kv, csv = merge_files(binary_accumulator, *movimentis)
    accumulator = str(Path(binary_accumulator).with_suffix('.txt'))
    write_txt(accumulator, kv, csv)
    logger.info('merged at %s', accumulator)

    for movimenti in movimentis:
        logger.info('and merged %s', movimenti)


def main() -> None:
    basicConfig(level=INFO, format='%(message)s')

    if not argv[1:] or '-h' in argv[1:] or '--help' in argv[1:]:
        logger.error('uso: %s ACCUMULATOR [MOVIMENTI...]', argv[0])
        raise SystemExit

    accumulator, *movimentis = argv[1:]

    if accumulator.endswith('txt'):
        _main_txt(accumulator, movimentis)
    else:
        _main_binary(accumulator, movimentis)
