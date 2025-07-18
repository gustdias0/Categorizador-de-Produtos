# Categorizador de Produtos


GIF do funcionamento

[![GIF do funcionamento.](https://imgur.com/h2df3Mm)](https://github.com/user-attachments/assets/56dca9b2-dd01-4bb2-b6fc-44ef9d9bf497)


---

### 🤔 Para que serve este aplicativo?

O objetivo é simples: pegar um CSV e devolver um arquivo limpo e organizado.

### O que ele faz ?

* **Lê arquivos "sujos"** que outros programas normalmente rejeitam (com vírgulas extras, erros de formatação, etc.).
* **Limpa os dados**, removendo tags HTML e padronizando o texto.
* **Usa um "cérebro" de regras customizável** para categorizar cada produto em 3 níveis de hierarquia.
* **Mostra os resultados** em uma interface web simples e permite que você baixe o arquivo final com um clique.

---

### 🚀 Como rodar na sua máquina

**Passo 1: Prepare o ambiente**

Abra o terminal na pasta do projeto e crie um ambiente virtual para instalar as bibliotecas.

```bash
# Crie o ambiente
python -m venv venv

# Ative o ambiente
# No Windows:
venv\Scripts\activate
# No Mac/Linux:
source venv/bin/activate

# Instale as bibliotecas necessárias
pip install streamlit pandas
```

**Passo 2: Execute o aplicativo**

Com o ambiente ativo, basta rodar o seguinte comando:

```bash
streamlit run app.py
```

Isso vai abrir seu navegador pra testar o app.

---

### 🧠 Como usar e "ensinar" o aplicativo

1.  **Faça o upload do seu CSV:** Arraste e solte o arquivo na área indicada.
2.  **Analise os resultados:** O app vai mostrar duas listas: os produtos que ele conseguiu categorizar e os que ele não reconheceu.
3.  **Ensine novas regras:** Para os produtos que não foram reconhecidos, você pode ensiná-los ao app!
    * Abra o arquivo `app.py`.
    * Procure pelo dicionário gigante chamado `REGRAS_DE_CATEGORIZACAO`.
    * Adicione uma nova linha com a nova regra. Por exemplo:
        ```python
        "Nova Categoria > Nova Subcategoria > Detalhe": ["palavra-chave-do-produto", "outra-palavra"],
        ```
    * Salve o arquivo. O aplicativo no navegador será atualizado na hora com o novo conhecimento!

### Feito com

* ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
* ![streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
* ![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)

---

## Feito por: Luís Gustavo S. Dias 💻
