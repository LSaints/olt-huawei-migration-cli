@echo off
setlocal

:: Caminho onde vamos instalar o exe
set CLI_DIR=C:\oltcli
set EXE_NAME=oltcli.exe

echo Instalando OLT CLI...

:: Cria a pasta, se necessário
if not exist "%CLI_DIR%" (
    mkdir "%CLI_DIR%"
)

:: Copia o exe para o destino
copy /Y "%EXE_NAME%" "%CLI_DIR%\"

:: Adiciona o diretório ao PATH do usuário (caso ainda não esteja)
powershell -Command ^
    $cliPath = '%CLI_DIR%'; ^
    $currentPath = [Environment]::GetEnvironmentVariable('Path', 'User'); ^
    if ($currentPath -notmatch [regex]::Escape($cliPath)) { ^
        [Environment]::SetEnvironmentVariable('Path', $currentPath + ';' + $cliPath, 'User') ^
    }

echo.
echo ========================================
echo OLT CLI instalado com sucesso!
echo Execute 'oltcli' no terminal de qualquer lugar.
echo Feche e abra o terminal se for necessário.
echo ========================================
pause
