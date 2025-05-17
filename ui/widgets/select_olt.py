from textual.widgets import Select

select_olt = Select(
    id="select_olt",
    options=[("", "")],
    allow_blank=False,
    prompt="*Selecionar OLT"
)