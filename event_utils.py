from dash import html
from calendar_config import DEFAULT_COLOR

def check_for_conflicts(rows, col, start, length):
    """
    Check if creating an event would conflict with existing events
    
    Args:
        rows: Calendar grid data
        col: Column (day) to check
        start: Starting row index
        length: Number of rows the event will span
    
    Returns:
        List of conflict descriptions, empty if no conflicts
    """
    conflicts = []
    for i in range(length):
        idx = start + i
        if idx < len(rows) and rows[idx][col] and rows[idx][col].strip():
            time_slot = rows[idx]["time"]
            event_name = rows[idx][col]
            conflicts.append(f"• {event_name} at {time_slot}")
    
    return conflicts

def format_conflict_details(conflicts):
    """
    Format conflict list into HTML components for display
    
    Args:
        conflicts: List of conflict strings
    
    Returns:
        List of HTML components for display
    """
    if not conflicts:
        return []
    
    return [
        html.P("The following events will be overwritten:", style={"marginBottom": "10px"}),
        *[html.P(
            conflict.replace('• ', ''), 
            style={"marginBottom": "5px", "marginLeft": "20px"}
        ) for conflict in conflicts]
    ]

def create_event_in_grid(rows, title, length, color, col, start):
    """
    Create an event in the calendar grid
    
    Args:
        rows: Calendar grid data
        title: Event title
        length: Number of time slots to span
        color: Event color (hex)
        col: Column (day) to place event
        start: Starting row index
    
    Returns:
        Updated rows data
    """
    # Set the event in the first cell with the specified span and color
    if start < len(rows):
        rows[start][col] = title
        rows[start][f"{col}_span"] = length
        rows[start][f"{col}_color"] = color or DEFAULT_COLOR
            
    # Clear content from subsequent cells that will be spanned over
    for i in range(1, length):
        idx = start + i
        if idx < len(rows):
            rows[idx][col] = ""  # Empty content for spanned cells
            rows[idx][f"{col}_span"] = 1  # Keep default span for these cells
            rows[idx][f"{col}_color"] = color or DEFAULT_COLOR  # Use same color

    return rows

def delete_event_from_grid(rows, col, start):
    """
    Delete an event from the calendar grid
    
    Args:
        rows: Calendar grid data
        col: Column (day) containing the event
        start: Starting row index of the event
    
    Returns:
        Updated rows data
    """
    if start < len(rows):
        span = rows[start].get(f"{col}_span", 1)
        
        # Reset only the starting cell
        rows[start][col] = ""
        rows[start][f"{col}_span"] = 1
        rows[start][f"{col}_color"] = DEFAULT_COLOR
        
    return rows

def format_event_info(event_title, span, time_slot):
    """
    Format event information for display in delete modal
    
    Args:
        event_title: Title of the event
        span: Number of time slots the event spans
        time_slot: Starting time slot
    
    Returns:
        Formatted event info string
    """
    slot_text = "slot" if span == 1 else "slots"
    return f'"{event_title}" at {time_slot} ({span} {slot_text})'

def validate_event_length(length):
    """
    Validate and normalize event length
    
    Args:
        length: Raw length input
    
    Returns:
        Validated length (minimum 1)
    """
    return max(1, length or 1) 