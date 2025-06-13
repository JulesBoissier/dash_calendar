from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
from modals import create_event_modal, delete_event_modal, conflict_warning_modal
from calendar_config import (
    initialize_calendar_data, 
    get_calendar_column_definitions,
    get_grid_options,
    get_default_column_definition
)

def create_app_layout():
    """Create and return the main application layout"""
    
    # Initialize calendar data and configuration
    calendar_data = initialize_calendar_data()
    column_definitions = get_calendar_column_definitions()
    grid_options = get_grid_options()
    default_col_def = get_default_column_definition()
    
    return dbc.Container([
        # Data stores for managing application state
        dcc.Store(id="selected-cell"),
        dcc.Store(id="pending-event", data=None),
        
        # Modal components
        create_event_modal,
        delete_event_modal,
        conflict_warning_modal,
        
        # Header section
        html.Div([
            html.H4("Calendar", className="mb-2"),
            html.P(
                "Double-click empty cells to create events. Double-click existing events to delete them.", 
                style={"color": "#666", "fontStyle": "italic"},
                className="mb-4"
            ),
        ]),
        
        # Calendar grid
        dag.AgGrid(
            id="calendar-grid",
            columnDefs=column_definitions,
            rowData=calendar_data,
            columnSize="sizeToFit",
            defaultColDef=default_col_def,
            dashGridOptions=grid_options,
            style={"height": "600px"},
        ),
    ]) 