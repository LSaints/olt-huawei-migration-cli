import asyncio
from time import sleep
import telnetlib3
import os
import platform

from colorama import Fore, Style, init
from .onu import Onu

class Tools:
    
    def __init__(self):
        pass
    
    
    async def acessar_ont(self, host, username, password, chassi_placa, porta):
        reader, writer = await telnetlib3.open_connection(
            host=host, port=23, encoding='utf-8'
        )

        try:       
            await reader.readuntil(b"name:")
            writer.write(f"{username}\n")

            await reader.readuntil(b"password:")
            writer.write(f"{password}\n")

            writer.write("enable\n")
            await reader.readuntil(b'#')

            writer.write("config\n")
            await reader.readuntil(b'(config)#')

            writer.write("mmi-mode enable\n")
            await reader.readuntil(b'(config)#')

            writer.write(f"interface gpon {chassi_placa.decode('utf-8')}\n")
            await reader.readuntil(b'(config-if-gpon-' + chassi_placa + b')#')

            writer.write(f"display ont info {porta} all\n")
            saida = await reader.readuntil(b'(config-if-gpon-' + chassi_placa + b')#')

            saida_limpa = saida.rsplit(b'\n', 1)

            saida_limpa = saida_limpa[0].decode('utf-8').replace("\r\n", "\n")
            return saida_limpa


        except asyncio.TimeoutError:
            print("Nenhuma mensagem recebida antes do login (timeout).")
        except Exception as e:
            print(f"erro inesperado:{e}")  
 
    
    def filtrar_onus(self, output_ont, status):
        onus = []
        with open("onts.txt", "w") as file:
            file.write(output_ont)

        with open("onts.txt", "r") as file:
            for l in file:
                if status in l:
                    l = l.split(" ")
                    for index, c in enumerate(l):
                        if c == "" or c == "\n":
                           l.pop(index)

                    for index, c in enumerate(l):
                        if c == "" or c == "\n":
                           l.pop(index)

                    for index, c in enumerate(l):
                        if c == "" or c == "\n":
                           l.pop(index)
                    onus.append(l)
        
        return onus
    
    def filtrar_ont_txt(self, status):
        onus = []
        with open("onts_desprovisionadas.txt", "r") as file:
            for l in file:
                if status in l:
                    l = l.split(" ")
                    for index, c in enumerate(l):
                        if c == "" or c == "\n":
                           l.pop(index)

                    for index, c in enumerate(l):
                        if c == "" or c == "\n":
                           l.pop(index)

                    for index, c in enumerate(l):
                        if c == "" or c == "\n":
                           l.pop(index)
                    onus.append(l)
        return onus

    def map_onus(self, onus_output):
        onus_array: list[Onu] = []
        for onu_obj in onus_output:
            if onu_obj[0].__len__() > 2:
                chassi_obj = self.formatar_chassi(onu_obj[0]).split(" ")
                onu = Onu(chassi_obj[0], 
                          chassi_obj[1],
                          onu_obj[1],
                          onu_obj[2],
                          onu_obj[3],
                          onu_obj[4])
                onus_array.append(onu)
            else:
                onu = Onu(onu_obj[0], 
                          onu_obj[1],
                          onu_obj[2],
                          onu_obj[3],
                          onu_obj[4],
                          onu_obj[5])
                onus_array.append(onu)
            
        return onus_array
    
    
    def formatar_chassi(self, chassi: str):
            chassi = chassi[:2] + " " + chassi[2:]
            return chassi
    
    
    def formatar_gpon(self, gpon: str):
        if len(gpon) > 4:
            return gpon[:2]
        else:
            return gpon[:-2]
 
    
    async def deletar_onu(self, 
                          host, 
                          username, 
                          password, 
                          chassi_placa, 
                          porta, 
                          onus: list[Onu]):
        reader, writer = await telnetlib3.open_connection(
            host=host, port=23, encoding='utf-8'
        )
        
        try:
            print("="*50)
            print(f"remover {len(onus)} ONUs")
            print("="*50)
            await reader.readuntil(b"name:")
            writer.write(f"{username}\n")

            await reader.readuntil(b"password:")
            writer.write(f"{password}\n")

            writer.write("enable\n")
            await reader.readuntil(b'#')
            
            #config
            writer.write("config\n")
            await reader.readuntil(b'(config)#')

            writer.write("mmi-mode enable\n")
            await reader.readuntil(b'(config)#')
            
                
            for index, onu in enumerate(onus):
                #print(f"{onu.chassi}, {onu.placa_porta}, {onu.ont_id}, {onu.mac}")
                sleep(2)
                print("\n")
                
                #undo service-port port 0/2/2 ont 0
                undo_service_command = f"undo service-port port {chassi_placa.decode("utf-8")}/{porta} ont {onu.ont_id}\n" 
                writer.write(undo_service_command)
                writer.write("\n")
                writer.write("y\n")
                print(undo_service_command)
                
                ##interface gpon 0/2
                interface_gpon_command = f"interface gpon {chassi_placa.decode("utf-8")}\n"
                #f"(config-if-gpon-{onu.chassi}{onu.placa_porta[:-3]})#".encode()
                await reader.readuntil()
                writer.write(interface_gpon_command)
                await reader.readuntil(b'(config)#') 
                print(interface_gpon_command)
                
                ##ont delete 2 0
                #print(f"=> {}")
                ont_delete_command = f"ont delete {onu.placa_porta[3:len(onu.placa_porta)]} {onu.ont_id}\n"
                sleep(1)
                writer.write(ont_delete_command)
                sleep(1)
                #await reader.readuntil(b'(config)#')
                print(ont_delete_command)
                print(f"[{index + 1}] remover => {onu.mac}")
                writer.write("quit\n")
                
        except Exception as e:
            print(f"erro inesperado:{e}")  


    def get_ont_description(self, onu_id: int) -> str:
        result = []
        with open('onts_desprovisionadas.txt', 'rb') as file:
            for l in file:
                if f" {str(onu_id)} ".encode() in l:
                    result.append(l)
        descricao = result[1].decode().split(" ")[-1]
        descricao = descricao
        return descricao


    async def provisionar_onus(self, 
                               host, 
                               username, 
                               password, 
                               chassi_placa, 
                               porta, 
                               vlan,
                               to_chassi_board,
                               to_port,
                               onus: list[Onu]):
        reader, writer = await telnetlib3.open_connection(
            host=host, port=23, encoding='utf-8'
        )
        
        try:
            sleep(2)
            await reader.readuntil(b"name:")
            writer.write(f"{username}\n")

            await reader.readuntil(b"password:")
            writer.write(f"{password}\n")

            writer.write("enable\n")
            await reader.readuntil(b'#')
            writer.write("enable\n")
            await reader.readuntil(b"#")
            print("enable\n")

            writer.write("config\n")
            await reader.readuntil(b"(config)#")
            print("config\n")
            
            writer.write("mmi-mode enable\n")
            await reader.readuntil(b'(config)#')
            
            for onu in onus:
                sleep(2)
                descricao = self.get_ont_description(onu.ont_id)
                
                print(f"provisionando [{onu.ont_id}] => {onu.mac} - {descricao}")
                
                sleep(1)
                command_interface = f"interface gpon {to_chassi_board.decode()}\n"
                writer.write(command_interface) 
                await reader.readuntil(f"(config-if-gpon-{to_chassi_board.decode()})#".encode())
                print(command_interface)

                sleep(1)
                command_ont_add = f"ont add {to_port} sn-auth {onu.mac} omci ont-lineprofile-id 900 ont-srvprofile-id 900 desc {descricao}\n" 
                writer.write(command_ont_add)
                print(command_ont_add)

                sleep(1)
                command_ont_port = f"ont port native-vlan {to_port} {onu.ont_id} eth 1 vlan 900 priority 0\n" 
                writer.write(command_ont_port)
                print(command_ont_port)

                sleep(1)
                command_quit = "quit\n"
                writer.write(command_quit)
                print(command_quit)

                sleep(1)
                command_service_port = f"service-port vlan {vlan} gpon {to_chassi_board.decode('utf-8')}/{to_port} ont {onu.ont_id} gemport 900 multi-service user-vlan 900 tag-transform translate\n"
                writer.write(command_service_port)
                print(command_service_port)
                
                print('='*50)
            writer.write("save\n")
            print("save")
        except Exception as e:
            print(f"erro inesperado:{e}") 
                


    def clear_screen(self):
        # Detecta o sistema e executa o comando apropriado
        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('clear')


    def show_logo(self):
        init(autoreset=True)
        print(Fore.CYAN + Style.BRIGHT + r"""
         ___        ___   ________          ________   ___    _________                           ________   ___        ___     
        |\  \      |\  \ |\   ____\        |\   __  \ |\  \  |\___   ___\                        |\   ____\ |\  \      |\  \    
        \ \  \     \ \  \\ \  \___|        \ \  \|\  \\ \  \ \|___ \  \_|      ____________      \ \  \___| \ \  \     \ \  \   
         \ \  \     \ \  \\ \  \  ___       \ \  \\\  \\ \  \     \ \  \      |\____________\     \ \  \     \ \  \     \ \  \  
          \ \  \____ \ \  \\ \  \|\  \       \ \  \\\  \\ \  \____ \ \  \     \|____________|      \ \  \____ \ \  \____ \ \  \ 
           \ \_______\\ \__\\ \_______\       \ \_______\\ \_______\\ \__\                          \ \_______\\ \_______\\ \__\
            \|_______| \|__| \|_______|        \|_______| \|_______| \|__|                           \|_______| \|_______| \|__|
        
            versão: 0.1.0
        """ + Style.RESET_ALL)
        sleep(1)
        self.clear_screen()