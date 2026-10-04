# Copyright (c) 2024, Nortex and Contributors
# See license.txt

from frappe.tests import IntegrationTestCase, UnitTestCase

from ex_maintenance.ex_maintenance.doctype.response_time.response_time import (
	calculate_average_response_time,
	format_duration,
)

# On IntegrationTestCase, the doctype test records and all
# link-field test record depdendencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]


class UnitTestResponseTime(UnitTestCase):
	"""
	Unit tests for ResponseTime.
	Use this class for testing individual functions and methods.
	"""

	def test_format_duration(self):
		self.assertEqual(format_duration(30), "30.00 seconds")
		self.assertEqual(format_duration(90), "1.50 minutes")
		self.assertEqual(format_duration(5400), "1.50 hours")


class IntegrationTestResponseTime(IntegrationTestCase):
	"""
	Integration tests for ResponseTime.
	Use this class for testing interactions between multiple components.
	"""

	def test_number_card_call_accepts_filters(self):
		# The v16 number card widget calls custom methods with `filters`
		self.assertTrue(calculate_average_response_time(filters="[]"))
