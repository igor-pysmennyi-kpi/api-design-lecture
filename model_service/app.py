import sys
import logging

from receiver import listen_queue


LOGGER = logging.getLogger(__file__)
logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":
    try:
        while True:
            listen_queue(LOGGER)
    except KeyboardInterrupt:
        print('Exiting listener app.')
        sys.exit(0)
