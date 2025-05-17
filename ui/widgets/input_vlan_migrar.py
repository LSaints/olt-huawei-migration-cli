from textual.widgets import Input

input_vlan_migrar = Input(
    placeholder="VLAN de Destino EX: 1212",
    id="vlan_input",
    classes="content",
    valid_empty=True,
    max_length=6,
)