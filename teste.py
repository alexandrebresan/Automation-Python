import pyautogui, pyperclip, csv, time, os, sys, logging, threading, tkinter as tk
from tkinter import messagebox

# =====================================================
# BASE DIRECTORY (funciona em .py e .exe)
# =====================================================
BASE_DIR = os.path.dirname(
    sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
)

LOG_DIR = os.path.join(BASE_DIR, "logs")
CSV_DIR = os.path.join(BASE_DIR, "csv")

LOG_PATH = os.path.join(LOG_DIR, "execucao.log")
CSV_PATH = os.path.join(CSV_DIR, "resultado.csv")

# =====================================================
# LOG
# =====================================================
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

# =====================================================
# CONFIGURAÇÕES FIXAS
# =====================================================
ID_BASE = (300, 205)
NOME_BASE = (380, 205)
OFFSET_Y = 21

TEMPO_CLIQUE = 0.5
TEMPO_COPY = 1.2

pyautogui.FAILSAFE = True

# =====================================================
# FUNÇÕES
# =====================================================
def copiar():
    pyautogui.hotkey("ctrl", "a")
    time.sleep(TEMPO_COPY)
    pyautogui.hotkey("ctrl", "c")
    time.sleep(TEMPO_COPY)
    return pyperclip.paste().strip()


def executar(linhas_fase1, total_linhas, status_label):
    try:
        logging.info("===== INÍCIO DA EXECUÇÃO =====")
        status_label.config(text="Iniciando em 5 segundos...")
        time.sleep(5)

        resultado = []

        ID_FIXO = (ID_BASE[0], ID_BASE[1] + OFFSET_Y * (linhas_fase1 - 1))
        NOME_FIXO = (NOME_BASE[0], NOME_BASE[1] + OFFSET_Y * (linhas_fase1 - 1))

        for i in range(1, total_linhas + 1):
            status_label.config(text=f"Capturando linha {i}/{total_linhas}")
            logging.info("Capturando linha %d", i)

            if i <= linhas_fase1:
                y_offset = OFFSET_Y * (i - 1)
                id_coord = (ID_BASE[0], ID_BASE[1] + y_offset)
                nome_coord = (NOME_BASE[0], NOME_BASE[1] + y_offset)
            else:
                pyautogui.press("down")
                time.sleep(2)
                id_coord = ID_FIXO
                nome_coord = NOME_FIXO

            pyautogui.click(id_coord)
            time.sleep(TEMPO_CLIQUE)
            id_valor = copiar()

            pyautogui.click(nome_coord)
            time.sleep(TEMPO_CLIQUE)
            nome_valor = copiar()

            resultado.append([id_valor, nome_valor])
            logging.info("ID: %s | Nome: %s", id_valor, nome_valor)

        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["ID", "Nome"])
            w.writerows(resultado)

        logging.info("CSV salvo com sucesso")
        status_label.config(text="Finalizado com sucesso!")
        messagebox.showinfo("Concluído", "Processo finalizado com sucesso!")

    except Exception as e:
        logging.error("Erro", exc_info=True)
        messagebox.showerror("Erro", "Ocorreu um erro. Verifique o log.")


def iniciar():
    try:
        linhas = int(entry_linhas.get())
        total = int(entry_total.get())
    except ValueError:
        messagebox.showerror("Erro", "Digite apenas números.")
        return

    thread = threading.Thread(
        target=executar,
        args=(linhas, total, status_label),
        daemon=True
    )
    thread.start()

# =====================================================
# INTERFACE GRÁFICA
# =====================================================
root = tk.Tk()
root.title("Automação de Captura")
root.geometry("350x220")
root.resizable(False, False)

tk.Label(root, text="Linhas da primeira página:").pack(pady=5)
entry_linhas = tk.Entry(root)
entry_linhas.pack()

tk.Label(root, text="Total de linhas:").pack(pady=5)
entry_total = tk.Entry(root)
entry_total.pack()

tk.Button(root, text="Iniciar", command=iniciar, height=2, width=20).pack(pady=15)

status_label = tk.Label(root, text="Aguardando...")
status_label.pack()

root.mainloop()
