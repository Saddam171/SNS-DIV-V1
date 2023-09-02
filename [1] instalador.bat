@echo off
color A
title Lofy UserDiv V3
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo                   ----------------------------------------------------
echo                     Bem vindo ao instalador do Lofy UserDiv V3        
echo                     Voce esta prestes a instalar todos os requisitos  
echo                     Em caso de duvida entre no grupo do discord 
echo                   ----------------------------------------------------
echo.
echo.
echo.
echo.
echo.
echo.
echo.
pause nul
cls
color B
cls
title Instalando....
call python -m pip install --upgrade pip
call pip uninstall -y psutil && pip uninstall -y colorama && pip uninstall -y tasksio && pip uninstall -y discum && pip uninstall -y aiohttp && pip uninstall -y discordsetup
call pip install psutil && pip install colorama && pip install tasksio && pip install discum && pip install aiohttp && pip install discordsetup
cls
title Lofy UserDiv V3
color C
echo.
echo.
echo.
echo.
echo                   ----------------------------------------------------
echo                       Prontinho agora voce pode fechar o arquivo.
echo                   ----------------------------------------------------
echo.
echo.
echo.
echo.
echo.
echo.
echo.
pause nul
exit