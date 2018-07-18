#!/bin/python
import subprocess
import sys
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument(
        "-t", "--type",
        dest="CHECK_TYPE",
        help="set critical limit",
        type=str,
        action="store",
        required=True
)
args = parser.parse_args()


# Flavor checker


def check_flavor_exist():
    P1 = subprocess.Popen(['nova', 'flavor-list', '--all'],
                          stdout=subprocess.PIPE)
    P2 = subprocess.Popen(['grep', 'nagios-test'], stdin=P1.stdout,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    P1.stdout.close()
    if P2.wait() != 0:
        return False
    else:
        return True


def add_flavor():
    p = subprocess.Popen(['openstack',
                         'flavor',
                          'create',
                          '--public',
                          'nagios-test',
                          '--id',
                          'auto',
                          '--ram',
                          '256',
                          '--disk',
                          '0',
                          '--vcpus',
                          '1'],
                         stdout=subprocess.PIPE)
    (output, err) = p.communicate()
    if p.wait() != 0:
        print "Creating flavor failed"
        sys.exit(1)


def delete_flavor():
    p = subprocess.Popen(['nova', 'flavor-delete', 'nagios-test'],
                         stdout=subprocess.PIPE)
    (output, err) = p.communicate()
    if p.wait() != 0:
        print "Deleting flavor failed"
        sys.exit(1)


# Glance checker


def check_image_exist():
    P1 = subprocess.Popen(['openstack', 'image', 'list'],
                          stdout=subprocess.PIPE)
    P2 = subprocess.Popen(['grep', 'nagios-test'],
                          stdin=P1.stdout,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    P1.stdout.close()
    if P2.wait() != 0:
        return False
    else:
        return True


def add_image():
    p = subprocess.Popen(['openstack',
                         'image',
                          'create', 'nagios-test',
                          '--file', '/var/run/nrpe/cirros-nagios-test.img',
                          '--disk-format', 'raw',
                          '--container-format', 'bare',
                          '--public'],
                         stdout=subprocess.PIPE)
    (output, err) = p.communicate()
    if p.wait() != 0:
        print "Creating image failed"
        sys.exit(1)


def delete_image():
    p = subprocess.Popen(['openstack', 'image', 'delete', 'nagios-test'],
                         stdout=subprocess.PIPE)
    (output, err) = p.communicate()
    if p.wait() != 0:
        print "Deleting image failed"
        sys.exit(1)


# Cinder checker


def check_volume_exists():
    P1 = subprocess.Popen(['openstack', 'volume', 'list', '--all'],
                          stdout=subprocess.PIPE)
    P2 = subprocess.Popen(['grep', 'nagios-test'],
                          stdin=P1.stdout,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    P1.stdout.close()
    if P2.wait() != 0:
        return False
    else:
        return True


def add_volume():
    p = subprocess.Popen(['openstack',
                         'volume',
                          'create',
                          'nagios-test',
                          '--size',
                          '5'],
                         stdout=subprocess.PIPE)
    (output, err) = p.communicate()
    if p.wait() != 0:
        print "Creating volume failed"
        sys.exit(1)


def delete_volume():
    p = subprocess.Popen(['openstack',
                         'volume',
                          'delete',
                          'nagios-test'],
                         stdout=subprocess.PIPE)
    (output, err) = p.communicate()
    if p.wait() != 0:
        print "Deleting volume failed"
        sys.exit(1)


# Main


if args.CHECK_TYPE == "flavor":
    if check_flavor_exist() is True:
        delete_flavor()
        add_flavor()
        print "Flavor check: HEALTHY"
        sys.exit(0)
    else:
        add_flavor()
        print "Flavor check: HEALTHY"
        sys.exit(0)

elif args.CHECK_TYPE == "glance":
    if check_image_exist() is True:
        delete_image()
        add_image()
        print "Glance check: HEALTHY"
        sys.exit(0)
    else:
        add_image()
        print "Glance check: HEALTHY"
        sys.exit(0)

elif args.CHECK_TYPE == "cinder":
    if check_volume_exists() is True:
        delete_volume()
        add_volume()
        print "Cinder check: HEALTHY"
    else:
        add_volume()
        print "Cinder check: HEALTHY"
