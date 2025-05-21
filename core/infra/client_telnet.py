import asyncio
import telnetlib3

class ClientTelnet:
    def __init__(self, host, porta=23, usuario=None, senha=None, prompt=">", timeout=10):
        self.host = host
        self.porta = porta
        self.usuario = usuario
        self.senha = senha
        self.timeout = timeout
        self.reader = None
        self.writer = None
        self.prompt = prompt
        
    async def conectar(self):
        print("conectando...")
        self.reader, self.writer = await telnetlib3.open_connection(
            self.host, port=self.porta, encoding='utf-8'
        )
        
        if self.usuario:
            await self.reader.readuntil(b"name:")
            self.writer.write(self.usuario + '\n')

        if self.senha:
            await self.reader.readuntil(b"password:")
            self.writer.write(self.senha + '\n')

    async def executar(self, comando, esperado):
        self.writer.write(comando + '\r\n')
        await asyncio.sleep(1)
        try:
            resultado = await self.reader.readuntil(esperado.encode())
            if isinstance(resultado, bytes):
                resultado = resultado.decode('utf-8')
            
        except asyncio.IncompleteReadError as e:
            print("[WARN] Leitura incompleta. Usando dados parciais.")
            resultado = e.partial.decode('utf-8', errors='ignore')
        except asyncio.TimeoutError:
            print("[ERRO] Timeout ao esperar resposta.")
            resultado = ''
        except Exception as e:
            print(f"[ERRO inesperado] {e}")
            resultado = ''
        return resultado.strip()
    
    
    async def desconectar(self):
        self.writer.write('exit\n')
        self.writer.close()    