import pyautogui
import pyperclip
import csv
import time
import keyboard

# =====================================================
# CONFIGURAÇÕES
# =====================================================

LINHAS_FASE1 = int(input("Adicione qual sera o numero de linhas na primeira pagina: "))       # linhas que mudam a coordenada
TOTAL_LINHAS = int(input("Adicione qual sera o numero de linhas totais: "))       # total a capturar
time.sleep(2)
# Coordenadas da PRIMEIRA LINHA (máquina-alvo!)
ID_BASE = (380, 247)
NOME_BASE = (516, 247)

# Deslocamento vertical entre uma linha e outra
OFFSET_Y = 21

# Coordenadas fixas após a linha 20
ID_FIXO = (380, 247 + OFFSET_Y * (LINHAS_FASE1 - 1))
NOME_FIXO = (516, 247 + OFFSET_Y * (LINHAS_FASE1 - 1))

TEMPO_CLIQUE = 0.5
TEMPO_COPY = 1.2


# =====================================================
# Copiar texto do campo atual
# =====================================================

def copiar():
    pyautogui.hotkey("ctrl", "a")
    time.sleep(TEMPO_COPY)

    pyautogui.hotkey("ctrl", "c")
    time.sleep(TEMPO_COPY)

    return pyperclip.paste().strip()


# =====================================================
# PROGRAMA PRINCIPAL
# =====================================================

print("COMEÇANDO EM 5 SEGUNDOS...")
time.sleep(5)

resultado = []

for i in range(1, TOTAL_LINHAS + 1):
    print(f"Capturando linha {i}/{TOTAL_LINHAS}")

    # --------------------------
    # FASE 1: linhas 1 a 20
    # --------------------------
    if i <= LINHAS_FASE1:

        y_offset = OFFSET_Y * (i - 1)

        # Coordenadas da linha atual
        id_coord = (ID_BASE[0], ID_BASE[1] + y_offset)
        nome_coord = (NOME_BASE[0], NOME_BASE[1] + y_offset)

    # --------------------------
    # FASE 2: linha 21 em diante
    # --------------------------
    else:
        # desce a grade 1 linha com seta para baixo
        pyautogui.press("down")
        time.sleep(1)

        id_coord = ID_FIXO
        nome_coord = NOME_FIXO

    # ---- Capturar ID ----
    pyautogui.click(id_coord)
    time.sleep(TEMPO_CLIQUE)
    id_valor = copiar()

    # ---- Capturar Nome ----
    pyautogui.click(nome_coord)
    time.sleep(TEMPO_CLIQUE)
    nome_valor = copiar()

    print(f"> ID = {id_valor} | Nome = {nome_valor}")
    resultado.append([id_valor, nome_valor])


# =====================================================
# SALVAR CSV
# =====================================================

with open("resultado.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["ID", "Nome"])
    w.writerows(resultado)

print("\nFINALIZADO! Arquivo criado: resultado.csv")
