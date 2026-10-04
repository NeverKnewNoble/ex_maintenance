# Copyright (c) 2026, Nortex and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase

from ex_maintenance.api.locations import get_request_options, search_location_issues, search_locations
from ex_maintenance.setup.default_locations import DEFAULT_LOCATIONS
from ex_maintenance.setup.install import create_default_locations


def set_facility_type(facility_type):
	frappe.db.set_single_value("Maintenance Settings", "facility_type", facility_type)


class IntegrationTestMaintenanceLocation(IntegrationTestCase):
	def setUp(self):
		create_default_locations()
		set_facility_type("All")

	def test_defaults_cover_all_facility_types(self):
		for facility_type in ("General", "Hotel", "School", "Office"):
			self.assertTrue(frappe.db.exists("Maintenance Location", {"facility_type": facility_type}))
		self.assertEqual(
			len(frappe.get_doc("Maintenance Location", "Classroom").issues),
			len(next(loc for loc in DEFAULT_LOCATIONS if loc["location_name"] == "Classroom")["issues"]),
		)

	def test_creating_defaults_twice_is_safe(self):
		count = frappe.db.count("Maintenance Location")
		create_default_locations()
		self.assertEqual(frappe.db.count("Maintenance Location"), count)

	def test_facility_type_filters_locations(self):
		set_facility_type("School")
		names = [row[0] for row in search_locations("Maintenance Location", "", "name", 0, 500, {})]
		self.assertIn("Classroom", names)
		self.assertIn("Restrooms", names)  # General
		self.assertNotIn("Guest Room", names)
		self.assertNotIn("Boardroom", names)

		options = get_request_options()
		self.assertIn("Classroom", options["requires_room_number"])
		self.assertNotIn("Guest Room", options["locations"])

	def test_disabled_location_is_hidden_and_rejected(self):
		frappe.db.set_value("Maintenance Location", "Playground", "disabled", 1)
		self.assertNotIn("Playground", get_request_options()["locations"])

		request = frappe.get_doc({"doctype": "Ex Requests", "location": "Playground"})
		with self.assertRaises(frappe.ValidationError):
			request.insert(ignore_permissions=True)

	def test_issue_search_uses_location_issues(self):
		issues = [
			row[0]
			for row in search_location_issues(
				"Maintenance Issue", "", "name", 0, 500, {"location": "Server Room"}
			)
		]
		self.assertIn("Server racks", issues)
		self.assertNotIn("Beds and mattresses", issues)

	def test_room_number_required_for_room_locations(self):
		request = frappe.get_doc({"doctype": "Ex Requests", "location": "Classroom"})
		with self.assertRaises(frappe.ValidationError):
			request.insert(ignore_permissions=True)

		request.room_number = "B12"
		request.insert(ignore_permissions=True)
		self.assertEqual(
			frappe.db.get_value("Ex Work Order", {"request_code": request.name}, "location"), "Classroom"
		)
