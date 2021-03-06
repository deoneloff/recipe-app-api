from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch

from core import models


def sample_user(email='test@eloffstreet.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

        # Arrange
        # Act
        # Assert

    def test_create_user_with_email_successful(self):
        '''Test creating an user with an email is successful'''
        # Arrange
        email = 'janbrandewijn@mydomain.com'
        password = 'Password123'
        # Act
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        # Assert
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_with_email_normalized(self):
        '''Test the user email is normalized'''
        # Arrange
        email = 'janbrandewijn@MYDOMAIN.COM'
        password = 'Password123'
        # Act
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        # Assert
        self.assertEqual(user.email, email.lower())

    def test_create_user_invalid_email(self):
        '''Test creating user with no email raises error'''
        with self.assertRaises(ValueError):
            # anything running inside with-statement must raise a ValueError
            get_user_model().objects.create_user(None, 'pass123')

    def test_create_superuser_successful(self):
        '''Test creating a super user is successful'''
        # Arrange
        email = 'janbrandewijn@mydomain.com'
        password = 'Password123'
        # Act
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
        )
        # Assert
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and mushroom sauce',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
