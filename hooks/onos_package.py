from charmhelpers.fetch import (
    apt_install,
    filter_installed_packages,
)

from subprocess import check_call

NEUTRON_CONF_DIR = "/etc/neutron"
NEUTRON_CONF = '%s/neutron.conf' % NEUTRON_CONF_DIR
ML2_CONF = '%s/plugins/ml2/ml2_conf.ini' % NEUTRON_CONF_DIR


# Packages to be installed by charm.
def install_packages(servicename):
    # Install drivers
    if hook_name() == "install":
        apt_install(['git'], fatal=True)
        check_call("sudo tar xvf files/networking-onos.tar", shell=True)
        check_call("cd networking-onos;sudo ./install_driver.sh;cd ..", shell=True)
        check_call("sudo tar xvf files/networking-sfc.tar", shell=True)
        check_call("cd networking-sfc;sudo ./install_driver.sh;cd ..", shell=True)
        # Install neutron
        pkgs = ['neutron-common', 'neutron-plugin-ml2']
        pkgs = filter_installed_packages(pkgs)
        apt_install(pkgs, fatal=True)
        check_call("sudo neutron-db-manage --subproject networking-sfc upgrade head", shell=True)
