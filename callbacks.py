import dash
from dash import callback, Output, Input, State, ctx
from event_utils import (
    check_for_conflicts,
    format_conflict_details,
    create_event_in_grid,
    delete_event_from_grid,
    format_event_info,
    validate_event_length
)

@callback(
    Output("event-modal", "is_open"),
    Output("delete-modal", "is_open"), 
    Output("selected-cell", "data"),
    Output("event-details", "children"),  # An html.P tag within the delete-modal
    Input("calendar-grid", "cellDoubleClicked"),
    State("calendar-grid", "rowData"),
    prevent_initial_call=True
)
def handle_cell_double_click(cell_click, rows):
    """Handle double-click events on calendar cells"""
    
    col = cell_click["colId"]
    row_idx = cell_click["rowIndex"]
    
    # Check if the clicked cell has content
    if row_idx < len(rows) and rows[row_idx][col]:
        # Cell has content - show delete modal
        event_title = rows[row_idx][col]
        span = rows[row_idx].get(f"{col}_span", 1)
        time_slot = rows[row_idx]["time"]
        event_info = format_event_info(event_title, span, time_slot)
        return False, True, cell_click, event_info
    else:
        # Cell is empty - show create modal
        return True, False, cell_click, dash.no_update

@callback(
    Output("delete-modal", "is_open", allow_duplicate=True),
    Input("cancel-delete", "n_clicks"),
    prevent_initial_call=True
)
def handle_delete_modal_cancel(cancel_clicks):
    """Handle cancel button in delete modal"""
    
    if cancel_clicks:
        return False
    
    return dash.no_update

@callback(
    Output("calendar-grid", "rowData"),
    Output("event-modal", "is_open", allow_duplicate=True),
    Output("conflict-modal", "is_open"),
    Output("conflict-details", "children"),
    Output("pending-event", "data"),
    Input("submit-event", "n_clicks"),
    State("event-title", "value"),
    State("event-length", "value"),
    State("event-color", "value"),
    State("selected-cell", "data"),
    State("calendar-grid", "rowData"),
    prevent_initial_call=True
)
def handle_event_creation(_, title, length, color, cell_data, rows):
    """Handle event creation from the create modal"""
    
    if not cell_data:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    col = cell_data["colId"]
    start = cell_data["rowIndex"]
    length = validate_event_length(length)
    
    print(f"DEBUG: Creating event '{title}' with color '{color}' at {col}[{start}] spanning {length} rows")

    # Check for conflicts in the target area
    conflicts = check_for_conflicts(rows, col, start, length)
    
    # If conflicts exist, show conflict modal
    if conflicts:
        conflict_text = format_conflict_details(conflicts)
        
        # Store the pending event data
        pending_data = {
            "title": title,
            "length": length,
            "color": color,
            "col": col,
            "start": start
        }
        
        print(f"DEBUG: Conflict detected! Events: {conflicts}")
        return dash.no_update, False, True, conflict_text, pending_data
    
    # No conflicts - proceed with creating the event
    updated_rows = create_event_in_grid(rows, title, length, color, col, start)
    return updated_rows, False, dash.no_update, dash.no_update, None

@callback(
    Output("calendar-grid", "rowData", allow_duplicate=True),
    Output("delete-modal", "is_open", allow_duplicate=True),
    Input("confirm-delete", "n_clicks"),
    State("selected-cell", "data"),
    State("calendar-grid", "rowData"),
    prevent_initial_call=True
)
def handle_event_deletion(confirm_clicks, cell_data, rows):
    """Handle event deletion from the delete modal"""
    
    if not cell_data or not confirm_clicks:
        return dash.no_update, dash.no_update

    col = cell_data["colId"]
    start = cell_data["rowIndex"]
    
    updated_rows = delete_event_from_grid(rows, col, start)
    return updated_rows, False

@callback(
    Output("calendar-grid", "rowData", allow_duplicate=True),
    Output("conflict-modal", "is_open", allow_duplicate=True),
    Output("pending-event", "data", allow_duplicate=True),
    Input("confirm-override", "n_clicks"),
    Input("cancel-override", "n_clicks"),
    State("pending-event", "data"),
    State("calendar-grid", "rowData"),
    prevent_initial_call=True
)
def handle_conflict_resolution(override_clicks, cancel_clicks, pending_data, rows):
    """Handle conflict resolution (override or cancel)"""
    
    if ctx.triggered_id == "cancel-override":
        # User cancelled - just close modal and clear pending data
        return dash.no_update, False, None
    
    if ctx.triggered_id == "confirm-override" and pending_data:
        # User confirmed override - create the event
        title = pending_data["title"]
        length = pending_data["length"]
        color = pending_data["color"]
        col = pending_data["col"]
        start = pending_data["start"]
        
        print(f"DEBUG: Override confirmed - creating event '{title}' at {col}[{start}]")
        
        # Create the event (this will overwrite existing events)
        updated_rows = create_event_in_grid(rows, title, length, color, col, start)
        return updated_rows, False, None
    
    return dash.no_update, dash.no_update, dash.no_update 