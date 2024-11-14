// Copyright (c) 2024, Nortex and contributors
// For license information, please see license.txt

frappe.query_reports["Work Order Report"] = {
    "filters": [
        {
            "fieldname": "status",
            "label": __("Status"),
            "fieldtype": "Select",
            "options": "\nOpen\nIn Progress\nCompleted\nOverdue", 
            "width": 80
        },
		{
            "fieldname": "priority_level",
            "label": __("Priority Level"),
            "fieldtype": "Select",
            "options": "\nLow\nMedium\nHigh\nUrgent", 
            "width": 80
        },
		{
            "fieldname": "location",
            "label": __("Location"),
            "fieldtype": "Select",
			"options": "\nGuest Room\nLobby\nLounge Area\nPool Area\nGym/Fitness Center\nSpa\nSavana Bar/Hotel bar\nRestaurant\nConference Hall\nMeeting Room\nBanquet Hall\nRooftop Bar\nBusiness Center\nElevators\nParking Lot\nReception Desk\nGarden/Patio\nTerrace\nBallroom\nValet Parking Area\nOther",
            "width": 80
        },
		{
            "fieldname": "request_date_created",
            "label": __("Request Date Created"),
            "fieldtype": "Date",
            "width": 80
        },
		{
            "fieldname": "request_time_created",
            "label": __("Request Time Created"),
            "fieldtype": "Time",
            "width": 80
        },

    ]
};
