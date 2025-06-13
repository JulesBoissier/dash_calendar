import pandas as pd

# Calendar configuration constants
WORK_START = "08:00"
WORK_END = "18:00"
TIME_FREQUENCY = "30min"
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
DEFAULT_COLOR = "#1fa22a"

def generate_time_slots():
    """Generate 30-minute time slots for the work day"""
    return pd.date_range(WORK_START, WORK_END, freq=TIME_FREQUENCY).strftime("%H:%M").tolist()

def initialize_calendar_data():
    """Initialize empty calendar grid data with proper structure"""
    slots = generate_time_slots()
    data = [{day: "" for day in WEEKDAYS} for _ in slots]
    
    # Add time column and tracking fields for each row
    for i, row in enumerate(data):
        row["time"] = slots[i]
        # Add span and color tracking for all days
        for day in WEEKDAYS:
            row[f"{day}_span"] = 1  # Default span of 1
            row[f"{day}_color"] = DEFAULT_COLOR  # Default green color
    
    return data

def get_calendar_column_definitions():
    """Define AG Grid column configuration for the calendar"""
    return [
        {
            "field": "time", 
            "pinned": "left", 
            "width": 90, 
            "headerName": "Time"
        },
        *[{
            "field": day,
            "editable": False,
            "onCellDoubleClicked": {"function": "doubleClickCallback"},
            "rowSpan": {"function": "rowSpanningSimple(params)"},
            "cellStyle": {"function": "getCellStyle(params)"},
        } for day in WEEKDAYS]
    ]

def get_grid_options():
    """Get AG Grid configuration options"""
    return {
        "rowHeight": 40, 
        "suppressRowTransform": True
    }

def get_default_column_definition():
    """Get default column configuration"""
    return {"resizable": True} 