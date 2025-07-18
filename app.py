import streamlit as st
import pandas as pd
import re

REGRAS_DE_CATEGORIZACAO = {
    "Padaria e Frios > Padaria > Pães": ["pão de forma", "pão integral", "pão francês", "pão de queijo"],
    "Mercearia > Matinais e Doces > Leite Condensado e Cremes": ["leite condensado", "creme de leite"],
    "Higiene e Beleza > Cuidados com o Cabelo > Coloração": ["tinta para cabelo", "koleston"],
    "Limpeza > Roupas > Sabão Líquido": ["lava roupas liquido", "ariel"],
    "Mercearia > Secos > Sal e Temperos": ["sal refinado", "cisne"],
    "Mercearia > Líquidos e Conservas > Molhos": ["ketchup", "hemmer", "molho de tomate", "heinz"],
    "Higiene e Beleza > Higiene Pessoal > Higiene Feminina": ["absorvente", "intimus"],
    "Automotivo > Pneus e Rodas > Pneus": ["pneu", "pirelli"],
    "Bebidas > Não Alcoólicas > Refrigerantes": ["refrigerante", "guaraná antarctica", "coca-cola", "pepsi", "fanta", "refri."],
    "Bebidas > Não Alcoólicas > Sucos": ["suco em pó", "tang", "suco", "delvalle", "néctar"],

    # --- HIGIENE E BELEZA ---
    "Higiene e Beleza > Cuidados com o Cabelo > Shampoos": ["shampoo", "head & shoulders", "johnson's baby"],
    "Higiene e Beleza > Cuidados com o Cabelo > Condicionadores": ["condicionador", "condicionador dove"],
    "Higiene e Beleza > Higiene Pessoal > Higiene Bucal": ["creme dental", "colgate", "oral-b", "dente"],
    "Higiene e Beleza > Higiene Pessoal > Sabonetes": ["sabonete", "sabonete liquido", "protex", "dove"],
    "Higiene e Beleza > Higiene Pessoal > Desodorantes": ["desodorante", "rexona"],
    "Higiene e Beleza > Higiene Pessoal > Outros": ["cotonetes", "papel higiênico", "neve"],
    "Higiene e Beleza > Perfumaria > Barbear": ["creme para barbear", "bozzano"],
    "Higiene e Beleza > Perfumaria > Maquiagem": ["esmalte", "risqué", "base liquida", "vult"],

    # --- LIMPEZA ---
    "Limpeza > Roupas > Sabão em Pó": ["sabão em pó", "sabao em po", "omo"],
    "Limpeza > Roupas > Amaciantes": ["amaciante", "comfort", "downy"],
    "Limpeza > Roupas > Alvejantes": ["água sanitária", "agua sanitaria", "qboa", "alvejante"],
    "Limpeza > Casa > Limpadores": ["limp.", "multiuso", "ypê", "ype", "veja", "limpador"],
    "Limpeza > Casa > Esponjas de Aço": ["esponja de aço", "bombril"],
    "Limpeza > Casa > Inseticidas": ["inseticida", "sbp"],
    "Limpeza > Descartáveis > Sacos de Lixo": ["saco de lixo", "embalixo"],
    "Limpeza > Descartáveis > Panos": ["pano de chão"],

    # --- BEBIDAS (REGRAS MAIS GENÉRICAS) ---
    "Bebidas > Não Alcoólicas > Águas": ["agua mineral", "água mineral", "água de coco"],
    "Bebidas > Não Alcoólicas > Chás": ["chá", "cha", "leão fuze"],
    "Bebidas > Não Alcoólicas > Isotônicos": ["isotônico", "gatorade"],
    "Bebidas > Alcoólicas > Vinhos": ["vinho", "aurora", "casillero del diablo", "chalise"],
    "Bebidas > Alcoólicas > Cervejas": ["cerveja", "heineken", "brahma"],
    "Bebidas > Alcoólicas > Destilados": ["vodka", "absolut", "destilado"],
    
    # --- PADARIA E FRIOS (REGRAS MAIS GENÉRICAS) ---
    "Padaria e Frios > Padaria > Pães": ["pão", "pao"],
    "Padaria e Frios > Frios e Laticínios > Queijos": ["queijo", "mussarela", "requeijão", "vigor"],
    "Padaria e Frios > Frios e Laticínios > Frios Diversos": ["presunto", "peito de peru", "salame"],
    "Padaria e Frios > Frios e Laticínios > Iogurtes": ["danone", "iogurte"],
    "Padaria e Frios > Frios e Laticínios > Leite e Derivados": ["leite"],
    "Padaria e Frios > Frios e Laticínios > Manteigas e Margarinas": ["manteiga", "aviação", "margarina", "qualy"],
    
    # --- HORTIFRUTI ---
    "Hortifruti > Frutas": ["maçã", "maca", "fuji", "banana", "laranja", "uva", "mamão", "limão"],
    "Hortifruti > Verduras e Legumes": ["alface", "tomate", "batata", "cebola", "cenoura"],
    
    # --- MERCEARIA (REGRAS MAIS GENÉRICAS) ---
    "Mercearia > Secos > Café": ["café", "3 corações", "pilão", "melitta"],
    "Mercearia > Secos > Arroz, Feijão e Grãos": ["arroz", "feijão", "grãos", "lentilha"],
    "Mercearia > Secos > Farináceos": ["farinha de trigo", "dona benta", "farinha de mandioca"],
    "Mercearia > Secos > Açúcares e Adoçantes": ["açúcar", "acucar", "adoçante", "zero-cal"],
    "Mercearia > Líquidos e Conservas > Enlatados": ["milho em lata", "enlatado", "ervilha", "seleta"],
    "Mercearia > Matinais e Doces > Biscoitos e Snacks": ["biscoito", "bolacha", "recheado", "snack", "trakinas", "negresco", "batata palha", "elma chips", "salgadinho"],
    "Mercearia > Matinais e Doces > Matinais": ["achocolatado", "nescau", "cereal", "sucrilhos"],
    "Mercearia > Matinais e Doces > Chocolates": ["chocolate", "lacta"],
    "Mercearia > Massas": ["macarrão", "espaguete", "penne", "massa", "renata"],
    
    # --- DEMAIS DEPARTAMENTOS ---
    "Congelados > Pratos Prontos": ["lasanha", "pizza congelada"],
    "Congelados > Salgados e Pães": ["pão de queijo congelado", "forno de minas"],
    "Congelados > Sorvetes": ["sorvete", "kibon"],
    "Utilidades Domésticas > Cozinha > Descartáveis e Filtros": ["papel toalha", "filtro de café", "papel alumínio", "wyda"],
    "Utilidades Domésticas > Outros > Pilhas e Lâmpadas": ["pilha", "duracell", "lâmpada", "lampada", "ourolux"],
    "Utilidades Domésticas > Outros > Fósforos e Velas": ["fósforo", "fosforo", "vela de aniversário"],
    "Utilidades Domésticas > Churrasco": ["carvão", "carvao", "acendedor"],
    "Pet Shop > Alimentos > Rações": ["ração", "pedigree", "whiskas", "golden"],
    "Pet Shop > Alimentos > Petiscos": ["petisco", "dreamies"],
    "Pet Shop > Higiene > Tapetes e Outros": ["tapete higiênico"],
    "Mundo Bebê > Higiene > Fraldas": ["fralda", "pampers", "huggies"],
    "Mundo Bebê > Higiene > Lenços Umedecidos": ["lenços umedecidos", "mônica"],
    "Mundo Bebê > Alimentação > Fórmulas e Leites": ["leite em pó ninho"],
    "Mundo Bebê > Alimentação > Papinhas": ["papinha nestlé"]
}

def carregar_csv(arquivo_enviado):
    arquivo_enviado.seek(0)
    linhas = [line.decode('utf-8', errors='ignore') for line in arquivo_enviado.readlines()]
    if not linhas: raise ValueError("O arquivo CSV enviado está vazio.")
    if linhas[0].startswith('\ufeff'): linhas[0] = linhas[0][1:]
    
    cabecalho = [h.strip() for h in linhas[0].split(',')]
    num_colunas_esperado = len(cabecalho)
    dados_corrigidos = []
    
    for num_linha, linha in enumerate(linhas[1:], 2):
        if not linha.strip(): continue
        campos = linha.strip().split(',')
        if len(campos) >= num_colunas_esperado:
            dados_corrigidos.append(campos[:num_colunas_esperado])
        else:
            print(f"AVISO: Linha {num_linha} ignorada (número de colunas insuficiente).")
            
    df = pd.DataFrame(dados_corrigidos, columns=cabecalho)
    return df

def processar_dados(df: pd.DataFrame):
    colunas_necessarias = ['ID_Produto', 'Nome_Produto', 'Descricao']
    for col in colunas_necessarias:
        if col not in df.columns:
            raise ValueError(f"Erro Crítico: A coluna '{col}' não foi encontrada. Verifique o cabeçalho do seu CSV.")

    df['Nome_Produto_Limpo'] = df['Nome_Produto'].str.replace(r'<[^<>]*>', '', regex=True).fillna('')
    df['Descricao_Limpa'] = df['Descricao'].str.replace(r'<[^<>]*>', '', regex=True).fillna('')
    df['texto_combinado_para_busca'] = (df['Nome_Produto_Limpo'].astype(str) + ' ' + df['Descricao_Limpa'].astype(str)).str.lower()
    
    df['temp_cat_n1'], df['temp_cat_n2'], df['temp_cat_n3'] = 'NÃO CATEGORIZADO', '', ''

    for categoria_completa, palavras_chave in REGRAS_DE_CATEGORIZACAO.items():
        niveis = categoria_completa.split(' > ')
        if len(niveis) < 3: continue 

        padrao_regex = '|'.join([re.escape(k) for k in palavras_chave])
        mask_uncategorized = df['temp_cat_n1'] == 'NÃO CATEGORIZADO'
        mask_keywords = df['texto_combinado_para_busca'].str.contains(padrao_regex, na=False, regex=True)
        rows_to_update = mask_uncategorized & mask_keywords

        if rows_to_update.any():
            df.loc[rows_to_update, 'temp_cat_n1'] = niveis[0]
            df.loc[rows_to_update, 'temp_cat_n2'] = niveis[1]
            df.loc[rows_to_update, 'temp_cat_n3'] = niveis[2]
    
    mask_incomplete = (df['temp_cat_n1'] != 'NÃO CATEGORIZADO') & (df['temp_cat_n3'] == '')
    if mask_incomplete.any():
        df.loc[mask_incomplete, ['temp_cat_n1', 'temp_cat_n2', 'temp_cat_n3']] = ['NÃO CATEGORIZADO', '', '']

   
    df_resultado = pd.DataFrame({
        'ID_PRODUTO_SISTEMA': df['ID_Produto'],
        'NOME_PRODUTO': df['Nome_Produto'],
        'NOVA_CATEGORIA_N1': df['temp_cat_n1'],
        'NOVA_CATEGORIA_N2': df['temp_cat_n2'],
        'NOVA_CATEGORIA_N3': df['temp_cat_n3'] 
    })
    return df_resultado

# --- Interface Streamlit ---
st.set_page_config(page_title="Categorizador de Produtos ", page_icon="💻", layout="wide")
st.title("💻 Categorizador de Produtos ")
st.markdown("A ferramenta definitiva para organizar seus produtos. Faça o upload do seu CSV e deixe a mágica acontecer.")

uploaded_file = st.file_uploader("1. Escolha seu arquivo CSV", type="csv")

if uploaded_file is not None:
    try:
        df_bruto = carregar_csv(uploaded_file)
        st.subheader("2. Prévia dos Dados Carregados")
        st.dataframe(df_bruto.head())

        st.subheader("3. Processamento e Resultados")
        with st.spinner('Aplicando inteligência em cada produto...'):
            df_resultado = processar_dados(df_bruto)
        
        st.success("Processamento Concluído!")

        colunas_para_exibir = ['ID_PRODUTO_SISTEMA', 'NOME_PRODUTO', 'NOVA_CATEGORIA_N1', 'NOVA_CATEGORIA_N2', 'NOVA_CATEGORIA_N3']
        df_categorizados = df_resultado[df_resultado['NOVA_CATEGORIA_N1'] != 'NÃO CATEGORIZADO'][colunas_para_exibir]
        df_nao_categorizados = df_resultado[df_resultado['NOVA_CATEGORIA_N1'] == 'NÃO CATEGORIZADO'][['ID_PRODUTO_SISTEMA', 'NOME_PRODUTO']]

        st.markdown("### ✅ Produtos Categorizados com Sucesso")
        st.dataframe(df_categorizados)

        if not df_nao_categorizados.empty:
            st.warning("⚠️ Atenção: Alguns produtos não foram categorizados pelas regras atuais!")
            st.dataframe(df_nao_categorizados)
        else:
            st.balloons()
            st.success("🎉 Fantástico! Todos os produtos foram categorizados com sucesso!")

        st.subheader("4. Download do Arquivo Final")
        df_para_download = df_resultado[['ID_PRODUTO_SISTEMA', 'NOVA_CATEGORIA_N1', 'NOVA_CATEGORIA_N2', 'NOVA_CATEGORIA_N3']]
        csv_resultado = df_para_download.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Fazer Download do Resultado para Importação",
            data=csv_resultado,
            file_name='produtos_prontos_para_importacao.csv',
            mime='text/csv',
        )

    except Exception as e:
        st.error("Ocorreu um erro crítico durante o processamento.")
        st.exception(e)