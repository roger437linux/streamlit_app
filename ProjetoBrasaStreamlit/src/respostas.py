# =====================================================================
#  SUAS RESPOSTAS
# =====================================================================
#  Escreva cada consulta SQL entre as aspas triplas, assim:
#
#      Q1 = """
#      SELECT ...
#      FROM ...
#      """
#
#  Depois salve o arquivo (Ctrl+S) e veja o resultado no painel.
#  Mexa só no que está ENTRE as aspas triplas.
# =====================================================================

# ---------------------------------------------------------------------
#  NÍVEL 1 - AQUECIMENTO
# ---------------------------------------------------------------------

# Q1. Clientes no Centro
# Colunas do resultado: ClientesNoCentro
Q1 = """
 SELECT * FROM clientes
WHERE bairro = 'Centro'
ORDER BY nome ASC;

"""

# Q2. Hambúrgueres acima de R$ 30
# Colunas do resultado: NomeProduto, Preco
Q2 = '''
    SELECT nome_produto, preco FROM produtos
    WHERE categoria LIKE '%_amb_rguer%' AND preco > 30
    ORDER BY preco DESC;
'''

# Q3. Pedidos por status
# Colunas do resultado: Status, QuantidadePedidos
Q3 = '''
    SELECT STATUS, COUNT(*) AS qtde_pedidos
    FROM pedidos
    GROUP BY STATUS
    ORDER BY STATUS DESC;
'''


# Q4. Nota média e pedidos sem avaliação
# Colunas do resultado: PedidosEntregues, PedidosAvaliados, PedidosSemAvaliacao, NotaMedia
Q4 = '''
    SELECT
        COUNT(*) AS "Pedidos entregues",
        COUNT(avaliacao) AS "Qtde com avaliação",
        COUNT(*) - COUNT(avaliacao) AS "Qtde sem avaliação",
        CAST(AVG(avaliacao) AS NUMERIC(5, 2)) AS "Média avaliação"
    FROM pedidos
    WHERE status = 'Entregue';
'''


# Q5. Delivery x Retirada por mês
# Colunas do resultado: Mes, TipoEntrega, QuantidadePedidos
Q5 = '''
    SELECT tipo_entrega,
    CASE
        WHEN MONTH(data_pedido) = 1 THEN 'Jan'
        WHEN MONTH(data_pedido) = 2 THEN 'Fev'
        WHEN MONTH(data_pedido) = 3 THEN 'Mar'
    END AS "Mês", 
    COUNT(*) AS qtde
    from pedidos
    GROUP BY MONTH(data_pedido), tipo_entrega
    ORDER BY MONTH(data_pedido) ASC;
'''

# ---------------------------------------------------------------------
#  NÍVEL 2 - CRUZANDO TABELAS
# ---------------------------------------------------------------------

# Q6. Pedidos de janeiro com cliente
# Colunas do resultado: IdPedido, DataPedido, Nome, Bairro, Status
Q6 = '''
    select p.id_pedido AS "Número pedido", 
    p.data_pedido AS "Data pedido", 
    p.status, c.nome AS "Cliente", c.bairro
    from pedidos p
    inner join clientes c
    on c.id_cliente = p.id_cliente
    where YEAR(p.data_pedido) = 2026 and MONTH(p.data_pedido) = 1
    order by p.data_pedido asc;
'''


# Q7. Entregas por entregador
# Colunas do resultado: Nome, Entregas
Q7 = '''
    SELECT e.nome_entregador AS "Entregador", 
    COUNT(p.id_pedido) AS "Qtde entrega"
    FROM pedidos p
    INNER JOIN entregadores e
    ON e.id_entregador = p.id_entregador
    WHERE p.status =  'Entregue'
    GROUP BY e.nome_entregador
    ORDER BY "Qtde entrega" DESC;
'''

# Q8. Unidades e faturamento por produto
# Colunas do resultado: NomeProduto, UnidadesVendidas, Faturamento
Q8 = '''
    SELECT p.nome_produto AS "Produto",
    SUM(i.quantidade) AS "Qtde vendida",
    p.preco AS "Preço R$",
    CAST(SUM(i.quantidade) * p.preco AS NUMERIC(10, 2)) AS "Faturamento R$"
    FROM produtos p
    INNER JOIN itenspedido i
    ON p.id_produto = i.id_produto
    GROUP BY p.nome_produto, p.preco
    ORDER BY "Qtde vendida" DESC;
'''

# Q9. Faturamento por categoria
# Colunas do resultado: Categoria, Faturamento
Q9 = '''
    SELECT
        p.categoria,
        SUM(i.quantidade * i.preco) AS faturamento
    FROM produtos AS p
    INNER JOIN itenspedido AS i
        ON i.id_produto = p.id_produto
    GROUP BY
        p.categoria
    ORDER BY
        faturamento DESC;
'''

# Q10. Bairros com 7+ pedidos entregues
# Colunas do resultado: Bairro, PedidosEntregues
Q10 = '''
    SELECT
        c.bairro,
        COUNT(p.id_pedido) AS quantidade_pedidos
    FROM clientes AS c
    INNER JOIN pedidos AS p
        ON p.id_cliente = c.id_cliente
    WHERE p.status = 'entregue'
    GROUP BY
        c.bairro
    HAVING COUNT(p.id_pedido) >= 7
    ORDER BY quantidade_pedidos DESC;
'''


# Q11. Preços praticados do X-Bacon
# Colunas do resultado: PrecoUnitario, Unidades, Faturamento
Q11 = '''
    SELECT
        i.preco,
        SUM(i.quantidade) AS unidades_vendidas,
        SUM(i.quantidade * i.preco) AS faturamento
    FROM produtos AS p
    INNER JOIN itenspedido AS i
        ON i.id_produto = p.id_produto
    WHERE p.nome_produto = 'X-Bacon'
    GROUP BY i.preco
    ORDER BY i.preco;
'''

# ---------------------------------------------------------------------
#  NÍVEL 3 - DESAFIO
# ---------------------------------------------------------------------

# Q12. Top 3 clientes (fidelidade)
# Colunas do resultado: Nome, Pedidos, TotalGasto
Q12 = '''
    SELECT TOP(3)
        c.nome AS cliente,
        COUNT(DISTINCT p.id_pedido) AS quantidade_pedidos,
        SUM(i.quantidade * i.preco) AS total_gasto
    FROM clientes AS c
    INNER JOIN pedidos AS p
        ON p.id_cliente = c.id_cliente
    INNER JOIN itenspedido AS i
        ON i.id_pedido = p.id_pedido
    GROUP BY
        c.id_cliente,
        c.nome
    ORDER BY
        total_gasto DESC, quantidade_pedidos DESC;
'''

# Q13. Faturamento mês a mês
# Colunas do resultado: Mes, PedidosEntregues, Faturamento
Q13 = '''
    SELECT 
        month(pedidos.data_pedido) as mes,
        count(distinct(pedidos.id_pedido)) as "pedidos entregues",
        sum(itenspedido.quantidade * itenspedido.preco) as faturamento
    from pedidos
    inner join itenspedido
    on pedidos.id_pedido = itenspedido.id_pedido
    where pedidos.status = 'Entregue'
    group by month(pedidos.data_pedido)
'''

# Q14. Entregador do trimestre
# Colunas do resultado: Nome, Entregas, NotaMedia
Q14 = '''
    SELECT 
        entregadores.nome_entregador,
        COUNT(pedidos.id_pedido) AS qtde_entregas,
        AVG(CAST(pedidos.avaliacao AS NUMERIC(5, 1))) AS nota_media
    FROM entregadores
    INNER JOIN pedidos
    ON entregadores.id_entregador = pedidos.id_entregador
    WHERE pedidos.status = 'Entregue'
    GROUP BY entregadores.nome_entregador
    HAVING COUNT(pedidos.id_pedido) >= 4 
    AND AVG(pedidos.avaliacao) >= 4
    ORDER BY qtde_entregas DESC, nota_media DESC;

'''

# Q15. Valor total dos pedidos de março
# Colunas do resultado: IdPedido, Nome, ValorProdutos, TaxaEntrega, ValorTotal
Q15 = '''
    SELECT
        p.id_pedido,
        c.nome AS cliente,
        SUM(i.quantidade * i.preco) + p.taxa_entrega AS valor_total
    FROM pedidos AS p
    INNER JOIN clientes AS c
        ON c.id_cliente = p.id_cliente
    INNER JOIN itenspedido AS i
        ON i.id_pedido = p.id_pedido
    WHERE p.status = 'entregue'
    AND MONTH(p.data_pedido) = 3
    GROUP BY
        p.id_pedido,
        c.nome,
        p.taxa_entrega
    ORDER BY
        valor_total DESC;
'''

# Q16. Clientes sem nenhum pedido
# Colunas do resultado: Nome, Bairro, DataCadastro
Q16 = '''
    SELECT clientes.nome, clientes.bairro
    FROM clientes
    LEFT JOIN pedidos
    ON clientes.id_cliente = pedidos.id_cliente
    WHERE pedidos.id_cliente IS NULL
    ORDER BY clientes.nome ASC;
'''

# Q17. Produto que nunca foi vendido
# Colunas do resultado: NomeProduto, Categoria, Preco
Q17 = '''
    SELECT produtos.nome_produto, itenspedido.id_produto
    FROM produtos
    LEFT JOIN itenspedido
    ON produtos.id_produto = itenspedido.id_produto
    WHERE itenspedido.id_produto IS NULL;
'''

