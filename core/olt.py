from core.client_telnet import ClientTelnet

class Olt:
    def __init__(self, cliente: ClientTelnet):
        self.__cliente = cliente
        
    async def listar_onts(self, status: str, gpon: str):
        ont_lista = []
        gpon = gpon.split("/")
        
        await self.__cliente.conectar()
        await self.__entrar_modo_configuração()

        interface_gpon = f"interface gpon {gpon[0]}/{gpon[1]}"
        interface_gpon_saida = await self.__cliente.executar(interface_gpon, 
                                                           f"(config-if-gpon-{gpon[0]}/{gpon[1]})#")

        display_ont = f"display ont info {gpon[2]} all"
        display_ont_saida = await self.__cliente.executar(display_ont, 
                                                        f"(config-if-gpon-{gpon[0]}/{gpon[1]})#")
        
        #self.__mostrar_saida(display_ont, display_ont_saida)

        display_ont_saida = display_ont_saida.split("\n")
        
        descricoes = self.__extrair_ont_descricoes(display_ont_saida)
        for l in display_ont_saida:
            l = l.split(" ")
            l = [item.strip() for item in l if item.strip()]
            if status in l:
                if int(gpon[1]) < 10:
                    l[0] = l[0] + l[1]
                    del l[1]
                for desc in descricoes:
                    if (desc[1] == l[1]):
                        l.append(desc[-1])
                        ont_lista.append(l)
        return ont_lista
    
    async def desprovisionar_ont(self, ont):
        gpon = ont[0].split("/")
        
        await self.__cliente.conectar()
        await self.__entrar_modo_configuração()
        
        undo_service = f"undo service-port port {gpon[0]}/{gpon[1]}/{gpon[2]} ont {ont[1]}\n\r\n"
        await self.__cliente.executar(undo_service, "(config)#")
        print(undo_service)
        
        interface_gpon = f"interface gpon {gpon[0]}/{gpon[1]}\n"
        await self.__cliente.executar(interface_gpon, "(config)#")
        print(interface_gpon)
        
        ont_delete = f"ont delete {gpon[2]} {ont[1]}\n"
        await self.__cliente.executar(ont_delete, "(config)#")
        print(ont_delete)
        
        quit = "quit\n"
        await self.__cliente.executar(quit, "#")
        print("quit\n")
        
        print('='*50)
        
        await self.__cliente.desconectar()
    
    async def provisionar_ont(self, ont, gpon_destino, vlan):
        
        await self.__cliente.conectar()
        await self.__entrar_modo_configuração()
        
        gpon_destino = gpon_destino.split("/")
        
        interface_gpon = f"interface gpon {gpon_destino[0]}/{gpon_destino[1]}\r\n"
        print(interface_gpon)
        saida_interface_gpon = await self.__cliente.executar(interface_gpon, 
                               f"(config-if-gpon-{gpon_destino[0]}/{gpon_destino[1]})#")
        self.__mostrar_saida(interface_gpon, saida_interface_gpon)
        
        if "\r" in ont[-1]:
            ont[-1] = ont[-1].replace("\r", "")
        
        ont_add = f"ont add {gpon_destino[2]} {ont[1]} sn-auth {ont[2]} omci ont-lineprofile-id 900 ont-srvprofile-id 900 desc {ont[-1]}\r\n"
        saida_ont_add = await self.__cliente.executar(ont_add, f"#")
        self.__mostrar_saida(ont_add, saida_ont_add)
        print(ont_add)
        
        ont_port = f"ont port native-vlan {gpon_destino[2]} {ont[1]} eth 1 vlan 900 priority 0\r\n"
        saida_ont_port = await self.__cliente.executar(ont_port, "#")
        self.__mostrar_saida(ont_port, saida_ont_port)
        print(ont_port)
        
        quit = f"quit\r\n"
        await self.__cliente.executar(quit, "(config)#")
        print(quit)
        
        service_port = f"service-port vlan {vlan} gpon {gpon_destino[0]}/{gpon_destino[1]}/{gpon_destino[2]} ont {ont[1]} gemport 900 multi-service user-vlan 900 tag-transform translate\r\n"
        await self.__cliente.executar("\n\r", "#")
        saida_service_port = await self.__cliente.executar(service_port, "(config)#")
        self.__mostrar_saida(service_port, saida_service_port)
        print(service_port)
        print("="*50)
        
        await self.__cliente.desconectar()
    
    async def __entrar_modo_configuração(self):
        enable = "enable"
        await self.__cliente.executar(enable, ">")

        config = "config"
        await self.__cliente.executar(config, "(config)#")

        mmi_mode = "mmi-mode enable"
        await self.__cliente.executar(mmi_mode, "(config)#")
    
    def __extrair_ont_descricoes(self, texto):
        linhas = []
        for linha in texto:
            if "offline" not in linha and "online" not in linha:
                linha = linha.split(" ")
                linha = [item for item in linha if item != ""]
                linhas.append(linha)
                #print(f"{linha} - {len(linha)}")
        linhas = [linha for linha in linhas if len(linha) >= 3 and "ONT-ID" not in linha]
        descricoes = []
        for linha in linhas:
            if len(linha) > 3:
                linha[0] = linha[0] + linha[1]
                del linha[1]
                descricoes.append(linha)
            else:
                descricoes.append(linha)
        
        return descricoes
               
    def __mostrar_saida(self, comando, saida):
        print(f'\n>> {comando}\n{saida}')
    
    