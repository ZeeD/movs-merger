#!/usr/bin/env python

import sys

from movsmerger import Merger


def main() -> None:
    if not sys.argv[1:]:
        raise SystemExit(f'uso: {sys.argv[0]} ACCUMULATOR [MOVIMENTI...]')

    accumulator, *movimentis = sys.argv[1:]
    in_place = True
    suffix = '~'

    Merger(suffix, in_place=in_place).merge(accumulator, *movimentis)

    print(f'overridden {accumulator}', file=sys.stderr)
    print(f'backupd at {accumulator}{suffix}', file=sys.stderr)
    for movimenti in movimentis:
        print(f'and merged {movimenti}', file=sys.stderr)


if __name__ == '__main__':
    main()
