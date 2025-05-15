from textual.widgets import Input

input_vlan_migrar = Input(
    placeholder="VLAN de Destino",
    id="vlan_input",
    classes="content",
    valid_empty=True,
    max_length=6,
)