# Lojas e Faturamento

Aplicativo desktop em Python para cadastrar lojas e acompanhar seus valores de vendas. A interface é feita com Tkinter e exibe os dados em uma tabela, o total de vendas e um relatório das alterações realizadas durante a execução.

## Funcionalidades

- Lista inicial de lojas e valores de vendas para Rio de Janeiro, São Paulo e Curitiba.
- Cadastro de novas lojas, sem permitir nomes duplicados (a comparação não diferencia maiúsculas de minúsculas).
- Atualização do valor de vendas de uma loja existente.
- Exibição do total de vendas e formatação dos valores em reais no padrão brasileiro.
- Relatório das lojas inseridas e das vendas atualizadas durante a sessão.
- Validação de nomes e valores informados.

> Os dados e o histórico são mantidos apenas enquanto o programa está aberto. Ao fechar o aplicativo, as alterações não são salvas.

## Requisitos

- Python 3 instalado.
- Tkinter disponível na instalação do Python. Em algumas distribuições Linux, pode ser necessário instalar o pacote Tkinter separadamente.

O programa utiliza apenas módulos da biblioteca padrão do Python; não há dependências de terceiros.

## Como executar

No terminal, na pasta do repositório, execute:

```bash
python "Lista_de_Numéricos.py"
```

Se o comando `python` não apontar para o Python 3, use `python3`:

```bash
python3 "Lista_de_Numéricos.py"
```

## Como usar

1. Informe o nome da loja e o valor das vendas.
2. Escolha **Inserir Loja** para cadastrar uma loja ou **Atualizar Vendas** para alterar uma loja existente.
3. Selecione uma loja na tabela para preencher os campos e facilitar a atualização.
4. Consulte o total exibido abaixo da tabela ou selecione **Exibir Relatório** para ver o histórico e a situação atual.

Os valores aceitam formatos como `15000`, `15.000,50` e `15000.50`. Valores negativos não são aceitos.
