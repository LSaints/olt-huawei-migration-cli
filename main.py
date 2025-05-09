import asyncio
import os

from datetime import datetime
from core import ClientTelnet, Olt


data_execucao = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def salvar_txt(ont) -> None:
    with open(f"logs/onts_{data_execucao}.txt", "a", encoding="utf-8") as file:
        linha = f'{ont.gpon};{ont.id};{ont.mac};{ont.status};{ont.descricao}'
        file.write(linha + "\n")

def realizar_escolha() -> str:
    print('='*100)
    print('\n[1] - Migrar\n')
    print('\n[0] - Sair\n')
    print('='*100)
    opcao = input(str('\n>: '))
    return opcao

async def migrar_olt(onts: list, olt: Olt) -> None:
    gpon_destino = input(str('\nDigite a gpon de destino: '))
    vlan_destino = input(str('\nDigite a vlan de destino: '))

    print("="*100)
    print("\nREMOVENDO ONTS\n")
    print("="*100)
    for ont in onts:
        await olt.desprovisionar_ont(ont)
  
    print("="*100)
    print("\nADICIONANDO ONTS\n")
    print("="*100)
    for ont in onts:
        await olt.provisionar_ont(ont=ont, 
                                  gpon_destino=gpon_destino, 
                                  vlan=vlan_destino)

async def main():
    cliente = ClientTelnet(
        host='10.55.160.2',
        usuario="smartolt",
        senha="rJXf2JA1p4NjTui"
    )
    
    print('='*100)
    gpon_origem = input('Digite a gpon de origem > ')
    print(gpon_origem)
    print('='*100)

    olt = Olt(cliente=cliente)
    onts = await olt.listar_onts(status="offline", gpon=gpon_origem)
    
    print("="*100)
    print("\nLISTANDO ONTS\n")
    print("="*100)
    with open(f"logs/onts_{data_execucao}.txt", "a") as file:
        file.writelines("="*100 + "\n")
       
    for ont in onts:
        salvar_txt(ont)
        print(f'{ont.gpon} {ont.id} {ont.mac} {ont.status} {ont.descricao}')
    
    opcao = realizar_escolha()

    if opcao == '1':
        await migrar_olt(onts=onts, olt=olt)

    if opcao == '0':
        os._exit(1)
  
if __name__ == "__main__":
    asyncio.run(main())
