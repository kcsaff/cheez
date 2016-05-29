import argparse
import random
import sys

from cheez.sources.filesystem import from_filesystem
from cheez.sources.flickr import from_flickr
from cheez.sinks.filesystem import to_filesystem
from cheez.sinks.display import to_display
from cheez.massage import Masseuse

parser = argparse.ArgumentParser()

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
from_subparsers = from_parser.add_subparsers()

from_file_parser = from_subparsers.add_parser('file', help='Read a photo from a filename')
from_file_parser.set_defaults(action=from_filesystem)
from_file_parser.add_argument(
    'filename',
    help='Read image from this file'
)


from_flickr_parser = from_subparsers.add_parser('flickr', help='Get random photo from Flickr')
from_flickr_parser.set_defaults(action=from_flickr)
from_flickr_parser.add_argument(
    '--keys', '-k', type=str, default='keys/flickr.json',
    help='Flickr API keys filename'
)
from_flickr_parser.add_argument(
    '--limit', '-L', type=int, default=100,
    help='Maximum number of images to search for'
)
from_flickr_parser.add_argument(
    '--group-id', type=str, default=None,
    help='Group ID to search through'
)
from_flickr_parser.add_argument(
    '--is-commons', action='store_true',
    help='Whether to restrict search to Flickr commons'
)
from_flickr_parser.add_argument(
    '--license', '-C', action='append',
    help='Flickr license ID(s)'
)
from_flickr_parser.add_argument(
    '--min-taken-date', default=None,
    help='Minimum taken date -- time before now if starts with `-`'
)
from_flickr_parser.add_argument(
    '--max-taken-date', default=None,
    help='Maximum taken date -- time before now if starts with `-`'
)
from_flickr_parser.add_argument(
    '--min-upload-date', default=None,
    help='Minimum upload date -- time before now if starts with `-`'
)
from_flickr_parser.add_argument(
    '--max-upload-date', default=None,
    help='Maximum upload date -- time before now if starts with `-`'
)
from_flickr_parser.add_argument(
    '--safe-search', '-S', choices=('1', '2', '3'), default='1',
    help='Safe search level: higher is less safe'
)
from_flickr_parser.add_argument(
    '--sort', type=str, choices=(
        'date-posted-desc',
        'date-posted-asc',
        'date-taken-desc',
        'date-taken-asc',
        'interestingness-desc',
        'interestingness-asc',
        'relevance',
    ),
    default='interestingness-desc',
    help='Search sort order'
)
from_flickr_parser.add_argument(
    '--tags', '-T', action='append',
    help='Tags to search for'
)
from_flickr_parser.add_argument(
    '--tag-mode', type=str, choices=('any', 'all'), default='all',
    help='Search for any or all tags'
)
from_flickr_parser.add_argument(
    '--text', '-t', type=str, default=None,
    help='Search for text associated with image'
)
from_flickr_parser.add_argument(
    '--user-id', type=str, default=None,
    help='User ID to search through'
)


thru_parser = subparsers.add_parser('thru', help='Process photo with a filter')
thru_subparsers = thru_parser.add_subparsers()


to_parser = subparsers.add_parser('to', help='Write photo to a location')
to_subparsers = to_parser.add_subparsers()

to_display_parser = to_subparsers.add_parser('display', help='Display image in a window')
to_display_parser.set_defaults(action=to_display)

to_file_parser = to_subparsers.add_parser('file', help='Write the photo to a file')
to_file_parser.set_defaults(action=to_filesystem)

to_file_parser.add_argument(
    'filename', nargs='?', default='out',
    help='Write to this file'
)


def main(argv=None):
    argv = (argv or sys.argv)[1:]

    commands = list()
    prev = 1
    for i in range(prev + 1, len(argv)):
        if sys.argv[i] in ('from', 'to'):
            commands.append(sys.argv[prev:i])
            prev = i
    commands.append(sys.argv[prev:])

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
