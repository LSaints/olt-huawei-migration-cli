from core.domain import Ont
from typing import List

from core.infra import OltRepository, ClientTelnet

class OltServices:
    
    def __init__(self):
        self.__client_telnet = ClientTelnet(
            host='10.55.160.2',
            usuario="smartolt",
            senha="rJXf2JA1p4NjTui"
        )
        self.__repository = OltRepository(cliente=self.__client_telnet)
        
    async def listar_onts(self, status: str, gpon: str) -> List[Ont]:
        onts = await self.__repository.listar_onts(status=status, gpon=gpon)
        self.__show_text(f"LISTANDO {len(onts)} ONTs")        
        for ont in onts:
            print(f"ID  => {ont.id}\nDESC => {ont.descricao}")
        return onts

    async def migrar_onts(self, onts: List[Ont], gpon_destino: str, vlan_destino: str) -> None:
        self.__show_text("REMOVENDO ONTS")
        for ont in onts:
            await self.__repository.desprovisionar_ont(ont=ont)
        
        self.__show_text("ADICIONANDO ONTS")
        for ont in onts:
            pass
            await self.__repository.provisionar_ont(
                ont=ont, 
                gpon_destino=gpon_destino, 
                vlan=vlan_destino
            )
        self.__show_text("concluído")
        
        
    def __show_text(self, title: str):
        print("="*100)
        print(f"\n{title}\n")
        print("="*100)
    