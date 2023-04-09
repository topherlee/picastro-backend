from django.contrib.auth.models import User
from .test_setup import TestSetup
import pdb

class TestViews(TestSetup):

    def test_user_cannot_register_without_data(self):
        res = self.client.post(self.register_url)
        #pdb.set_trace()
        self.assertEqual(res.status_code, 400)


    def test_user_can_register(self):
        res = self.client.post(
            self.register_url,
            self.user_data,
            format='json')
        #pdb.set_trace()
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['email'], self.user_data['email'])
        self.assertEqual(res.data['username'], self.user_data['username'])


    #test not yet working, because email verification not yet implemented
    # def test_user_cannot_login_when_email_unverified(self):
    #     self.client.post(
    #         self.register_url, self.user_data, format='json'
    #     )
    #     res = self.client.post(
    #         self.login_url,
    #         self.user_data,
    #         format='json'
    #     )
    #     self.assertEqual(res.status_code, 401)


    def test_user_can_login_after_email_verification(self):
        res = self.client.post(
            self.register_url,
            self.user_data,
            format='json'
        )
        username = res.data['username']
        user = User.objects.get(username=username)
        user.is_verified = True
        user.save()
        res2 = self.client.post(
            self.login_url,
            self.user_data,
            format='json'
        )
        self.assertEqual(res2.status_code, 200)


    # def test_cannot_get_current_user_without_login(self):
    #     res = self.client.get(
    #         self.current_user_url, self.user_data, format='json'
    #     )
    #     self.assertEqual(res.status_code, 400)

    
    def test_can_get_current_user_after_login(self):
        res = self.client.post(
            self.register_url,
            self.user_data,
            format='json'
        )
        username = res.data['username']
        user = User.objects.get(username=username)
        user.is_verified = True
        user.save()
        res2 = self.client.post(
            self.login_url,
            self.user_data,
            format='json'
        )
        access_token = res2.data['access']
        print(access_token)
        res3 = self.client.get(
            self.current_user_url, format='json'
        )
        pdb.set_trace()
        self.assertEqual(res3.data['username'], self.user_data['username'])


    #def test_cannot_create_post_without_login(self):


    #def test_can_create_post_after_login(self):
