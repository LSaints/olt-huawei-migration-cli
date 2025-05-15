from textual.widgets import Input

input_gpon_migrar = Input(
    placeholder="GPON de Destino",
    id="gpon_destino_input",
    classes="content",
    valid_empty=True,
    max_length=10,
)