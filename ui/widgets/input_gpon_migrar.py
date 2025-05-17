from textual.widgets import Input

input_gpon_migrar = Input(
    placeholder="GPON de Destino EX: 0/10/10 ou 0/1/1",
    id="gpon_destino_input",
    classes="content",
    valid_empty=True,
    max_length=10,
)