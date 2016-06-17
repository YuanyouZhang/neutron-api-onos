from test_utils import CharmTestCase
from mock import patch
import onos_relation
import charmhelpers
import charmhelpers.core.services.helpers
import json
TO_PATCH = [
    'config',
]


def fake_context(settings):
    def outer():
        def inner():
            return settings
        return inner
    return outer


FULL_ONOSCTRL = {
    'data': {
        'private-address': '10.0.0.27',
        'port': '8080',
        'username': 'onosuser',
        'password': 'hardpassword',
    },
    'rids': ['onos-controller:2'],
    'runits': ['onos-controller/0'],
}

MISSING_DATA_ONOSCTRL = {
    'data': {
        'private-address': '10.0.0.27',
    },
    'rids': ['onos-controller:2'],
    'runits': ['onos-controller/0'],
}


class NeutronApiSDNRelationTest(CharmTestCase):

    def setUp(self):
        super(NeutronApiSDNRelationTest, self).setUp(onos_relation, TO_PATCH)
        self.config.side_effect = self.test_config.get

    def tearDown(self):
        super(NeutronApiSDNRelationTest, self).tearDown()

    @patch.object(charmhelpers.core.hookenv, 'relation_get')
    @patch.object(charmhelpers.core.hookenv, 'related_units')
    @patch.object(charmhelpers.core.hookenv, 'relation_ids')
    def test_provide_data(self, _hrids, _hrunits, _hrget):
        sdn_relation = onos_relation.BuildSDNRelation()
        expect = {
            'core-plugin': 'neutron.plugins.ml2.plugin.Ml2Plugin',
            'neutron-plugin': 'onos',
            'neutron-plugin-config': '/etc/neutron/plugins/ml2/ml2_conf.ini',
            'service-plugins': 'onos_router',
        }
        provide_data = sdn_relation.provide_data()
        for key in expect.keys():
            self.assertEqual(provide_data[key], expect[key])
        # Check valid json is being passed
        principle_config = json.loads(
            provide_data['subordinate_configuration']
        )
        self.assertEqual(principle_config['neutron-api'].keys()[0],
                         '/etc/neutron/neutron.conf')


class ONOSControllerRelationTest(CharmTestCase):

    def setUp(self):
        super(ONOSControllerRelationTest, self).setUp(onos_relation, TO_PATCH)
        self.config.side_effect = self.test_config.get

    def tearDown(self):
        super(ONOSControllerRelationTest, self).tearDown()

    @patch.object(charmhelpers.core.hookenv, 'relation_get')
    @patch.object(charmhelpers.core.hookenv, 'related_units')
    @patch.object(charmhelpers.core.hookenv, 'relation_ids')
    def get_onosrel(self, _hrids, _hrunits, _hrget, relinfo=None):
        _hrids.return_value = relinfo['rids']
        _hrunits.return_value = relinfo['runits']
        self.test_relation.set(relinfo['data'])
        _hrget.side_effect = self.test_relation.get
        onos_rel = onos_relation.ONOSControllerRelation()
        onos_rel.get_data()
        return onos_rel

    def test_get_data(self):
        onos_rel = self.get_onosrel(relinfo=FULL_ONOSCTRL)
        expect = {
            'onos_ip': '10.0.0.27',
            'onos_port': '8080',
            'onos_username': 'onosuser',
            'onos_password': 'hardpassword',
        }
        for key in expect.keys():
            self.assertEqual(onos_rel[key], expect[key])

    def test_is_ready(self):
        onos_rel = self.get_onosrel(relinfo=FULL_ONOSCTRL)
        self.assertEqual(onos_rel.is_ready(), True)

    def test_is_ready_incomplete(self):
        onos_rel = self.get_onosrel(relinfo=MISSING_DATA_ONOSCTRL)
        self.assertEqual(onos_rel.is_ready(), False)


class ConfigTranslationTest(CharmTestCase):

    def setUp(self):
        super(ConfigTranslationTest, self).setUp(onos_relation, TO_PATCH)
        self.config.side_effect = self.test_config.get

    def tearDown(self):
        super(ConfigTranslationTest, self).tearDown()

    def test_config_default(self):
        ctxt = onos_relation.ConfigTranslation()
        self.assertEqual(ctxt, {'overlay_network_type': 'vxlan',
                                'security_groups': False})

        self.test_config.set('security-groups', True)
        ctxt = onos_relation.ConfigTranslation()
        self.assertEqual(ctxt, {'overlay_network_type': 'vxlan',
                                'security_groups': True})
