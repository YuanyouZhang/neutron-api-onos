from charmhelpers.fetch import (
    apt_install,
    filter_installed_packages,
)
from charmhelpers.core.hookenv import hook_name
from charmhelpers.core.hookenv import log
from subprocess import check_call
import subprocess
import os

NEUTRON_CONF_DIR = "/etc/neutron"
NEUTRON_CONF = '%s/neutron.conf' % NEUTRON_CONF_DIR
ML2_CONF = '%s/plugins/ml2/ml2_conf.ini' % NEUTRON_CONF_DIR


# Packages to be installed by charm.
def install_packages(servicename):
    if hook_name() == "install":
        # Install drivers
        apt_install(['git'], fatal=True)
        check_call("sudo tar xvf files/networking-onos.tar", shell=True)
        check_call("cd networking-onos;sudo ./install_driver.sh;cd ..", shell=True)
        check_call("sudo tar xvf files/networking-sfc.tar", shell=True)
        check_call("cd networking-sfc;sudo ./install_driver.sh;cd ..", shell=True)
        # Install neutron
        pkgs = ['neutron-common', 'neutron-plugin-ml2']
        pkgs = filter_installed_packages(pkgs)
        apt_install(pkgs, fatal=True)
        # Update neutron table
        update_sfc()

def local_unit():
    """Local unit ID"""
    return os.environ['JUJU_UNIT_NAME']

def update_sfc():
    try:
        check_call("sudo neutron-db-manage --subproject networking-sfc upgrade head", shell=True)
    except subprocess.CalledProcessError as e:
        log('Faild to update sfc')
