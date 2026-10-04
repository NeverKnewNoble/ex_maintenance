# Copyright (c) 2024, Nortex and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import format_datetime, now_datetime

TEAM_ROLE = "Ex Maintenance Team Member"
MANAGER_ROLES = {"System Manager", "Ex Maintenance Manager"}


class TaskAssignments(Document):
	pass


# ! Team members only see the tasks they are assigned to (directly or as part of the team)
def _is_restricted(user):
	roles = set(frappe.get_roles(user))
	return TEAM_ROLE in roles and not roles & MANAGER_ROLES


def get_permission_query_conditions(user=None):
	user = user or frappe.session.user
	if not _is_restricted(user):
		return ""

	assignee, assigned = frappe.db.escape(user), frappe.db.escape(f'%"{user}"%')
	return f"(`tabTask Assignments`.assignee = {assignee} or `tabTask Assignments`._assign like {assigned})"


def has_permission(doc, ptype=None, user=None, debug=False):
	user = user or frappe.session.user
	if not _is_restricted(user):
		return True

	return doc.assignee == user or user in frappe.parse_json(doc.get("_assign") or "[]")


# ! Update the Work Order with the technician's progress
@frappe.whitelist()
def update_linked_document(doc_reference, task_status, description_on_the_task, attach_work_progress=None):
	if isinstance(doc_reference, str) and doc_reference.lstrip().startswith("{"):
		doc_reference = frappe.parse_json(doc_reference)
	if isinstance(doc_reference, dict):
		if doc_reference.get("doctype", "Ex Work Order") != "Ex Work Order":
			frappe.throw(_("Only Ex Work Orders can be updated from a Task Assignment."))
		doc_reference = doc_reference.get("name")

	work_order = frappe.get_doc("Ex Work Order", doc_reference)
	if not _can_update(work_order):
		frappe.throw(_("You are not assigned to this Work Order."), frappe.PermissionError)

	timestamp = format_datetime(now_datetime(), "MMM dd, yyyy hh:mm a")
	new_log_entry = f"{frappe.session.user} updated this document on {timestamp}"

	work_order.status = task_status
	work_order.description_on_the_task = description_on_the_task
	work_order.attach_image_rypl = attach_work_progress or ""
	work_order.status_change_logs = "\n".join(filter(None, [work_order.status_change_logs, new_log_entry]))

	# Technicians don't have access to Work Orders; _can_update() has checked they are assigned
	work_order.save(ignore_permissions=True)
	return "success"


def _can_update(work_order):
	if frappe.has_permission("Ex Work Order", "write", work_order):
		return True

	# get_list applies the Task Assignments permission rules above
	return bool(frappe.get_list("Task Assignments", filters={"doc_reference": work_order.name}, limit=1))
