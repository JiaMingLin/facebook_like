import unittest
import config

class TestConfig(unittest.TestCase):

	def test_get_value_of_specific_key(self):
		test = config.get_value('system', 'version')
		self.assertEqual(isinstance(test, str), True)

if __name__ == '__main__':
    unittest.main()