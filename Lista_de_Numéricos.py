import math
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk


def converter_valor(texto):
    """Converte textos como '15000', '15.000,50' ou '15000.50' em número."""
    valor = texto.strip().replace("R$", "").replace(" ", "")
    if not valor:
        raise ValueError("Informe o valor de vendas.")

    if "," in valor:
        # Formato brasileiro: ponto separa milhar e vírgula separa centavos
        valor = valor.replace(".", "").replace(",", ".")
    else:
        partes = valor.split(".")
        # '15.000' ou '1.500.000' são tratados como separadores de milhar
        if len(partes) > 1 and all(len(parte) == 3 for parte in partes[1:]):
            valor = valor.replace(".", "")

    try:
        numero = float(valor)
    except ValueError:
        raise ValueError("Valor inválido. Use, por exemplo, 15000 ou 15.000,50.") from None

    if not math.isfinite(numero):
        raise ValueError("Valor inválido. Use, por exemplo, 15000 ou 15.000,50.")
    if numero < 0:
        raise ValueError("O valor de vendas não pode ser negativo.")
    return numero


def formatar_moeda(valor):
    """Formata um número no padrão brasileiro: R$ 15.000,50"""
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


class LojasVendasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lojas e Vendas")
        self.root.geometry("620x560")
        self.root.minsize(560, 480)

        # Listas iniciais
        # ATENÇÃO -> As duas listas são alteradas sempre na mesma posição,
        # assim cada loja continua ligada ao seu valor de vendas.
        self.lojas = ['Rio de Janeiro', 'São Paulo', 'Curitiba']
        self.vendas = [10000.0, 20000.0, 50000.0]

        # Guarda tudo o que foi inserido ou atualizado durante a execução
        self.historico = []

        # Criar os widgets
        self.create_widgets()

        # Atualizar a tabela
        self.atualizar_tabela()

        # O "X" da janela também pede confirmação antes de fechar
        self.root.protocol("WM_DELETE_WINDOW", self.fechar_programa)

    def create_widgets(self):
        # Frame para digitar loja e valor
        frame_dados = tk.LabelFrame(self.root, text="Dados da Loja", padx=10, pady=10)
        frame_dados.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_dados, text="Loja:").grid(row=0, column=0, sticky="w", pady=3)
        self.entry_loja = tk.Entry(frame_dados, width=40)
        self.entry_loja.grid(row=0, column=1, sticky="we", pady=3)

        tk.Label(frame_dados, text="Valor de vendas (R$):").grid(row=1, column=0, sticky="w", pady=3)
        self.entry_valor = tk.Entry(frame_dados, width=40)
        self.entry_valor.grid(row=1, column=1, sticky="we", pady=3)
        frame_dados.columnconfigure(1, weight=1)

        # Botões para inserir e atualizar
        frame_botoes = tk.Frame(self.root)
        frame_botoes.pack(pady=5)

        btn_inserir = tk.Button(frame_botoes, text="Inserir Loja", width=16, command=self.inserir_loja)
        btn_inserir.pack(side=tk.LEFT, padx=5)

        btn_atualizar = tk.Button(frame_botoes, text="Atualizar Vendas", width=16, command=self.atualizar_vendas)
        btn_atualizar.pack(side=tk.LEFT, padx=5)

        btn_limpar = tk.Button(frame_botoes, text="Limpar Campos", width=16, command=self.limpar_campos)
        btn_limpar.pack(side=tk.LEFT, padx=5)

        # Frame para a tabela de lojas e vendas
        frame_tabela = tk.LabelFrame(self.root, text="Lojas e Vendas", padx=10, pady=10)
        frame_tabela.pack(fill="both", expand=True, padx=10, pady=5)

        self.tabela = ttk.Treeview(frame_tabela, columns=("loja", "vendas"), show="headings", height=10)
        self.tabela.heading("loja", text="Loja")
        self.tabela.heading("vendas", text="Vendas")
        self.tabela.column("loja", width=300, anchor="w")
        self.tabela.column("vendas", width=180, anchor="e")
        self.tabela.pack(fill="both", expand=True, side=tk.LEFT)

        # Scrollbar para a tabela
        scrollbar = tk.Scrollbar(frame_tabela, command=self.tabela.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.tabela.config(yscrollcommand=scrollbar.set)

        # Ao clicar numa loja, os campos são preenchidos para facilitar a atualização
        self.tabela.bind("<<TreeviewSelect>>", self.selecionar_loja)

        # Total de vendas
        self.label_total = tk.Label(self.root, text="", font=("Arial", 11, "bold"))
        self.label_total.pack(pady=5)

        # Botões de relatório e fechar
        frame_rodape = tk.Frame(self.root)
        frame_rodape.pack(pady=10)

        btn_relatorio = tk.Button(frame_rodape, text="Exibir Relatório", width=18, command=self.exibir_relatorio)
        btn_relatorio.pack(side=tk.LEFT, padx=5)

        btn_fechar = tk.Button(frame_rodape, text="Fechar Programa", width=18, command=self.fechar_programa)
        btn_fechar.pack(side=tk.LEFT, padx=5)

    def atualizar_tabela(self):
        # Limpar a tabela
        for linha in self.tabela.get_children():
            self.tabela.delete(linha)

        # Preencher com loja e venda na mesma posição (como a tupla do exemplo original)
        for i, (loja, venda) in enumerate(zip(self.lojas, self.vendas)):
            self.tabela.insert("", tk.END, iid=str(i), values=(loja, formatar_moeda(venda)))

        self.label_total.config(text=f"Total de vendas: {formatar_moeda(sum(self.vendas))}")

    def procurar_loja(self, nome):
        """Retorna a posição da loja na lista (sem diferenciar maiúsculas) ou None."""
        for i, loja in enumerate(self.lojas):
            if loja.casefold() == nome.casefold():
                return i
        return None

    def ler_campos(self):
        """Lê e valida os campos. Retorna (loja, valor) ou None se houver erro."""
        loja = " ".join(self.entry_loja.get().split())
        if not loja:
            messagebox.showwarning("Aviso", "Digite o nome da loja!")
            self.entry_loja.focus_set()
            return None

        try:
            valor = converter_valor(self.entry_valor.get())
        except ValueError as erro:
            messagebox.showwarning("Aviso", str(erro))
            self.entry_valor.focus_set()
            return None

        return loja, valor

    def registrar(self, acao, loja, valor_anterior, valor_novo):
        self.historico.append({
            "hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "acao": acao,
            "loja": loja,
            "anterior": valor_anterior,
            "novo": valor_novo,
        })

    def inserir_loja(self):
        dados = self.ler_campos()
        if dados is None:
            return
        loja, valor = dados

        if self.procurar_loja(loja) is not None:
            messagebox.showwarning(
                "Aviso",
                f"A loja '{loja}' já existe!\nUse o botão 'Atualizar Vendas' para mudar o valor.",
            )
            return

        self.lojas.append(loja)
        self.vendas.append(valor)
        self.registrar("Inserida", loja, None, valor)
        self.atualizar_tabela()
        self.limpar_campos()
        messagebox.showinfo("Sucesso", f"Loja '{loja}' inserida com {formatar_moeda(valor)}.")

    def atualizar_vendas(self):
        dados = self.ler_campos()
        if dados is None:
            return
        loja, valor = dados

        indice = self.procurar_loja(loja)
        if indice is None:
            messagebox.showwarning(
                "Aviso",
                f"A loja '{loja}' não foi encontrada!\nUse o botão 'Inserir Loja' para cadastrá-la.",
            )
            return

        valor_anterior = self.vendas[indice]
        if valor_anterior == valor:
            messagebox.showinfo("Aviso", "O valor informado é igual ao atual. Nada foi alterado.")
            return

        self.vendas[indice] = valor
        self.registrar("Atualizada", self.lojas[indice], valor_anterior, valor)
        self.atualizar_tabela()
        self.limpar_campos()
        messagebox.showinfo(
            "Sucesso",
            f"Vendas de '{self.lojas[indice]}' atualizadas:\n"
            f"{formatar_moeda(valor_anterior)} → {formatar_moeda(valor)}",
        )

    def selecionar_loja(self, event=None):
        selecionado = self.tabela.selection()
        if not selecionado:
            return
        indice = int(selecionado[0])
        self.entry_loja.delete(0, tk.END)
        self.entry_loja.insert(0, self.lojas[indice])
        self.entry_valor.delete(0, tk.END)
        self.entry_valor.insert(0, formatar_moeda(self.vendas[indice]).replace("R$ ", ""))

    def limpar_campos(self):
        self.entry_loja.delete(0, tk.END)
        self.entry_valor.delete(0, tk.END)
        if self.tabela.selection():
            self.tabela.selection_remove(self.tabela.selection())
        self.entry_loja.focus_set()

    def gerar_relatorio(self):
        linhas = ["RELATÓRIO DE ALTERAÇÕES", "=" * 50, ""]

        inseridas = [h for h in self.historico if h["acao"] == "Inserida"]
        atualizadas = [h for h in self.historico if h["acao"] == "Atualizada"]

        linhas.append(f"Lojas inseridas: {len(inseridas)}")
        linhas.append(f"Vendas atualizadas: {len(atualizadas)}")
        linhas.append("")
        linhas.append("HISTÓRICO")
        linhas.append("-" * 50)

        if not self.historico:
            linhas.append("Nenhuma alteração foi feita até o momento.")
        for h in self.historico:
            if h["acao"] == "Inserida":
                linhas.append(f"[{h['hora']}] INSERIDA: {h['loja']} - {formatar_moeda(h['novo'])}")
            else:
                diferenca = h["novo"] - h["anterior"]
                sinal = "+" if diferenca >= 0 else "-"
                linhas.append(
                    f"[{h['hora']}] ATUALIZADA: {h['loja']}: "
                    f"{formatar_moeda(h['anterior'])} → {formatar_moeda(h['novo'])} "
                    f"({sinal}{formatar_moeda(abs(diferenca))})"
                )

        linhas.append("")
        linhas.append("SITUAÇÃO ATUAL")
        linhas.append("-" * 50)
        for loja, venda in zip(self.lojas, self.vendas):
            linhas.append(f"{loja}: {formatar_moeda(venda)}")
        linhas.append("")
        linhas.append(f"TOTAL DE VENDAS: {formatar_moeda(sum(self.vendas))}")
        return "\n".join(linhas)

    def exibir_relatorio(self):
        janela = tk.Toplevel(self.root)
        janela.title("Relatório")
        janela.geometry("640x420")
        janela.transient(self.root)

        frame = tk.Frame(janela)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        texto = tk.Text(frame, wrap="word", font=("Consolas", 10))
        scrollbar = tk.Scrollbar(frame, command=texto.yview)
        texto.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        texto.pack(side=tk.LEFT, fill="both", expand=True)

        texto.insert("1.0", self.gerar_relatorio())
        texto.config(state="disabled")  # Somente leitura

        tk.Button(janela, text="Fechar Relatório", command=janela.destroy).pack(pady=(0, 10))

    def fechar_programa(self):
        if messagebox.askyesno("Fechar", "Deseja realmente fechar o programa?"):
            self.root.destroy()


def main():
    root = tk.Tk()
    app = LojasVendasApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
