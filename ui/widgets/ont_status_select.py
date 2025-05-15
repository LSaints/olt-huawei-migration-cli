from textual.widgets import Select

ont_status_select = Select(
    id="select_status",
    options=[("offline","offline"), ("online","online")],
    value="offline",
    allow_blank=False
)