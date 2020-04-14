from __future__ import annotations

import shutil
import sys
import typing

import movs

from .accumulator import accumulate


class Merger:
    def __init__(self, suffix: str='~', *, in_place: bool=True) -> None:
        self.suffix = suffix
        self.in_place = in_place

    def merge(self, acc_fn: str, *mov_fns: str) -> None:

        acc_csv = movs.read_txt(acc_fn)[1]
        mov_kv_csvs = (movs.read_txt(mov_fn) for mov_fn in mov_fns)
        csv = acc_csv
        for kv, mov_csv in mov_kv_csvs:
            csv = accumulate(csv, mov_csv)

        if self.in_place:
            shutil.move(acc_fn, f'{acc_fn}{self.suffix}')
            movs.write_txt(acc_fn, kv, csv)
        else:
            movs.write_kv(sys.stdout, kv)
            movs.write_csv(sys.stdout, csv)
