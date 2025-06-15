import unittest
from requirements_manager import RequirementManager

class TestRequirementManager(unittest.TestCase):
    def setUp(self):
        self.rm = RequirementManager()
        self.rm.add_requirement('R1', 'The system shall allow users to reset passwords for security reasons.')
        self.rm.add_requirement('R2', 'The application should start within five seconds for better performance.')
        self.rm.add_requirement('R3', 'The interface shall be easy to use for usability.')

    def test_preprocess(self):
        tokens = self.rm.preprocess('User shall be able to LOGIN securely.')
        self.assertIn('login', tokens)
        self.assertIn('securely', tokens)
        self.assertNotIn('user', tokens)  # removed as stop word

    def test_find_related(self):
        related = self.rm.find_related('Improve security around password management.')
        self.assertIn('R1', related)

    def test_integrate(self):
        affected = self.rm.integrate_new_requirement('R4', 'Startup time must be improved to enhance performance.')
        self.assertIn('R2', affected)
        self.assertIn('R4', self.rm.requirements)

if __name__ == '__main__':
    unittest.main()
