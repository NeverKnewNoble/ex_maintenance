import frappe
from frappe import _
from frappe.auth import LoginManager


# ? --------------- API POST CALL TO LOG IN ----------------------------
# Logs the user in through Frappe's LoginManager (lockout, disabled users, 2FA, IP rules)
# and starts a session: the app must keep the `sid` cookie and send it on later API calls.
@frappe.whitelist(allow_guest=True, methods=["POST"])
def verify_login(username, password):
	frappe.form_dict.update({"usr": username, "pwd": password})
	login_manager = LoginManager()

	try:
		logged_in = login_manager.login() is not False
	except frappe.AuthenticationError:
		frappe.clear_messages()
		frappe.local.response["http_status_code"] = 401
		logged_in = False

	if not logged_in:
		return {"status": "failed", "message": _("Invalid login credentials")}

	return {
		"status": "success",
		"message": _("Login successful"),
		"full_name": frappe.db.get_value("User", frappe.session.user, "full_name"),
	}


# http://127.0.0.1:8001/api/v2/method/ex_maintenance.api.login.verify_login
