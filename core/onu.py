import telnetlib3
import asyncio

class Onu:
    def __init__(self, chassi, placa_porta, ont_id, mac, status, status_online):
       self.chassi = chassi
       self.placa_porta = placa_porta
       self.ont_id = ont_id
       self.mac = mac
       self.status = status
       self.status_online = status_online
    
    