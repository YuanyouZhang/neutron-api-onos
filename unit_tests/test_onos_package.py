from test_utils import CharmTestCase
import onos_package

TO_PATCH = [
    'apt_install',
    'filter_installed_packages',
    'os_release',
]


class VPPUtilsTest(CharmTestCase):

    def setUp(self):
        super(VPPUtilsTest, self).setUp(onos_package, TO_PATCH)

    def tearDown(self):
        super(VPPUtilsTest, self).tearDown()

    def test_install_packages(self):
        def _filter(pkg_list):
            return pkg_list
        self.filter_installed_packages.side_effect = _filter
        self.os_release.return_value = 'icehouse'
        onos_package.install_packages('neutron-api')
        self.apt_install.assert_called_with(['neutron-common',
                                             'neutron-plugin-ml2'],
                                            fatal=True)

    def test_install_packages_kilo(self):
        def _filter(pkg_list):
            return pkg_list
        self.filter_installed_packages.side_effect = _filter
        self.os_release.return_value = 'kilo'
        onos_package.install_packages('neutron-api')
        self.apt_install.assert_called_with(['neutron-common',
                                             'neutron-plugin-ml2'],
                                            fatal=True)
