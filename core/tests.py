from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy

from core.forms import ProfileForm, ProcessForm, ProcessFeedbackForm


class ProfileFormTest(TestCase):
    def setUp(self):
        self.profile_data = {
            'first_name': 'John',
            'last_name': 'Snow',
            'email': 'john_snow@winterfell.com',
            'password': 'the_winter_is_coming',
            'password_confirm': 'the_winter_is_coming'
        }

    def test_it_is_possible_to_create_profiles(self):
        """
        Ensure users can create new profiles
        """
        form = ProfileForm(data=self.profile_data)

        self.assertTrue(form.is_valid())

        profile = form.save()
        self.assertEqual(profile.user.first_name, self.profile_data['first_name'])
        self.assertEqual(profile.user.last_name, self.profile_data['last_name'])
        self.assertEqual(profile.user.email, self.profile_data['email'])

    def test_blank_data(self):
        """
        Ensure the form return error message with required fields
        """
        form = ProfileForm(data={})
        default_error_message = {
            'first_name': ['Este campo é obrigatório.'],
            'email': ['Este campo é obrigatório.'],
            'password': ['Este campo é obrigatório.'],
            'password_confirm': ['Este campo é obrigatório.']
        }

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, default_error_message)


class ProcessFormTest(TestCase):
    def setUp(self):
        self.process_data = {
            'title': 'I want the Iron Throne',
            'description': 'I\'m the true King.',
            'feedback_users': [self.fake_publisher.pk],
        }

    @classmethod
    def setUpTestData(cls):
        cls.fake_user = mommy.make(User)
        cls.fake_publisher = mommy.make(User)
        cls.fake_publisher.profile.is_publisher = True
        cls.fake_publisher.profile.save()

    def test_it_is_possible_to_create_process(self):
        """
        Ensure users can create new processes
        """
        form = ProcessForm(data=self.process_data)

        self.assertTrue(form.is_valid())

        process = form.save(commit=False)
        process.created_by = self.fake_user
        process.save()
        form.save_m2m()

        self.assertEqual(process.title, self.process_data['title'])
        self.assertEqual(process.description, self.process_data['description'])
        self.assertIn(self.fake_publisher, process.feedback_users.all())

    def test_blank_data(self):
        """
        Ensure the form return error message with required fields
        """
        form = ProcessForm(data={})
        default_error_message = {
            'title': ['Este campo é obrigatório.'],
            'description': ['Este campo é obrigatório.']
        }

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, default_error_message)


class ProcessFeedbackFormTest(TestCase):
    def setUp(self):
        self.process_feedback_data = {
            'description': 'This is war tho.'
        }

    @classmethod
    def setUpTestData(cls):
        cls.process = mommy.make('core.Process')
        cls.user = mommy.make(User)

    def test_it_is_possible_to_create_feedback(self):
        """
        Ensure users can create feedback process
        """
        form = ProcessFeedbackForm(data=self.process_feedback_data)

        self.assertTrue(form.is_valid())

        process_feedback = form.save(commit=False)
        process_feedback.process = self.process
        process_feedback.created_by = self.user
        process_feedback.save()

        self.assertEqual(
            process_feedback.description,
            self.process_feedback_data['description']
        )

    def test_blank_data(self):
        """
        Ensure the form return error message with required fields
        """
        default_error_message = {'description': ['Este campo é obrigatório.']}
        form = ProcessFeedbackForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, default_error_message)


class ProfileViewTest(TestCase):
    """
    Tests for: ProfileCreateView, ProfileListView, ProfileUpdateView,
               ProfileDeleteView
    """
    username = 'admin'
    password = '1234qwer'

    def setUp(self):
        self.client.login(username=self.username, password=self.password)

    @classmethod
    def setUpTestData(cls):
        cls.user = mommy.make(User, username=cls.username)
        cls.user.set_password(cls.password)
        cls.user.save()

    def test_administrator_can_create_profiles(self):
        """
        Ensure user-administrator can create profiles
        """
        self.user.profile.is_admin = True
        self.user.profile.save()

        response = self.client.get(reverse('profile-create-view'))
        self.assertEqual(response.status_code, 200)

    def test_users_can_not_create_profiles(self):
        """
        Ensure user without permission do not create profiles
        """
        response = self.client.get(reverse('profile-create-view'))
        self.assertEqual(response.status_code, 403)

    def test_administrator_can_list_profiles(self):
        """
        Ensure user-administrator can list profiles
        """
        self.user.profile.is_admin = True
        self.user.profile.save()

        response = self.client.get(reverse('profile-list-view'))
        self.assertEqual(response.status_code, 200)

    def test_users_can_not_list_profiles(self):
        """
        Ensure user without permission do not list profiles
        """
        response = self.client.get(reverse('profile-list-view'))
        self.assertEqual(response.status_code, 403)

    def test_administrator_can_update_profiles(self):
        """
        Ensure user-administrator can update profiles
        """
        self.user.profile.is_admin = True
        self.user.profile.save()

        url = reverse('profile-update-view', kwargs={'pk': self.user.profile.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_users_can_not_update_profiles(self):
        """
        Ensure user without permission do not update profiles
        """
        url = reverse('profile-update-view', kwargs={'pk': self.user.profile.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_administrator_can_delete_profiles(self):
        """
        Ensure user-administrator can delete profiles
        """
        self.user.profile.is_admin = True
        self.user.profile.save()

        url = reverse('profile-delete-view', kwargs={'pk': self.user.profile.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_users_can_not_delete_profiles(self):
        """
        Ensure user without permission do not delete profiles
        """
        url = reverse('profile-delete-view', kwargs={'pk': self.user.profile.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


class ProcessViewTest(TestCase):
    """
    Tests for: ProcessCreateView, ProcessListView, ProcessUpdateView,
               ProcessDeleteView
    """
    username = 'admin'
    password = '1234qwer'

    def setUp(self):
        self.client.login(username=self.username, password=self.password)

    @classmethod
    def setUpTestData(cls):
        cls.process = mommy.make('core.Process')
        cls.user = mommy.make(User, username=cls.username)
        cls.user.set_password(cls.password)
        cls.user.save()

    def test_manager_can_create_processes(self):
        """
        Ensure user-manager can create processes
        """
        self.user.profile.is_manager = True
        self.user.profile.save()

        response = self.client.get(reverse('process-create-view'))
        self.assertEqual(response.status_code, 200)

    def test_users_can_not_create_processes(self):
        """
        Ensure user without permission do not create processes
        """
        response = self.client.get(reverse('process-create-view'))
        self.assertEqual(response.status_code, 403)

    def test_manager_can_list_processes(self):
        """
        Ensure user-manager can list processes
        """
        self.user.profile.is_manager = True
        self.user.profile.save()

        response = self.client.get(reverse('process-list-view'))
        self.assertEqual(response.status_code, 200)

    def test_users_can_not_list_processes(self):
        """
        Ensure user without permission do not list processes
        """
        response = self.client.get(reverse('process-list-view'))
        self.assertEqual(response.status_code, 403)

    def test_manager_can_update_processes(self):
        """
        Ensure user-manager can update processes
        """
        self.user.profile.is_manager = True
        self.user.profile.save()

        url = reverse('process-update-view', kwargs={'pk': self.process.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_users_can_not_update_processes(self):
        """
        Ensure user without permission do not update processes
        """
        url = reverse('process-update-view', kwargs={'pk': self.process.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_manager_can_delete_processes(self):
        """
        Ensure user-manager can delete processes
        """
        self.user.profile.is_manager = True
        self.user.profile.save()

        url = reverse('process-delete-view', kwargs={'pk': self.process.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_users_can_not_delete_processes(self):
        """
        Ensure user without permission do not delete profiles
        """
        url = reverse('process-delete-view', kwargs={'pk': self.process.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


class ProcessFeedbackViewTest(TestCase):
    """
    Tests for: ProcessFeedbackCreateView, ProcessFeedbackListView,
               ProcessFeedbackUpdateView, ProcessFeedbackDeleteView
    """
    username = 'admin'
    password = '1234qwer'

    def setUp(self):
        self.client.login(username=self.username, password=self.password)

    @classmethod
    def setUpTestData(cls):
        cls.process_feedback = mommy.make('core.ProcessFeedback')
        cls.user = mommy.make(User, username=cls.username)
        cls.user.set_password(cls.password)
        cls.user.save()

    def test_publisher_can_create_processfeedbacks(self):
        """
        Ensure user-publisher can create process feedback's with him is
        associated with the process
        """
        self.user.profile.is_publisher = True
        self.user.profile.save()
        self.process_feedback.process.feedback_users.add(self.user)

        url = reverse('processfeedback-create-view', kwargs={'process_pk': self.process_feedback.process.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_users_can_not_create_processfeedbacks(self):
        """
        Ensure user without permission do not create process feedback's
        """
        url = reverse('processfeedback-create-view', kwargs={'process_pk': self.process_feedback.process.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_publisher_can_update_processfeedbacks(self):
        """
        Ensure user-publisher can update process feedback's created by him
        """
        self.user.profile.is_publisher = True
        self.user.profile.save()
        self.process_feedback.created_by = self.user
        self.process_feedback.save()

        url = reverse('processfeedback-update-view', kwargs={'process_pk': self.process_feedback.pk, 'pk': self.process_feedback.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_users_can_not_update_processfeedbacks(self):
        """
        Ensure user without permission do not update process feedback's
        """
        url = reverse('processfeedback-update-view', kwargs={'process_pk': self.process_feedback.pk, 'pk': self.process_feedback.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_publisher_can_delete_processfeedbacks(self):
        """
        Ensure user-publisher can delete process feedback's created by him
        """
        self.user.profile.is_publisher = True
        self.user.profile.save()
        self.process_feedback.created_by = self.user
        self.process_feedback.save()

        url = reverse('processfeedback-delete-view', kwargs={'process_pk': self.process_feedback.pk, 'pk': self.process_feedback.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_users_can_not_delete_processfeedbacks(self):
        """
        Ensure user without permission do not delete process feedback's
        """
        url = reverse('processfeedback-delete-view', kwargs={'process_pk': self.process_feedback.pk, 'pk': self.process_feedback.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
