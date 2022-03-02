from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(username='Misiaty', email='test@email.tt', password='testpass'):
    """Create sample user"""
    return get_user_model().objects.create_user(username, email, password)


class ModelTest(TestCase):

    def test_create_user_with_good_data(self):
        """Test creating new user with expecting data"""
        username = 'Missiaty3'
        email = 'misiaty@mis.mm'
        password = 'TestPass321'
        user = get_user_model().objects.create_user(
            username=username,
            email=email,
            password=password
        )

        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_with_upper_email(self):
        """Test creating user with upper font in email"""
        email = 'misiaty@MIS.MM'
        user = get_user_model().objects.create_user(
            username='Missiaty3',
            email=email,
            password='TestPass321'
        )
        self.assertEqual(user.email, email.lower())

    def test_create_user_with_invalid_username(self):
        """Test creating user with no username raise error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'misiaty@mis.mm', 'test123')

    def test_create_user_with_invalid_email(self):
        """Test creating user with no email raise error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('Missiaty3', None, 'test123')

    def test_create_new_superuser(self):
        """Test creating new supperuser"""
        user = get_user_model().objects.create_superuser(
            'Misiaty'
            'test@gmail.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_event_str(self):
        """Test the event string representation"""
        event = models.Event.objects.create(
            user=sample_user(),
            title='Testtt'
        )
        self.assertEqual(str(event), event.title)

    @patch('uuid.uuid4')
    def test_event_filename_uuid(self, mock_uuid):
        """Test that event image is saved in correct location"""
        uuid = 'testoo-uuid'
        mock_uuid.return_value = uuid
        file_path = models.event_image_file_path(None, 'soneImage.png')

        expected_path = f'events/images/{uuid}.png'
        self.assertEqual(file_path, expected_path)
