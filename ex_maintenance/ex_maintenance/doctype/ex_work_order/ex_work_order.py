# Copyright (c) 2024, Nortex and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.desk.form.assign_to import add as add_assignment
from frappe.model.document import Document
from frappe.utils import nowdate, nowtime

TEAM_ROLE = "Ex Maintenance Team Member"
TASK_STATUSES = ("Open", "In Progress", "Completed")


class ExWorkOrder(Document):
	def validate(self):
		self.set_completion_time()

	def on_update(self):
		self.sync_task_assignments()

		if self.status == "Completed" and self.has_value_changed("status"):
			self.record_response_time()

	def set_completion_time(self):
		if self.status != "Completed":
			self.completed_date = None
			self.request_completed_time = None
		elif not self.completed_date:
			self.completed_date = nowdate()
			self.request_completed_time = nowtime()

	# ! Create / update one Task Assignment per employee, or one shared by the whole team
	def sync_task_assignments(self):
		if self.is_an_indvidual:
			for row in self.assign_task:
				if row.employee:
					self.sync_task_assignment(
						assignee=row.employee,
						instructions=row.instructions,
						assign_to=[row.employee],
						description=_("Assigned task based on instructions: {0}").format(
							row.instructions or ""
						),
					)

		if self.is_a_team:
			self.sync_task_assignment(
				assignee=None,
				instructions=self.team_descriptioninstructions,
				assign_to=get_team_members(),
				description=_("Assigned task to team: {0}").format(self.team_descriptioninstructions or ""),
			)

	def sync_task_assignment(self, assignee, instructions, assign_to, description):
		name = frappe.db.get_value(
			"Task Assignments", {"doc_reference": self.name, "assignee": assignee or ("is", "not set")}
		)
		task = frappe.get_doc("Task Assignments", name) if name else frappe.new_doc("Task Assignments")
		before = _task_snapshot(task)

		task.update(
			{
				"doc_reference": self.name,
				"assignee": assignee,
				"request_code": self.request_code,
				"priority": self.priority_level,
				"instructions": instructions,
				"deadline_set_date": self.deadline_date,
				"deadline_set_time": self.deadline_time,
			}
		)
		# Only push the status when the manager changed it, so a technician's progress isn't overwritten
		if self.status in TASK_STATUSES and (task.is_new() or self.has_value_changed("status")):
			task.task_status = self.status
		task.set("issue", [{"issue_type": i.issue_type, "description": i.description} for i in self.issue])

		if task.is_new() or _task_snapshot(task) != before:
			task.save(ignore_permissions=True)

		if not self.task_assignment_reference:
			self.db_set("task_assignment_reference", task.name)

		assign_users(task.name, assign_to, description)

	def record_response_time(self):
		if not self.request_code:
			return

		name = frappe.db.get_value("Response Time", {"management_document": self.name})
		response = frappe.get_doc("Response Time", name) if name else frappe.new_doc("Response Time")
		response.update(
			{
				"management_document": self.name,
				"request_document": self.request_code,
				"completed_date": self.completed_date,
				"completed_time": self.request_completed_time,
			}
		)
		response.save(ignore_permissions=True)


def _task_snapshot(task):
	fields = (
		"assignee",
		"request_code",
		"priority",
		"instructions",
		"deadline_set_date",
		"deadline_set_time",
		"task_status",
	)
	return (
		tuple(str(task.get(f) or "") for f in fields),
		tuple((i.issue_type, i.description) for i in task.get("issue", [])),
	)


def get_team_members():
	users = frappe.get_all("Has Role", filters={"role": TEAM_ROLE, "parenttype": "User"}, pluck="parent")
	if not users:
		return []
	return frappe.get_all("User", filters={"name": ["in", users], "enabled": 1}, pluck="name")


def assign_users(task_name, users, description):
	"""Add a ToDo for every user that doesn't already have an open one on this task."""
	already_assigned = set(
		frappe.get_all(
			"ToDo",
			filters={"reference_type": "Task Assignments", "reference_name": task_name, "status": "Open"},
			pluck="allocated_to",
		)
	)
	new_users = [user for user in users if user not in already_assigned]
	if new_users:
		add_assignment(
			{
				"assign_to": new_users,
				"doctype": "Task Assignments",
				"name": task_name,
				"description": description,
				"notify": 1,
			}
		)


# ! Reopen the Work Order; saving it re-syncs and reassigns the Task Assignments
@frappe.whitelist()
def reopen_and_assign_to_both_tasks(ex_work_order_name):
	work_order = frappe.get_doc("Ex Work Order", ex_work_order_name)
	work_order.check_permission("write")

	if not (work_order.is_a_team or work_order.is_an_indvidual):
		frappe.throw(_("Please specify whether the assignment is for a team or an individual."))

	work_order.status = "Open"
	work_order.save()


# ? Older endpoints, kept so existing callers (e.g. the mobile app) keep working.
# Task Assignments and Response Time are now handled in ExWorkOrder.on_update.
@frappe.whitelist()
def reopen_and_reassign_task(ex_work_order_name):
	reopen_and_assign_to_both_tasks(ex_work_order_name)


@frappe.whitelist()
def reopen_and_assign_to_team(ex_work_order_name):
	reopen_and_assign_to_both_tasks(ex_work_order_name)


@frappe.whitelist()
def create_task_assignment(ex_work_order):
	_get_work_order_for_update(ex_work_order).sync_task_assignments()


@frappe.whitelist()
def assign_to_team(ex_work_order):
	_get_work_order_for_update(ex_work_order).sync_task_assignments()


def _get_work_order_for_update(ex_work_order):
	if isinstance(ex_work_order, str) and ex_work_order.lstrip().startswith("{"):
		ex_work_order = frappe.parse_json(ex_work_order)
	name = ex_work_order.get("name") if isinstance(ex_work_order, dict) else ex_work_order

	work_order = frappe.get_doc("Ex Work Order", name)
	work_order.check_permission("write")
	return work_order
