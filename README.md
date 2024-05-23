
# Receitaria

Um pequeno projeto em Python que busca receitas no site https://www.receiteria.com.br e envia para o usuário, utilizando **webscraping** com o [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)




## Documentação

Essa biblioteca é de fácil uso, precisando somente de um único comando para buscar as receitas:

```py
receitaria = Receitaria()
receita = receitaria.search_recipe("bolo")
print(receita)
```

Também é possível escrever essa receita para um arquivo .txt:

```py
receita.to_txt()
```