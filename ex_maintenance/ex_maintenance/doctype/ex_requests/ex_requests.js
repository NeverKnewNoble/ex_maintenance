// Copyright (c) 2024, Nortex and contributors
// For license information, please see license.txt

// ? Function to get request time
frappe.ui.form.on("Ex Requests", {
    refresh(frm) {
        if (frm.is_new()) {
            frm.set_value('request_time', frappe.datetime.now_time());
            frm.set_value('request_date', frappe.datetime.now_date());
        }
    },
}); 


//  ? Function to call python function 
frappe.ui.form.on('Ex Requests', {
    onload(frm) {
        frm.add_custom_button('Create Work Order', function() {
            console.log('Create Work Order button clicked');

            frappe.call({
                method: 'ex_maintenance.ex_maintenance.doctype.ex_requests.ex_requests.create_work_order',
                args: {
                    event: {
                        location: frm.doc.location,
                        room_number: frm.doc.room_number,
                        other: frm.doc.other,
                        id: frm.doc.name,
                        date: frm.doc.date,
                        time: frm.doc.time,
                        further_description: frm.doc.further_information,
                        table_umyd: frm.doc.issue || []
                    }
                },
                callback: function(response) {
                    console.log('Response from create_work_order:', response);
                    if (!response.exc) {
                        frappe.msgprint('Work Order created with ID: ' + response.message);
                    } else {
                        frappe.msgprint('An error occurred: ' + response.exc);
                    }
                }
            });
        });
    }
});



//  ! Function To Get Location 
frappe.ui.form.on('Ex Requests', {
    refresh: function(frm) {
        set_location_based_options(frm); // Set options when form loads
    },
    location: function(frm) {
        set_location_based_options(frm); // Set options when location changes
    }
});

function set_location_based_options(frm) {
    // Get the options based on the selected location
    const location = frm.doc.location;
    const options = get_options_based_on_location(location);

    // Update the 'issue_type' field in the child table with the new options
    frm.fields_dict['table_umyd'].grid.update_docfield_property(
        'issue_type', 'options', options.join('\n')
    );
}

// Helper function to return options based on location
function get_options_based_on_location(location) {
    const issueOptions = {
        'Guest Room': [
            'Bed (king, queen, twin, etc.)',
            'Nightstand',
            'Dresser/Closet',
            'Desk/Workspace',
            'Television',
            'Safe',
            'Mini fridge/Minibar',
            'Coffee maker/kettle',
            'Iron and ironing board',
            'Alarm clock',
            'Seating area (armchair, sofa)',
            'Phone',
            'Air conditioning/heating control',
            'Full-length mirror',
            'Ensuite bathroom'
        ],
        'Lobby': [
            'Reception desk',
            'Seating area',
            'Information kiosk or concierge',
            'Luggage storage',
            'Digital information displays',
            'Magazine rack/newspaper stand',
            'Water station',
            'ATM',
            'Public restrooms',
            'Business center corner (computers, printer)'
        ],
        'Lounge Area': [
            'Comfortable seating (sofas, armchairs)',
            'Coffee tables',
            'Charging stations',
            'Magazines and newspapers',
            'Beverage service area',
            'Television(s)',
            'Art or decor installations',
            'Ambient lighting',
            'Speaker system'
        ],
        'Pool Area': [
            'Pool chairs/loungers',
            'Towels',
            'Umbrellas/shaded areas',
            'Poolside bar',
            'Lifeguard station (if applicable)',
            'Changing rooms and showers',
            'Hot tub/jacuzzi',
            'Pool toys or floaties',
            'Water fountain/drink station',
            'Rinsing station'
        ],
        'Gym/Fitness Center': [
            'Treadmills and cardio machines',
            'Weightlifting equipment (dumbbells, barbells)',
            'Yoga mats/stretching area',
            'Resistance bands',
            'Towels and water station',
            'Television(s)',
            'Mirrors',
            'Locker room',
            'Showers',
            'Sauna or steam room (sometimes)'
        ],
        'Spa': [
            'Treatment rooms (massage, facials)',
            'Relaxation lounge',
            'Aromatherapy station',
            'Sauna and steam rooms',
            'Jacuzzi/hot tub',
            'Showers',
            'Changing rooms/lockers',
            'Robes and slippers',
            'Tea/water station',
            'Reception and retail area (for spa products)'
        ],
        'Savana Bar/Hotel bar': [
            'Bar counter and seating',
            'High tables/stools',
            'Lounge seating',
            'Dance floor (if applicable)',
            'Live entertainment stage (if applicable)',
            'Menu displays',
            'Televisions',
            'Bar games (pool table, darts)',
            'Music system',
            'Beverage and snack menu'
        ],
        'Restaurant': [
            'Dining tables and chairs',
            'Host/Reception stand',
            'Menu stands/displays',
            'Bar or beverage counter',
            'Buffet stations (if applicable)',
            'Private dining area (in some cases)',
            'Tableware (utensils, glasses)',
            'High chairs/booster seats',
            'Kitchen (back-of-house)',
            'Restrooms nearby'
        ],
        'Conference Hall': [
            'Stage or podium',
            'Projector and screen',
            'Audio-visual equipment (microphones, speakers)',
            'Seating (movable or fixed)',
            'Lighting controls',
            'Presentation boards/whiteboards',
            'Charging stations',
            'Refreshment area (coffee, water)',
            'Restrooms nearby',
            'Registration desk (if needed)'
        ],
        'Meeting Room': [
            'Conference table',
            'Chairs',
            'Whiteboard or flip chart',
            'Projector or screen',
            'Telephone for conference calls',
            'Notepads and pens',
            'Refreshment station',
            'Video conferencing equipment',
            'Charging outlets',
            'Lighting controls'
        ],
        'Banquet Hall': [
            'Movable tables and chairs',
            'Stage or podium',
            'Dance floor',
            'Audio-visual equipment (speakers, mics)',
            'Buffet or catering area',
            'Decor options (lighting, drapes)',
            'Restrooms nearby',
            'Coat check area',
            'Bar setup (sometimes)'
        ],
        'Rooftop Bar': [
            'Seating (high tables, loungers)',
            'Bar counter',
            'Fire pits/heaters',
            'Lighting fixtures',
            'Umbrellas or awnings',
            'DJ booth (if applicable)',
            'Plants or greenery',
            'View points or telescopes',
            'Small dining area',
            'Ambient music'
        ],
        'Business Center': [
            'Computers',
            'Printers and scanners',
            'Fax machine',
            'Copy machine',
            'Workstations or desks',
            'Office supplies (stapler, paper, etc.)',
            'Charging stations',
            'Conference room booking service',
            'Telephones',
            'Secure internet access'
        ],
        'Elevators': [
            'Directory of floors',
            'Mirror or reflective panels',
            'Handrail',
            'Security camera',
            'Emergency buttons',
            'Soft lighting',
            'Braille panels for accessibility'
        ],
        'Parking Lot': [
            'Parking spaces',
            'EV charging stations',
            'Lighting poles',
            'Security cameras',
            'Signage for directions',
            'Handicap parking spots',
            'Payment kiosk (if applicable)',
            'Bicycle racks',
            'Loading zones'
        ],
        'Reception Desk': [
            'Concierge service',
            'Key card printing',
            'Luggage storage area',
            'Information brochures',
            'Charging stations',
            'Guest book or sign-in screen',
            'Digital signage',
            'ATM or currency exchange (sometimes)'
        ],
        'Garden/Patio': [
            'Seating (benches, tables)',
            'Pathways and walkways',
            'Water features (fountains, ponds)',
            'Plants and landscaping',
            'Gazebo or shaded area',
            'Outdoor lighting',
            'BBQ grills (in some patios)',
            'Playground (family-friendly hotels)',
            'Decorative sculptures'
        ],
        'Terrace': [
            'Seating (tables, loungers)',
            'Fire pits or heaters',
            'Umbrellas/shades',
            'Plants and greenery',
            'View points',
            'Lighting for evening ambiance',
            'Small bar or refreshment area',
            'Charging stations'
        ],
        'Ballroom': [
            'Stage or podium',
            'Dance floor',
            'Movable tables and chairs',
            'Lighting controls (chandeliers, spotlights)',
            'Audio-visual equipment (projectors, microphones)',
            'Buffet/catering area',
            'Coat check',
            'Restrooms nearby',
            'Decor setup options (drapes, lights)'
        ],
        'Valet Parking Area': [
            'Waiting area with seating',
            'Valet stand/booth',
            'Key storage rack',
            'Signage with valet rates',
            'Parking cones or markers',
            'Umbrella stand (for rainy weather)',
            'Security cameras',
            'Mobile payment system'
        ],
        'Other': [
            'General Inquiry',
            'Other'
        ]
    };

    // Return options for the selected location or a default if not found
    return issueOptions[location] || issueOptions['Other'];
}
