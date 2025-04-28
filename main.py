import argparse
import asyncio

from core import Tools
from core.onu import Onu

def create_cli():
    parser = argparse.ArgumentParser(description="CLI para filtrar ONUs via telnet")
    parser.add_argument("-H", 
                        "--host", 
                        required=True, 
                        help="IP da OLT")
    
    parser.add_argument("-u", 
                        "--user", 
                        required=True, 
                        help="Usuário de login")
    
    parser.add_argument("-p", 
                        "--password", 
                        required=True, 
                        help="Senha de login")
    
    parser.add_argument("-cp", 
                        "--chassi_placa", 
                        required=True, 
                        help="Chassis e placa da ONU")
    
    parser.add_argument("-op", 
                        "--ont_port", 
                        required=True, 
                        help="Porta da da placa ONU")
    
    parser.add_argument("-s", 
                        "--status", 
                        required=True, 
                        help="status da ONU")
    
    parser.add_argument("-r", 
                        "--remove", 
                        required=False, 
                        help="Remover uma lista de ONUs",  
                        action=argparse.BooleanOptionalAction,
                        default=False)
    
    parser.add_argument("-P", 
                        "--provision", 
                        required=False, 
                        help="Provisionar uma lista de ONUs",  
                        action=argparse.BooleanOptionalAction,
                        default=False)
    
    parser.add_argument("-v", 
                        "--vlan", 
                        required=False, 
                        help="Vlan para provisionar",  
                        default=False)
    parser.add_argument("-tcb", 
                        "--to-chassi-board",
                        required=False,
                        help="Chassi e placa destino",
                        default=False)
    
    parser.add_argument("-tp", 
                        "--to-port",
                        required=False,
                        help="porta destino",
                        default=False)
    
    return parser.parse_args()


def print_header(total, status):
    print("="*50)
    print(f"Total de {total} ONUs {status}")
    print("="*50)


def get_onus(cli, tools: Tools):
    saida = asyncio.run(tools.acessar_ont(host=cli.host, 
                                          username=cli.user, 
                                          password=cli.password, 
                                          chassi_placa=cli.chassi_placa.encode(), 
                                          porta=cli.ont_port))
        
    onus_output = tools.filtrar_onus(saida, cli.status)
    onus: list[Onu] = tools.map_onus(onus_output)
    onus = [onu for onu in onus if "In" not in onu.chassi]
        
    return onus


def init_cli():
    cli = create_cli()
    tools = Tools()

    tools.show_logo()
    if not cli.provision and not cli.remove:
        onus = get_onus(cli=cli, tools=tools)

        print("="*50)
        for onu in onus:
            print(f"{onu.chassi} {onu.placa_porta} {onu.mac} {onu.status_online}")
        print_header(len(onus), cli.status)
    
    if cli.remove:
        with open("onts.txt", "r") as file:
            content = file.read()
            
        with open("onts_desprovisionadas.txt", "w") as des:
            des.write(content)
        
        onus = get_onus(tools=tools, cli=cli)
        asyncio.run(tools.deletar_onu(host=cli.host, 
                                      username=cli.user, 
                                      password=cli.password, 
                                      chassi_placa=cli.chassi_placa.encode(), 
                                      porta=cli.ont_port,
                                      onus=onus))
                
                
    if cli.provision:                
        onus = tools.filtrar_ont_txt(cli.status)
        onus = tools.map_onus(onus)
        asyncio.run(tools.provisionar_onus(host=cli.host, 
                                           username=cli.user, 
                                           password=cli.password, 
                                           chassi_placa=cli.chassi_placa.encode(), 
                                           porta=cli.ont_port,
                                           vlan=cli.vlan,
                                           onus=onus,
                                           to_chassi_board=cli.to_chassi_board.encode(),
                                           to_port=cli.to_port))
        
if __name__ == "__main__":
    init_cli()
