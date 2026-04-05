import pandas as pd
import random
from datetime import datetime

FILE_PATH = "etl.csv"

def carregar_dados():
    try:
        return pd.read_csv(FILE_PATH, sep=';', encoding='utf-8')
    except FileNotFoundError:
        print("Arquivo não encontrado. Criando base vazia.")
        return pd.DataFrame(columns=['UserID', 'Nome', 'Conta', 'Cartao'])

def salvar_csv(df_to_save):
    df_to_save.to_csv(FILE_PATH, sep=';', index=False, encoding='utf-8-sig')
    print(f"\n O arquivo '{FILE_PATH}' foi atualizado.")

# --- FUNÇÕES DE ETL ---

def adicionar_usuario(df):
    try:
        new_id = int(input("\nID do Usuário: "))
        nome = input("Nome: ")
        conta = input("Número da Conta: ")
        cartao = input("Número do Cartão: ")
        
        novo_usuario = {'UserID': new_id, 'Nome': nome, 'Conta': conta, 'Cartao': cartao}
        return pd.concat([df, pd.DataFrame([novo_usuario])], ignore_index=True)
    except ValueError:
        print("ERRO: ID deve ser um número.")
        return df

def modificar_usuario(df):
    try:
        user_id = int(input("\nID do usuário para MODIFICAR: "))
        if user_id in df['UserID'].values:
            idx = df.index[df['UserID'] == user_id][0]
            df.at[idx, 'Nome'] = input(f"Novo Nome [{df.at[idx, 'Nome']}]: ") or df.at[idx, 'Nome']
            df.at[idx, 'Conta'] = input(f"Nova Conta [{df.at[idx, 'Conta']}]: ") or df.at[idx, 'Conta']
            df.at[idx, 'Cartao'] = input(f"Novo Cartão [{df.at[idx, 'Cartao']}]: ") or df.at[idx, 'Cartao']
            print("Usuário atualizado na memória.")
        else:
            print("ID não encontrado.")
    except ValueError:
        print("ERRO: Entrada inválida.")
    return df

def excluir_usuario(df):
    try:
        user_id = int(input("\nID do usuário para EXCLUIR: "))
        df = df[df['UserID'] != user_id]
        print(f"Usuário {user_id} removido da memória.")
    except ValueError:
        print("ERRO: Entrada inválida.")
    return df

# --- FUNÇÃO DE NEWS (para serem inseridas de forma aleatória) ---

def gerar_news(df):
    """Função que escolhe a frase e aplica em todo o DataFrame"""
    def escolher_frase(row):
        mensagens = [
            f"Olá {row['Nome']}, sua conta {row['Conta']} tem ofertas de investimento hoje!",
            f"Ei {row['Nome']}, já pensou em render seu saldo da conta {row['Conta']}?",
            f"Atenção {row['Nome']}! O cartão {row['Cartao']} agora dá cashback.",
            f"{row['Nome']}, o futuro da sua conta {row['Conta']} começa com um aporte.",
            f"Dica: {row['Nome']}, diversificar é o segredo do sucesso!"
        ]
        return random.choice(mensagens)

    data_hoje = datetime.now().strftime('%d_%m_%Y')
    nome_coluna = f'Mensagem_{data_hoje}'
    
    print(f"Gerando notícias na coluna {nome_coluna}...")
    df[nome_coluna] = df.apply(escolher_frase, axis=1)
    return df

# --- MÉTODO PRINCIPAL ---

def main():
    df = carregar_dados()
    
    while True:
        print("\n==============================")
        print("      SISTEMA BANCÁRIO ETL    ")
        print("==============================")
        print("1. Adicionar Usuário")
        print("2. Modificar Usuário")
        print("3. Excluir Usuário")
        print("4. Gerar News Aleatórias")
        print("5. Salvar Alterações (CSV)")
        print("0. Sair do Programa")
        
        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            df = adicionar_usuario(df)
        elif opcao == '2':
            df = modificar_usuario(df)
        elif opcao == '3':
            df = excluir_usuario(df)
        elif opcao == '4':
            df = gerar_news(df)
        elif opcao == '5':
            salvar_csv(df)
        elif opcao == '0':
            confirmar = input("Deseja salvar antes de sair? (s/n): ")
            if confirmar.lower() == 's':
                salvar_csv(df)
            print("Encerrando programa...")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()
