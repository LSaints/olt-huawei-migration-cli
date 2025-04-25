import asyncio
import telnetlib3

from .onu import Onu

class Tools:
    async def acessar_ont(host, username, password, chassi_placa, porta):
        reader, writer = await telnetlib3.open_connection(
            host=host, port=23, encoding='utf-8'
        )

        try:       
            await reader.readuntil(b"name:")
            writer.write(f"{username}\n")
            print("name")

            await reader.readuntil(b"password:")
            writer.write(f"{password}\n")
            print("password")

            writer.write("enable\n")
            await reader.readuntil(b'#')
            print("anable")

            writer.write("config\n")
            await reader.readuntil(b'(config)#')
            print("config")

            writer.write("mmi-mode enable\n")
            await reader.readuntil(b'(config)#')
            print("mmi-mode")

            writer.write(f"interface gpon {chassi_placa.decode('utf-8')}\n")
            await reader.readuntil(b'(config-if-gpon-' + chassi_placa + b')#')
            print("interface gpon")

            writer.write(f"display ont info {porta} all\n")
            print("display ont")
            saida = await reader.readuntil(b'(config-if-gpon-' + chassi_placa + b')#')

            saida_limpa = saida.rsplit(b'\n', 1)

            saida_limpa = saida_limpa[0].decode('utf-8').replace("\r\n", "\n")
            return saida_limpa


        except asyncio.TimeoutError:
            print("Nenhuma mensagem recebida antes do login (timeout).")
        except Exception as e:
            print(f"erro inesperado:{e}")
    
    
    def filtrar_onus(output_ont, status):
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
    

    def map_onus(onus_output):
        onus_array:list[Onu] = []
        for onu_obj in onus_output:
            onu = Onu(onu_obj[0], 
                    onu_obj[1],
                    onu_obj[2],
                    onu_obj[3],
                    onu_obj[4],
                    onu_obj[5])
            onus_array.append(onu)
        return onus_array