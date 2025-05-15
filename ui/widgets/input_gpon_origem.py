from textual.widgets import Input

input_gpon_origem = Input(
    placeholder="GPON de origem",
    id="gpon_origem_input",
    classes="content",
    valid_empty=True,
    max_length=10,
)