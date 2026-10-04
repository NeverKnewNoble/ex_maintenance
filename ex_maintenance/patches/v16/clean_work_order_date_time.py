import frappe
from frappe.utils import get_datetime


def execute():
	"""Ex Work Order `date` and `time` change from Data to Date/Time.

	Blank or unparsable values would make the column type change fail, so they are cleared
	(or normalised) before the schema sync.
	"""
	if not frappe.db.table_exists("Ex Work Order"):
		return

	for name, date, time in frappe.db.sql("select name, `date`, `time` from `tabEx Work Order`"):
		values = {"date": _normalise(date, "date"), "time": _normalise(time, "time")}
		if values != {"date": date, "time": time}:
			frappe.db.set_value("Ex Work Order", name, values, update_modified=False)


def _normalise(value, part):
	if not value or not str(value).strip():
		return None
	try:
		if part == "date":
			return str(get_datetime(str(value)).date())
		return str(get_datetime(f"2000-01-01 {value}").time())
	except Exception:
		return None
