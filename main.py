import argparse
import asyncio
from core import Tools

def create_cli():
    parser = argparse.ArgumentParser(description="CLI para filtrar ONUs via telnet")
    parser.add_argument("-H", "--host", required=True, help="IP da OLT")
    parser.add_argument("-u", "--user", required=True, help="Usuário de login")
    parser.add_argument("-p", "--password", required=True, help="Senha de login")
    parser.add_argument("-cp", "--chassi_placa", required=True, help="Chassis e placa da ONU")
    parser.add_argument("-op", "--ont_port", required=True, help="Porta da da placa ONU")
    parser.add_argument("-s", "--status", required=True, help="status da ONU")
    return parser.parse_args()

def init_cli():
    cli = create_cli()
    tools = Tools
    saida = asyncio.run(tools.acessar_ont(host=cli.host, 
                                          username=cli.user, 
                                          password=cli.password, 
                                          chassi_placa=cli.chassi_placa.encode(), 
                                          porta=cli.ont_port))
    onus_output = tools.filtrar_onus(saida, cli.status)
    onus = tools.map_onus(onus_output)
    
    for onu in onus:
        print(f"{onu.chassi} {onu.placa_porta,} {onu.mac}, {onu.status_online}")   
    


if __name__ == "__main__":
    init_cli()
