from .test_setup import TestSetup
import pdb

class TestViews(TestSetup):

    def test_user_cannot_register_without_data(self):
        res = self.client.post(self.register_url)
        #pdb.set_trace()
        self.assertEqual(res.status_code, 400)

    def test_user_can_register(self):
        res = self.client.post(self.register_url, self.user_data, format='json')
        pdb.set_trace()
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['email'], self.user_data['email'])
        self.assertEqual(res.data['username'], self.user_data['username'])