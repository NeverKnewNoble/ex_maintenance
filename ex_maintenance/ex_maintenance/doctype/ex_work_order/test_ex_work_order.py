# Copyright (c) 2024, Nortex and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase, UnitTestCase

from ex_maintenance.ex_maintenance.doctype.ex_work_order.ex_work_order import (
	TEAM_ROLE,
	reopen_and_assign_to_both_tasks,
)
from ex_maintenance.setup.install import create_default_locations

# On IntegrationTestCase, the doctype test records and all
# link-field test record depdendencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]


def make_user(email, roles):
	if not frappe.db.exists("User", email):
		user = frappe.new_doc("User")
		user.update({"email": email, "first_name": email.split("@")[0], "send_welcome_email": 0})
		user.insert(ignore_permissions=True)
	user = frappe.get_doc("User", email)
	user.add_roles(*roles)
	return email


def make_request(**kwargs):
	"""Insert a request the way the public web form does (as Guest)."""
	create_default_locations()
	frappe.set_user("Guest")
	try:
		request = frappe.get_doc(
			{
				"doctype": "Ex Requests",
				"location": "Guest Room",
				"room_number": "101",
				"further_description": "Air conditioning is not cooling",
				"table_umyd": [{"issue_type": "Air conditioning/heating control", "description": "Warm air"}],
				**kwargs,
			}
		).insert(ignore_permissions=True)
	finally:
		frappe.set_user("Administrator")
	return request


def get_work_order(request):
	return frappe.get_doc("Ex Work Order", {"request_code": request.name})


class UnitTestExWorkOrder(UnitTestCase):
	"""
	Unit tests for ExWorkOrder.
	Use this class for testing individual functions and methods.
	"""

	def test_completion_time_follows_status(self):
		work_order = frappe.new_doc("Ex Work Order")
		work_order.status = "Completed"
		work_order.set_completion_time()
		self.assertTrue(work_order.completed_date)
		self.assertTrue(work_order.request_completed_time)

		work_order.status = "Open"
		work_order.set_completion_time()
		self.assertIsNone(work_order.completed_date)
		self.assertIsNone(work_order.request_completed_time)


class IntegrationTestExWorkOrder(IntegrationTestCase):
	"""
	Integration tests for ExWorkOrder.
	Use this class for testing interactions between multiple components.
	"""

	def test_guest_request_creates_work_order(self):
		request = make_request()

		self.assertTrue(request.request_date)
		self.assertTrue(request.request_time)

		work_order = get_work_order(request)
		self.assertEqual(work_order.location, "Guest Room")
		self.assertEqual(work_order.room_number, "101")
		self.assertEqual(len(work_order.issue), 1)

	def test_completion_records_one_response_time(self):
		work_order = get_work_order(make_request())

		work_order.status = "Completed"
		work_order.save()
		work_order.save()  # saving again must not add another Response Time

		self.assertTrue(work_order.completed_date)
		self.assertEqual(frappe.db.count("Response Time", {"management_document": work_order.name}), 1)

	def test_individual_assignment_creates_one_task_per_employee(self):
		employees = [
			make_user("ex-tech-1@example.com", [TEAM_ROLE]),
			make_user("ex-tech-2@example.com", [TEAM_ROLE]),
		]
		work_order = get_work_order(make_request())
		work_order.is_an_indvidual = 1
		for employee in employees:
			work_order.append("assign_task", {"employee": employee, "instructions": "Check the unit"})
		work_order.save()
		work_order.save()  # saving again must not duplicate tasks or ToDos

		tasks = frappe.get_all(
			"Task Assignments", filters={"doc_reference": work_order.name}, fields=["name", "assignee"]
		)
		self.assertEqual(sorted(t.assignee for t in tasks), sorted(employees))
		self.assertIn(work_order.task_assignment_reference, [t.name for t in tasks])

		for task in tasks:
			todos = frappe.get_all(
				"ToDo",
				filters={"reference_type": "Task Assignments", "reference_name": task.name, "status": "Open"},
				pluck="allocated_to",
			)
			self.assertEqual(todos, [task.assignee])

	def test_reopen_resets_completion_and_tasks(self):
		employee = make_user("ex-tech-1@example.com", [TEAM_ROLE])
		work_order = get_work_order(make_request())
		work_order.is_an_indvidual = 1
		work_order.append("assign_task", {"employee": employee, "instructions": "Fix it"})
		work_order.status = "Completed"
		work_order.save()

		reopen_and_assign_to_both_tasks(work_order.name)
		work_order.reload()

		self.assertEqual(work_order.status, "Open")
		self.assertIsNone(work_order.completed_date)
		self.assertEqual(
			frappe.db.get_value("Task Assignments", {"doc_reference": work_order.name}, "task_status"), "Open"
		)

	def test_team_member_only_sees_own_tasks(self):
		tech_1 = make_user("ex-tech-1@example.com", [TEAM_ROLE])
		tech_2 = make_user("ex-tech-2@example.com", [TEAM_ROLE])

		work_order = get_work_order(make_request())
		work_order.is_an_indvidual = 1
		work_order.append("assign_task", {"employee": tech_1, "instructions": "Fix it"})
		work_order.save()

		other_order = get_work_order(make_request())
		other_order.is_an_indvidual = 1
		other_order.append("assign_task", {"employee": tech_2, "instructions": "Fix it"})
		other_order.save()

		frappe.set_user(tech_1)
		try:
			visible = frappe.get_list("Task Assignments", pluck="doc_reference")
			self.assertIn(work_order.name, visible)
			self.assertNotIn(other_order.name, visible)
		finally:
			frappe.set_user("Administrator")

	def test_technician_completes_work_order_from_task(self):
		from ex_maintenance.ex_maintenance.doctype.task_assignments.task_assignments import (
			update_linked_document,
		)

		tech_1 = make_user("ex-tech-1@example.com", [TEAM_ROLE])
		tech_2 = make_user("ex-tech-2@example.com", [TEAM_ROLE])
		work_order = get_work_order(make_request())
		work_order.is_an_indvidual = 1
		work_order.append("assign_task", {"employee": tech_1, "instructions": "Fix it"})
		work_order.save()

		frappe.set_user(tech_2)
		try:
			with self.assertRaises(frappe.PermissionError):
				update_linked_document(work_order.name, "Completed", "Done")
		finally:
			frappe.set_user("Administrator")

		frappe.set_user(tech_1)
		try:
			self.assertEqual(update_linked_document(work_order.name, "Completed", "Done"), "success")
		finally:
			frappe.set_user("Administrator")

		work_order.reload()
		self.assertEqual(work_order.status, "Completed")
		self.assertIn(tech_1, work_order.status_change_logs)
		self.assertEqual(frappe.db.count("Response Time", {"management_document": work_order.name}), 1)
