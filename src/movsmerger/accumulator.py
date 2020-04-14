from __future__ import annotations

import difflib
import typing

import movs


def new_rows(acc: typing.Sequence[movs.model.Row],
             new: typing.Sequence[movs.model.Row]
             ) -> typing.Iterator[movs.model.Row]:
    for tag, _i1, _i2, j1, j2 in difflib.SequenceMatcher(
            None, acc, new, False).get_opcodes():
        if tag in ('insert', 'replace'):
            yield from new[j1:j2]


def accumulate(acc: typing.Sequence[movs.model.Row],
               new: typing.Sequence[movs.model.Row]
               ) -> typing.Sequence[movs.model.Row]:
    print(f'acc: {acc}')
    print(f'new: {new}')

    ret = list(new_rows(acc, new))
    ret.extend(acc)

    print(f'ret: {ret}')

    return ret
