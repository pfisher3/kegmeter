#!/usr/bin/env python

import argparse
import logging
import signal

from kegmeter.common import DB, KegmeterStatus
from kegmeter.web import WebServer

def run_webserver():
    parser = argparse.ArgumentParser()

    parser.add_argument("--init-db", dest="init_db", action="store_true",
                        help="Initialize database and exit.")
    parser.add_argument("--base-dir", dest="base_dir",
                        help="Specify base directory.")
    parser.add_argument("--debug", dest="debug", action="store_true",
                        help="Display debugging information.")
    parser.add_argument("--logfile", dest="logfile",
                        help="Output to log file instead of STDOUT.")

    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.logfile:
        logging.basicConfig(filename=args.logfile)

    if args.base_dir:
        Config.base_dir = args.base_dir

    if args.init_db:
        DB.init_db()
        sys.exit(0)

    status = KegmeterStatus()
    signal.signal(signal.SIGINT, status.interrupt)

    webserver = WebServer(status)
    webserver.listen()


if __name__ == "__main__":
    run_webserver()
