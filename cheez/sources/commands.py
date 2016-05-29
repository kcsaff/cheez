from cheez.sources.filesystem import from_filesystem
from cheez.sources.flickr import from_flickr


def add_from_parsers(from_subparsers):
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
