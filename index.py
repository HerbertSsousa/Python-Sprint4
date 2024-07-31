import json
import oracledb

class DadosIA:
    def __init__(self):
        self.dados = {}
        self.proximo_id = 1

    @staticmethod
    def create_oracle_connection():
        with open("credenciais.json") as f:
            credenciais = json.load(f)

        user = credenciais["user"]
        password = credenciais["pass"]

        dsn_str = oracledb.makedsn("oracle.fiap.com.br", 1521, "ORCL")

        conn = oracledb.connect(user=user, password=password, dsn=dsn_str)

        cursor = conn.cursor()
        return conn, cursor

    def filtrar_e_armazenar_dados(self):
        try:
            conn, cursor = self.create_oracle_connection()

            for dado in self.dados.values():
                categoria_id = dado["categoriaProdutoID"]
                cursor.execute("SELECT ID_categoria FROM CategoriaProduto WHERE ID_categoria = :id", id=categoria_id)
                if not cursor.fetchone():
                    print(f"Erro: categoriaProdutoID {categoria_id} não encontrado na tabela CategoriaProduto.")
                    continue

                nome = dado["nome"]
                descricao = dado["descricao"]
                preco = dado["preco"]
                categoriaProdutoID = categoria_id
                quantidade = dado["quantidade"]
                status = dado["status"]

                query = """
                        INSERT INTO Produto (nome, descricao, preco, categoriaProdutoID, quantidade, status) 
                        VALUES (:nome, :descricao, :preco, :categoriaProdutoID, :quantidade, :status)
                        """
                cursor.execute(query, nome=nome, descricao=descricao, preco=preco,
                            categoriaProdutoID=categoriaProdutoID, quantidade=quantidade, status=status)

            conn.commit()
            print("Registros inseridos com sucesso.")
        except Exception as e:
            print("Erro ao filtrar e armazenar dados:", e)
        finally:
            conn.close()  
            print("Processo de filtragem e armazenamento de dados finalizado.")





    def inserir_dados(self, novo_dado, cursor, conn):
        try:
            nome = novo_dado["nome"]
            descricao = novo_dado["descricao"]
            preco = novo_dado["preco"]
            categoriaProdutoID = novo_dado["categoriaProdutoID"]
            quantidade = novo_dado["quantidade"]
            status = novo_dado["status"]

            query = """
                INSERT INTO Produto (ID_produto, nome, descricao, preco, categoriaProdutoID, quantidade, status) 
                VALUES (produto_seq.NEXTVAL, :nome, :descricao, :preco, :categoriaProdutoID, :quantidade, :status)
                """

            cursor.execute(query, nome=nome, descricao=descricao, preco=preco, categoriaProdutoID=categoriaProdutoID, quantidade=quantidade, status=status)
            conn.commit()
            print("Registro inserido com sucesso.")
        except Exception as e:
            print("Erro ao inserir registro:", e)
        finally:
            print("Processo de inserção de dados finalizado.")


    def atualizar_dados(self, identificador, nova_dado):
        try:
            for chave, valor in self.dados.items():
                if chave == identificador:
                    self.dados[chave]["descricao"] = nova_dado
                    break
            else:
                print("Registro não encontrado.")
        except Exception as e:
            print("Erro ao atualizar dado:", e)
        finally:
            print("Processo de atualização de dados finalizado.")

    def excluir_dados(self, identificador):
        try:
            del self.dados[identificador]
            print("Registro excluído.")
        except KeyError:
            print("Registro não encontrado.")
        except Exception as e:
            print("Erro ao excluir dado:", e)
        finally:
            print("Processo de exclusão de dados finalizado.")

    

    def exportar_para_json(self, dados, nome_arquivo):
        with open(nome_arquivo, 'w') as arquivo:
            json.dump(dados, arquivo, indent=4)
        print(f"Dados exportados para {nome_arquivo}.")

    def exibir_menu(self):
        while True:
            print("\nMenu Principal:")
            print("1. Visualizar dados")
            print("2. Manipular dados")
            print("3. Exportar consulta para JSON")
            print("4. Sair")

            try:
                opcao = int(input("Escolha uma opção: "))
                if opcao == 1:
                    self.exibir_dados()
                elif opcao == 2:
                    self.exibir_menu_manipular_dados()
                
                elif opcao == 3:
                    categoria = input("Digite a categoria para filtrar os dados: ")
                    resultados = self.consultar_dados_por_categoria(categoria)
                    nome_arquivo = input("Digite o nome do arquivo JSON para exportação: ")
                    self.exportar_para_json(resultados, nome_arquivo)
                elif opcao == 4:
                    print("Saindo do programa...")
                    break
                else:
                    print("Opção inválida. Tente novamente.")
            except ValueError:
                print("Opção inválida. Deve ser um número inteiro.")

    def exibir_menu_manipular_dados(self):
        while True:
            print("\nMenu Manipular Dados:")
            print("1. Inserir novo registro")
            print("2. Atualizar registro existente")
            print("3. Excluir registro")
            print("4. Voltar ao menu principal")

            try:
                opcao = int(input("Escolha uma opção: "))
                if opcao == 1:
                    nome = input("Digite o nome do novo produto: ")
                    descricao = input("Digite a descrição do novo produto: ")
                    preco = float(input("Digite o preço do novo produto: "))
                    categoriaProdutoID = int(input("Digite o ID da categoria do novo produto: "))
                    quantidade = int(input("Digite a quantidade do novo produto: "))
                    status = input("Digite o status do novo produto: ")
                    
                    novo_dado = {
                        "nome": nome,
                        "descricao": descricao,
                        "preco": preco,
                        "categoriaProdutoID": categoriaProdutoID,
                        "quantidade": quantidade,
                        "status": status
                    }
                    conn, cursor = self.create_oracle_connection()
                    self.inserir_dados(novo_dado, cursor, conn)
                    conn.close()
                elif opcao == 2:
                    identificador = int(input("Digite o número do registro a ser atualizado: "))
                    nova_descricao = input("Digite a nova descrição do registro: ")
                    self.atualizar_dados(identificador, nova_descricao)
                elif opcao == 3:
                    identificador = int(input("Digite o número do registro a ser excluído: "))
                    self.excluir_dados(identificador)
                elif opcao == 4:
                    break
                else:
                    print("Opção inválida. Tente novamente.")
            except ValueError:
                print("Opção inválida. Deve ser um número inteiro.")

    def exibir_dados(self):
        try:
            conn, cursor = self.create_oracle_connection()

            cursor.execute("SELECT * FROM Produto")
            produtos = cursor.fetchall()

            print("Dados da tabela Produto:")
            for produto in produtos:
                print(produto)  

        except Exception as e:
            print("Erro ao exibir dados da tabela Produto:", e)
        finally:
            conn.close()
            print("Processo de exibição de dados da tabela Produto finalizado.")



def main():
    dados_ia = DadosIA()
    dados_ia.filtrar_e_armazenar_dados()
    dados_ia.exibir_menu()

if __name__ == "__main__":
    main()
