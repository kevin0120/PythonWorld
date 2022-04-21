from sdk.structs import CURVE_TEMPLATE_CLUSTER, PTR_CURVE_TEMPLATE_CLUSTER
from sdk.constants import CURVE_MODES
import unittest
from typing import Dict, Optional
import json
from sdk.sdk import ca_attach, ca_detach, get_platform_version, doCALoadCurveTemplate, doCACurveEncode


class Test_CurveSDK(unittest.TestCase):
    mock_params = {}

    def load_params(self, bolt_number: str) -> Optional[Dict]:
        mock_params = self.mock_params
        if bolt_number not in mock_params.keys():
            return None
        return mock_params.get(bolt_number)

    def setUp(self):
        ca_attach()
        with open('mock_curve_params.json') as f:
            self.mock_params = json.load(f)

    def tearDown(self):
        ca_detach()

    def testGetPlatformVersion(self):
        version = get_platform_version()
        self.assertIsInstance(version, str)

    def testLoadCurveTmpl(self):
        mode = CURVE_MODES.get('CURVE_OK')
        bolt= "CA-008L3-1"
        craft_type = 1
        curve_param = self.load_params(bolt)
        if not curve_param:
            self.fail("曲线参数未找到{}".format(bolt))
        template_cluster: CURVE_TEMPLATE_CLUSTER = doCACurveEncode(bolt, craft_type, mode, curve_param, {}, 100.0, 120.1)
        doCALoadCurveTemplate(bolt, craft_type, mode, curve_param, template_cluster)
