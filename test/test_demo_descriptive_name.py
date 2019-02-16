import unittest

class TestDemoExecution(unittest.TestCase):

	def test_demo_result_true(self):
		"""
		This is an example of how to write a boolean unit test
		Ex: 4==4 -> True
		"""
		some_function = lambda x : x==4
		self.assertTrue(some_function(4))

	def test_demo_results_equals(self):
		"""
		This is an example of how to write a unit test that checks for equality
		Ex: 4**2 = 16
		"""
		some_function = lambda x : x**2
		self.assertEqual(some_function(4), 16)
