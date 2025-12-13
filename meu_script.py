import pyautogui, keyboard, time

pyautogui.FAILSAFE = True
pyautogui.alert(text='A automação irá iniciar em 3 segundos após o OK.', title='ATENÇÃO!!!!', button='OK')
time.sleep(3) # dá tempo de você mudar de janela

quantidade = int(input("Digite a quantidade de vezes que deseja executar a automação: "))

for i in range(quantidade):
    print(f"Execução {i+1}/{quantidade}")

    try:
        # tenta localizar o botão "Uncheck"
        local = pyautogui.locateOnScreen('uncheck.png', confidence=0.8)

        if local:
            # pega o centro do botão
            x, y = pyautogui.center(local)
            time.sleep(1)
            pyautogui.click(x, y)
            time.sleep(1)
            # enter
            pyautogui.press('enter')
            time.sleep(1)
            # seta para baixo
            pyautogui.press('down')
            #print("Uncheck encontrado → clique + enter + down")

        else:
            # não encontrou → apenas seta para baixo
            time.sleep(1)
            pyautogui.press('down')
            # print("Uncheck NÃO encontrado → apenas down")

    except Exception as e:
        # Se ocorrer qualquer erro inesperado
        print("Erro detectado, ignorando e continuando:", e)
        time.sleep(1)
        pyautogui.press('down')

    time.sleep(0.5)


#pyautogui.moveTo(100, 100)
# keyboard.wait("enter")
#pyautogui.write('Maria Eduarda, eu te amo!s2S2s2S2s2', interval=0.5)

# while True:
#     if keyboard.is_pressed("ESC"):
#         print("Parando automação...")
#         break
#     pyautogui.press("enter")



# pyautogui.write(' mundo!', interval=0.3)