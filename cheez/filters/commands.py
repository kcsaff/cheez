from cheez.filters.overlays import thru_overlay_text
from cheez.filters.resize import thru_resize


def add_thru_parsers(thru_subparsers):
    thru_overlay_text_parser = thru_subparsers.add_parser('overlay-text', help='Add overlay text/quote')
    thru_overlay_text_parser.set_defaults(action=thru_overlay_text)

    thru_overlay_text_parser.add_argument(
        '--margin', type=str, default='4%',
        help='Margin around quote block'
    )
    thru_overlay_text_parser.add_argument(
        '--padding', type=str, default='2%',
        help='Padding inside quote block'
    )
    thru_overlay_text_parser.add_argument(
        '--font', '-F', type=str, default=None,
        help='Font'
    )
    thru_overlay_text_parser.add_argument(
        '--font-size', '-S', type=str, default='10%',
        help='Font size'
    )
    thru_overlay_text_parser.add_argument(
        '--text', '-t', type=str, default='',
        help='Text to add to image'
    )
    thru_overlay_text_parser.add_argument(
        '--file', '-f', type=str, default=None,
        help='File to load text from; use `-` for stdin'
    )

    thru_resize_parser = thru_subparsers.add_parser('resize', help='Resize image to given limits')
    thru_resize_parser.set_defaults(action=thru_resize)
