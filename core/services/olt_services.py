from typing import List
from core.domain.olt import Olt
from core.infra.olt_repository import OltRepository


class OltServices:
    def __init__(self):
        self.__repository = OltRepository()
        
    def buscar_olts(self) -> List[Olt]:
        olts = self.__repository.listar_olts()
        return olts
    
    def buscar_olt_por_nome(self, nome) -> Olt:
        olt = self.__repository.consultar_olt_por_nome(nome=nome)
        return olt
        