from datetime import datetime
import os
from typing import List

from core.domain.ont import Ont

class Logger:
    def __init__(self) -> None:
        self.__verificar_log_dir()
    
    def gerar_log_onts(self, onts: List[Ont]):
        self.__verificar_log_dir()
        data_log = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        for ont in onts:
            with open(f"logs/onts_{data_log}.log", "a", encoding="utf-8") as file:    
                linha = f"{ont.gpon};{ont.id};{ont.mac};{ont.status};{ont.descricao}"
                file.write(linha)
    
    
    def __verificar_log_dir(self):
        path = "."
        dir_list = os.listdir(path=path)
        if "logs" not in dir_list:
            os.mkdir("logs")
        pass