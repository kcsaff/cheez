import argparse
import random
import sys

from cheez.sources.commands import add_from_parsers
from cheez.filters.commands import add_thru_parsers
from cheez.sinks.commands import add_to_parsers

from cheez.massage import Masseuse


import pkg_resources
try:
    VERSION = pkg_resources.require("cheez")[0].version
except:
    VERSION = 'DEV'


parser = argparse.ArgumentParser(
    description=(
        "Pipeline for cheez-y image macros and filters, for random downloaded images" +
        "\n{}".format(VERSION)
    ),
    formatter_class=argparse.RawDescriptionHelpFormatter
)

parser.add_argument(
    '--version', action='store_true',
    help='Print version ({}) and exit'.format(VERSION)
)
parser.add_argument(
    '--width', '-W', type=int, default=1200,
    help='Width of generated image'
)
parser.add_argument(
    '--height', '-H', type=int, default=630,
    help='Height of generated image'
)

subparsers = parser.add_subparsers(help='Image sources')

from_parser = subparsers.add_parser('from', help='Get photo from a location')
add_from_parsers(from_parser.add_subparsers())

thru_parser = subparsers.add_parser('thru', help='Process photo with a filter')
add_thru_parsers(thru_parser.add_subparsers())

to_parser = subparsers.add_parser('to', help='Write photo to a location')
add_to_parsers(to_parser.add_subparsers())


def main(argv=None):
    argv = (argv or sys.argv)[1:]

    commands = list()
    prev = None
    for i in range(1, len(argv)):
        if sys.argv[i] in ('from', 'thru', 'to'):
            if prev is not None:
                commands.append(sys.argv[prev:i])
            prev = i
    if prev is not None:
        commands.append(sys.argv[prev:])

    if not commands:
        args = parser.parse_args()
        if args.version:
            print(VERSION)
            return
        else:
            raise RuntimeError('At least one source (`from`) is required!')

    sources = list()
    filters = list()
    sinks = list()
    for command in commands:
        {'from': sources, 'thru': filters, 'to':sinks}[command[0]].append(command)

    massage = Masseuse().massage

    # Choose one source at random
    if not sources:
        raise RuntimeError('At least one source (`from`) is required!')
    source = random.choice(sources)
    source_args = parser.parse_args(source)
    image = source_args.action(source_args)
    image = massage(image)

    # Apply any/all filters in order
    for filter in filters:
        filter_args = parser.parse_args(filter)
        image = filter_args.action(image, filter_args)
        image = massage(image)

    # Run all outputs
    if not sinks:
        sinks.append('to file'.split())
    for sink in sinks:
        sink_args = parser.parse_args(sink)
        sink_result = sink_args.action(image, source_args)
        if sink_result:
            print(sink_result)


if __name__ == '__main__':
    main()
