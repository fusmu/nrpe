#!/bin/python
import sys
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument(
        "-c", "--critical",
        dest="CRITICAL",
        help="set critical limit",
        type=int,
        action="store",
        required=True)
parser.add_argument(
        "-w", "--warning",
        dest="WARNING",
        help="set warning limit",
        type=int,
        action="store",
        required="true"
)
args = parser.parse_args()


def usage(CRITICAL, WARNING):

    for line in open("/proc/meminfo"):
        if "Active:" in line:
            active_memory = int(line.split()[1]) / 1024
    for line in open("/proc/meminfo"):
        if "MemTotal:" in line:
            total_memory = int(line.split()[1]) / 1024
    usage = (active_memory * 100) / total_memory

    if usage > WARNING and usage < CRITICAL:
        print "WARNING: Memory usage is %s%% " % usage
        sys.exit(1)
    elif usage > CRITICAL:
        print "CRITICAL: Memory usage is %s%% " % usage
        sys.exit(2)
    elif usage < WARNING and usage < CRITICAL:
        print "OK: Memory usage is %s%% " % usage
        sys.exit(0)
    return usage


usage(args.CRITICAL, args.WARNING)
