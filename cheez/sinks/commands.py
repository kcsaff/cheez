from cheez.sinks.display import to_display
from cheez.sinks.filesystem import to_filesystem


def add_to_parsers(to_subparsers):
    to_display_parser = to_subparsers.add_parser('display', help='Display image in a window')
    to_display_parser.set_defaults(action=to_display)

    to_file_parser = to_subparsers.add_parser('file', help='Write the photo to a file')
    to_file_parser.set_defaults(action=to_filesystem)

    to_file_parser.add_argument(
        'filename', nargs='?', default='out',
        help='Write to this file'
    )
