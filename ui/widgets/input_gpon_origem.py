from textual.widgets import Input

input_gpon_origem = Input(
    placeholder="GPON de origem EX: 0/10/10 ou 0/1/1",
    id="gpon_origem_input",
    classes="content",
    valid_empty=True,
    max_length=10,
)