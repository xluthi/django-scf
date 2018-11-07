from django.test import TestCase
from climbing.models import Competitor, Result, Athlete, Club, Category, Competition, Boulder, Gender
from django.db.utils import IntegrityError
from django.db.models.deletion import ProtectedError

class ClubTestCase(TestCase):
    def setUp(self):
        Club.objects.create(name="SCF", city="Brussels", gym="Stone Age Mounier")
        Club.objects.create(name="ECT", city="Louvain-la-Neuve", gym="Blocry")

    def test_get_club(self):
        """Return correct string representation"""
        scf = Club.objects.get(name="SCF")
        self.assertEqual(str(scf), "SCF (Brussels)")

    def test_club_uniqueness(self):
        """Cannot create two club with the same name"""
        with self.assertRaises(IntegrityError):
            scf2 = Club.objects.create(name="SCF", city="Arlon", gym="Escal'pades")

class GenderTestCase(TestCase):
    def test_default_values(self):
        """Check presence of default male and female gender"""
        m = Gender.objects.get(name="male")
        f = Gender.objects.get(name="female")

class CategoryTestCase(TestCase):
    def setUp(self):
        m = Gender.objects.get(name="male")
        cm = Category.objects.create(code="CM", description="Male C", gender = m)

    def test_create_categories(self):
        """Create basic categories"""
        m = Gender.objects.get(name="male")
        with self.assertRaises(IntegrityError):
            cm2 = Category.objects.create(code="CM", description="Male C 2", gender = m)

    def test_get_category(self):
        """String representation"""
        cm = Category.objects.get(code="CM")
        self.assertEqual(str(cm), "Male C")

    def test_cannot_delete_gender_if_category_exists(self):
        """Try to delete male gender while a category uses it"""
        m = Gender.objects.get(name="male")
        with self.assertRaises(ProtectedError):
            m.delete()
