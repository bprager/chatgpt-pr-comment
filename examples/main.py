# /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
import logging
import sys

# setup logger
logger = logging.getLogger(__name__)
stoh = logging.StreamHandler(sys.stderr)
fmth = logging.Formatter(
    "%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"
)
stoh.setFormatter(fmth)
logger.addHandler(stoh)
logger.setLevel(logging.DEBUG)


def main():
    logger.info("Hello World!")


if __name__ == "__main__":
    main()
