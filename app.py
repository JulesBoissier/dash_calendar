"""
Calendar Application - Main Entry Point

A Dash application for managing weekly calendar events with:
- Event creation with custom colors and durations
- Event deletion with confirmation
- Conflict detection and resolution
- Row spanning for multi-slot events
"""

from dash import Dash
import dash_bootstrap_components as dbc
from layout import create_app_layout
import callbacks  # Import callbacks to register them

# Initialize Dash application
app = Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP], 
    suppress_callback_exceptions=True
)

# Set application layout
app.layout = create_app_layout()

# Application metadata
app.title = "Calendar - Event Manager"

if __name__ == "__main__":
    app.run(debug=True)
