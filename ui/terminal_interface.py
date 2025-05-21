from typing import override

from rich.text import Text
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import DataTable, Static, Button, Input, Footer, Log

from core.services.olt_services import OltServices
from .widgets import input_gpon_origem, ont_status_select, btn_listar, btn_migrar, input_gpon_migrar, input_vlan_migrar, select_olt

from core.domain import Ont, Olt
from core.services import OntServices
from core.utils.logger import Logger
from .utils import StdoutRedirector
import sys

COLLUMNS = ("GPON", "ONT Id", "MAC", "Status", "Descrição")


class TerminalInterface(App):
    
    __olt_services = OltServices()
    __ont_services = OntServices()
    __logger = Logger()
    __onts = []
    __olts = []
    
    CSS_PATH = "terminal_interface.tcss"
    TITLE = "LIG OLTs - CLI"
    
    @override
    def compose(self) -> ComposeResult:
        
        self.gpon_origem_input = input_gpon_origem
        self.status_ont_select = ont_status_select
        self.gpon_origem_button = btn_listar
        self.migrar_button = btn_migrar
        self.gpon_destino_input = input_gpon_migrar
        self.vlan_destino_input = input_vlan_migrar
        self.tabela = DataTable(classes="table")
        self.select_olt = select_olt
        
        with Horizontal(id="olt-config-section"):
            yield self.select_olt
            
        with Horizontal(classes="input_list_gpon"):
            yield self.gpon_origem_input
            yield self.status_ont_select
            yield self.gpon_origem_button
            
            
        with Vertical(classes="table"):
            self.tabela.add_columns(*COLLUMNS)
            yield self.tabela
         
         
        with Horizontal(classes="input_list_gpon"):
            yield self.gpon_destino_input
            yield self.vlan_destino_input
            yield self.migrar_button
        
        
        with Static():
            yield Log(classes="log", auto_scroll=True)
        yield Footer()
        

    def on_mount(self) -> None:
        if len(self.__onts) > 0:
            self.TITLE = f"LIG OLTs - CLI -> Total de ONTs {len(__onts)}"  
            table = self.query_one(DataTable)
            table.add_columns(*COLLUMNS)
            for row in self.__onts:
                styled_row = [
                    Text(str(cell), style="italic #03AC13", justify="right") for cell in row
                ]
                table.add_row(*styled_row)
        pass
    
    
    @on(Input.Changed)
    def input_changed(self, event: Input.Changed) -> None:
        gpon_origem_input = self.query_one("#gpon_origem_input")
        gpon_origem_value = gpon_origem_input.value
        
        gpon_origem_button = self.query_one("#gpon_origem_button")
        
        if self.__input_gpon_is_valid(gpon_value=gpon_origem_value):
            gpon_origem_button.disabled = False
        else:
            gpon_origem_button.disabled = True
            
        
        vlan_destino_input = self.query_one("#vlan_input")
        vlan_destino_value = vlan_destino_input.value
        gpon_destino_input = self.query_one("#gpon_destino_input")
        gpon_destino_value = gpon_destino_input.value
        
        migrar_button = self.query_one("#migrar_button")
        
        if self.__input_gpon_is_valid(gpon_value=gpon_destino_value) and len(vlan_destino_value) > 2 and len(self.__onts) > 0:
            migrar_button.disabled = False
        else:
            migrar_button.disabled = True
           
            
    @on(Button.Pressed)
    async def on_button_pressed(self, event: Button.Pressed):
        
        if event.button.id == "gpon_origem_button":
            
            select_olt = self.query_one("#select_olt")
            select_olt_value = select_olt.value
            
            olt_info = self.__buscar_olt(select_olt_value)
            await self.__ont_services.definir_client_olt(
                host=olt_info.host, 
                usuario=olt_info.usuario, 
                senha=olt_info.senha
            )
            
            gpon_origem_input = self.query_one("#gpon_origem_input")
            gpon_origem_value = gpon_origem_input.value
            
            select_status_ont = self.query_one("#select_status")
            select_status_ont_value = select_status_ont.value
            
            await self.__load_data(
                gpon_origem=gpon_origem_value, 
                status_ont=select_status_ont_value
            )
        
        if event.button.id == "migrar_button":
            gpon_destino_input = self.query_one("#gpon_destino_input")
            gpon_destino_value = gpon_destino_input.value
            
            vlan_destino_input = self.query_one("#vlan_input")
            vlan_destino_value = vlan_destino_input.value
            
            await self.__migrar_onts(gpon_destino=gpon_destino_value, vlan_destino=vlan_destino_value)
              
   
    def __buscar_olt(self, nome: str) -> Olt:
       olt = self.__olt_services.buscar_olt_por_nome(nome)
       return olt
    
    async def __migrar_onts(self, gpon_destino: str, vlan_destino: str):
        onts = [Ont(gpon=t[0], id=t[1], mac=t[2], status=t[3], descricao=t[4]) for t in self.__onts]
        await self.__ont_services.migrar_onts(
            onts=onts,
            gpon_destino=gpon_destino, 
            vlan_destino=vlan_destino
        )
    
    async def __load_data(self, gpon_origem: str, status_ont: str) -> None:
        
        onts_result = await self.__ont_services.listar_onts(status=status_ont, gpon=gpon_origem)
        self.__onts = [(ont.gpon, ont.id, ont.mac, ont.status, ont.descricao) for ont in onts_result]
        self.__logger.gerar_log_onts(onts=onts_result)
        self.__refresh_table()

    
    def __load_olts(self) -> None:
        log = self.query_one(Log)
        log.clear()
        olts_result = self.__olt_services.buscar_olts()
        self.__olts = [(f"{olt.nome} - {olt.host}", f"{olt.nome} - {olt.host}") for olt in olts_result]
        select_olt = self.select_olt
        select_olt.set_options(self.__olts)
        
        
    def __refresh_table(self) -> None:
        table = self.query_one(DataTable)
        table.clear(columns=False)
        for number, row in enumerate(self.__onts, start=1):
            label = Text(str(number), style="#00ff00 italic")
            styled_row = [
                Text(str(cell), style="italic #03AC13", justify="right") for cell in row
            ]
            table.add_row(*styled_row, label=label)
    
    
    def on_ready(self) -> None:
        log = self.query_one(Log)
        sys.stdout = StdoutRedirector(log)
        self.__load_olts()
        
            
    def __input_gpon_is_valid(self, gpon_value) -> bool:
        if len(gpon_value) > 2 and "/" in gpon_value:
            return True
        else: 
            return False
        