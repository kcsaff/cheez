import sys


# We cache data piped in so it can be re-used by multiple handlers if desired
# However you can ONLY use text or bytes, not both
BYTES_PIPED_IN = None
TEXT_PIPED_IN = None


def read_file(filename, mode='r'):
    global BYTES_PIPED_IN
    global TEXT_PIPED_IN

    if filename == '-':
        if 'b' in mode:
            if TEXT_PIPED_IN is not None:
                raise RuntimeError('Cannot pipe in both text and raw bytes')
            if BYTES_PIPED_IN is None:
                BYTES_PIPED_IN = sys.stdin.buffer.read()
            return BYTES_PIPED_IN
        else:
            if BYTES_PIPED_IN is not None:
                raise RuntimeError('Cannot pipe in both text and raw bytes')
            if TEXT_PIPED_IN is None:
                TEXT_PIPED_IN = sys.stdin.read()
            return TEXT_PIPED_IN
    else:
        with open(filename, mode) as f:
            return f.read()

