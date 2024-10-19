# # Copyright (c) 2024, Nortex and contributors
# # For license information, please see license.txt

# import frappe
# from frappe.model.document import Document


# class ExRequests(Document):
# 	pass


# # ! Function to create new work order doc for manager 
# @frappe.whitelist()
# def create_work_order(event):
#     try: 
#         # ? This is to get the document fields
#         work_order = frappe.get_doc('Ex Requests', event)
        
#         # ? Getting and assigning the fields to each other
#         get_fields = frappe.get_doc({
#             'doctype': 'Ex Work Order',
#             'name1': event.location,
#             'room_number': event.room_number,
#             'other': event.other,
#             'request_code': event.id,
#             'date': event.date,
#             'time': event.time,
#             'further_information': event.further_description,
#             'issue': []
#         })
        
#         # ? For loop to get table contents
#         for item in event.table_umyd:
#             get_fields.append('issue', {
#                 'issue_type': item.issue_type,
#                 'description': item.description,
#             })		


#         get_fields.insert()
#         get_fields.submit()
#         work_order.save()

#         return get_fields.name

#     except Exception as e:
#         frappe.log_error(f"Error creating Work Order: {e}")
#         return str(e)



import frappe
from frappe.model.document import Document

class ExRequests(Document):
    # Hook into the document save event (this runs after the document is inserted)
    def after_insert(self):
        # Call the method to create the Work Order
        create_work_order(self)

# ! Function to create new work order doc for manager 
@frappe.whitelist()
def create_work_order(ex_request):
    try:
        # Create the new Work Order document
        work_order = frappe.get_doc({
            'doctype': 'Ex Work Order',
            'name1': ex_request.location,  # Assuming location is a field in Ex Request
            'room_number': ex_request.room_number,  # Field in Ex Request
            'other': ex_request.other,  # Other field
            'request_code': ex_request.name,  # The request document name (ID)
            'date': ex_request.date,  # Date field in Ex Request
            'time': ex_request.time,  # Time field
            'further_information': ex_request.further_description,  # Description
            'issue': []  # Empty table, we will populate it below
        })

        # ?Iterate over the child table (table_umyd) in Ex Requests, if it exists
        if ex_request.table_umyd:
            for item in ex_request.table_umyd:
                # Append each issue in the child table to the Work Order's issue field
                work_order.append('issue', {
                    'issue_type': item.issue_type,
                    'description': item.description
                })
        
        # ? Save the new Work Order (as draft)
        work_order.insert()

        frappe.msgprint(f"Work Order {work_order.name} created successfully!")
        return work_order.name

    except Exception as e:
        frappe.log_error(f"Error creating Work Order: {str(e)}")
        frappe.msgprint(f"Error: {str(e)}")
        return str(e)
