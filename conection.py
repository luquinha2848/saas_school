import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="saas_escola",
        user="postgres",
        password="xbala"
    )

    print("✅ Conexão realizada com sucesso!")

    # Fecha a conexão
    conn.close()

except Exception as e:
    print("❌ Erro ao conectar ao banco de dados")
    print(e)
