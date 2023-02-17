from __future__ import absolute_import

import argparse
import sys
from cowsay import cowsay, list_cows

OPTIONALS = set("bdgpstwy")

def main(args):
    if args.l:
        if '/' in args.f:
            print(list_cows(args.f), file=sys.stdout)
        else:
            print(list_cows(), file=sys.stdout)
    else:
        lines = []
        for line in sys.stdin:
            lines.append(line.strip())
        preset = None
        for option, value in args._get_kwargs():
            if option in OPTIONALS and value:
                preset = option
                break
        print(
            cowsay(
                message = "\n".join(lines),
                cow=args.f,
                preset = preset,
                eyes = args.e,
                tongue = args.T,
                width = args.W,
                wrap_text = not args.n
            ), 
            file=sys.stdout
        )

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='cowsay app')
    parser.add_argument("-e", type=str, default = 'oo', help="eye_string")
    parser.add_argument("-f", type=str, default = 'default', help="file with cow")
    parser.add_argument("-l", action="store_true", help="")
    parser.add_argument("-n", action="store_true", help="")
    parser.add_argument("-T", type=str, default = '  ', help="tongue_string")
    parser.add_argument("-W", type=int, default=40, help="column")
    for option in OPTIONALS:
        parser.add_argument(f"-{option}", action="store_true")
    args = parser.parse_args()
    main(args)
