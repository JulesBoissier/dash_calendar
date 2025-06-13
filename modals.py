import dash_bootstrap_components as dbc
from dash import html

# Create Event Modal
create_event_modal = dbc.Modal([
    dbc.ModalHeader("Create Event"),
    dbc.ModalBody([
        dbc.Label("Event Title"),
        dbc.Input(id="event-title", value="New Event"),
        dbc.Label("Duration (30-min increments)"),
        dbc.Input(id="event-length", type="number", value=1, min=1, max=5),
        dbc.Label("Event Color"),
        dbc.Input(id="event-color", type="color", value="#1fa22a")
    ]),
    dbc.ModalFooter(
        dbc.Button("Submit", id="submit-event", color="primary")
    ),
], id="event-modal", is_open=False)

# Delete Event Modal
delete_event_modal = dbc.Modal([
    dbc.ModalHeader("Delete Event"),
    dbc.ModalBody([
        html.P(id="delete-event-text", children="Are you sure you want to delete this event?"),
        html.P(id="event-details", style={"fontWeight": "bold", "color": "#d32f2f"})
    ]),
    dbc.ModalFooter([
        dbc.Button("Delete", id="confirm-delete", color="danger"),
        dbc.Button("Cancel", id="cancel-delete", color="secondary", className="ms-2")
    ]),
], id="delete-modal", is_open=False)

# Conflict Warning Modal
conflict_warning_modal = dbc.Modal([
    dbc.ModalHeader("Event Conflict Detected", style={"color": "#d32f2f"}),
    dbc.ModalBody([
        html.P("The new event conflicts with existing events:"),
        html.Div(id="conflict-details", style={"fontWeight": "bold", "color": "#d32f2f", "marginBottom": "15px"}),
        html.P("Do you want to override the existing events?"),
        dbc.Alert([
            html.I(className="fas fa-exclamation-triangle me-2"),
            "This will permanently delete the conflicting events."
        ], color="warning")
    ]),
    dbc.ModalFooter([
        dbc.Button("Override", id="confirm-override", color="danger"),
        dbc.Button("Cancel", id="cancel-override", color="secondary", className="ms-2")
    ]),
], id="conflict-modal", is_open=False) 