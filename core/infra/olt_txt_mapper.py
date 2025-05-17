from typing import List

from core.domain import Olt


class OltTxtMapper:
    def __init__(self, dir: str) -> None:
        self.__dir = dir
    
    def retornar_lista_olt(self) -> List[Olt]:
        olts = self.__map(self.__dir)
        return olts
    
    def filtrar_olt_nome(self, nome: str) -> Olt:
        olts = self.__map(self.__dir)
        for olt in olts:
            if olt.nome in nome:
                return olt
    
    def __map(self, dir: str) -> List[Olt]:
        olts_split = []
        olts = []
        with open(self.__dir, "r") as arquivo:
            for linha in arquivo:
                linha = linha.split(";")
                linha[-1] = linha[-1].replace("\n","")
                olts_split.append(linha)

        if len(olts_split) <= 0:
           return []
        
        for olt_split in olts_split:
            olt = Olt(*olt_split)
            olts.append(olt)
        return olts