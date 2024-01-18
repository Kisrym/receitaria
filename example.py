from Receitaria import *

receitaria = Receitaria()
receita = receitaria.search_recipe("bolo de chocolate")
print(receita)
receita.to_txt()
