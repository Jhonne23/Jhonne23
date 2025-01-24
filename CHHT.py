from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, Text, END, filedialog, simpledialog
import threading
from tkinter import ttk
from bs4 import BeautifulSoup
import time
import os
import pandas as pd

try:
    from fpdf import FPDF
    fpdf_available = True
except ImportError:
    fpdf_available = False

def scrape_data():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Erro", "Por favor, insira uma URL.")
        return
    data_type = data_type_var.get()
    if not data_type:
        messagebox.showerror("Erro", "Por favor, selecione o tipo de dado para raspar.")
        return
    try:
        wait_time = int(wait_time_entry.get())
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um tempo de espera válido.")
        return
    progress_bar.start()
    scrape_button.config(state='disabled')
    def run_scrape():
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')  # Roda o chrome no modomj headless 
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.get(url)
            time.sleep(wait_time)  # Espera o tempo especificado para garantir que a página carregue completamente
            html = driver.page_source
            driver.quit()

            soup = BeautifulSoup(html, 'html.parser')
            if data_type == "Títulos":
                elements = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            elif data_type == "Subtítulos":
                elements = soup.find_all(['h2', 'h3', 'h4', 'h5', 'h6'])
            elif data_type == "Textos":
                elements = soup.find_all('p')

            result_text.delete(1.0, END)
            scraped_data = []
            for element in elements:
                text = element.get_text().strip()
                result_text.insert(END, text + "\n")
                scraped_data.append(text)

            save_option = messagebox.askyesno("Salvar Dados", "Deseja salvar os dados raspados?")
            if save_option:
                root.withdraw()  # Esconde a janela principal para evitar conflitos
                show_save_options(scraped_data)
                root.deiconify()  # Mostra a janela principal novamente
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao raspar os dados: {e}")
        finally:
            progress_bar.stop()
            scrape_button.config(state='normal')

    threading.Thread(target=run_scrape).start()

def show_save_options(data):
    save_window = Tk()
    save_window.title("Salvar Dados")

    def save_as_txt():
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            save_data(data, 'txt', file_path)
            messagebox.showinfo("Sucesso", f"Dados salvos com sucesso em {file_path}")
        save_window.destroy()

    def save_as_pdf():
        if not fpdf_available:
            messagebox.showerror("Erro", "FPDF não está disponível.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            save_data(data, 'pdf', file_path)
            messagebox.showinfo("Sucesso", f"Dados salvos com sucesso em {file_path}")
        save_window.destroy()

    def save_as_xlsx():
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            save_data(data, 'xlsx', file_path)
            messagebox.showinfo("Sucesso", f"Dados salvos com sucesso em {file_path}")
        save_window.destroy()

    Button(save_window, text="Salvar como TXT", command=save_as_txt).pack(pady=5)
    Button(save_window, text="Salvar como PDF", command=save_as_pdf).pack(pady=5)
    Button(save_window, text="Salvar como XLSX", command=save_as_xlsx).pack(pady=5)

    save_window.mainloop()

def save_data(data, file_format, file_path):
    if file_format == 'txt':
        with open(file_path, 'w') as f:
            for item in data:
                f.write("%s\n" % item)
    elif file_format == 'pdf':
        if not fpdf_available:
            messagebox.showerror("Erro", "FPDF não está disponível.")
            return
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for item in data:
            pdf.cell(200, 10, txt=item, ln=True)
        pdf.output(file_path)
    elif file_format == 'xlsx':
        df = pd.DataFrame(data, columns=["Dados Raspados"])
        df.to_excel(file_path, index=False)

def clear_results():
    result_text.delete(1.0, END)

root = Tk()
root.title("Web Scraper")

Label(root, text="URL:").grid(row=0, column=0, padx=10, pady=10)
url_entry = Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

Label(root, text="Tipo de Dado:").grid(row=1, column=0, padx=10, pady=10)
data_type_var = StringVar()
data_type_combobox = ttk.Combobox(root, textvariable=data_type_var)
data_type_combobox['values'] = ("Títulos", "Subtítulos", "Textos")
data_type_combobox.grid(row=1, column=1, padx=10, pady=10)

Label(root, text="Tempo de Espera (s):").grid(row=2, column=0, padx=10, pady=10)
wait_time_entry = Entry(root, width=10)
wait_time_entry.grid(row=2, column=1, padx=10, pady=10)

scrape_button = Button(root, text="Raspar Dados", command=scrape_data)
scrape_button.grid(row=3, column=0, columnspan=2, pady=10)

clear_button = Button(root, text="Limpar Resultados", command=clear_results)
clear_button.grid(row=4, column=0, columnspan=2, pady=10)

progress_bar = ttk.Progressbar(root, mode='indeterminate')
progress_bar.grid(row=5, column=0, columnspan=2, pady=10)

result_text = Text(root, height=15, width=80)
result_text.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
