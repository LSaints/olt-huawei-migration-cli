from typing import List

from core.domain.olt import Olt
from .olt_txt_mapper import OltTxtMapper


class OltRepository:
    def __init__(self):
        self.__txt_mapper = OltTxtMapper("./data/olts.txt")
    
    def listar_olts(self) -> List[Olt]:
        olts = self.__txt_mapper.retornar_lista_olt()
        return olts
    
    def consultar_olt_por_nome(self, nome: str) -> Olt:
        olt = self.__txt_mapper.filtrar_olt_nome(nome)
        return olt