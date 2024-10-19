# Copyright (c) 2024, Nortex and Contributors
# See license.txt

# import frappe
from frappe.tests import IntegrationTestCase, UnitTestCase


# On IntegrationTestCase, the doctype test records and all
# link-field test record depdendencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]


class TestExWorkOrder(UnitTestCase):
	"""
	Unit tests for ExWorkOrder.
	Use this class for testing individual functions and methods.
	"""

	pass


class TestExWorkOrder(IntegrationTestCase):
	"""
	Integration tests for ExWorkOrder.
	Use this class for testing interactions between multiple components.
	"""

	pass
