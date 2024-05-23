from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from unidecode import unidecode

class Receita:
    def __init__(self, dict):
        self.link = dict.pop("link")
        self.nome = dict.pop("nome")
        self.preparo = dict.pop("preparo")
        self.ingredientes = dict
        self.string = f"{self.nome} - {self.link}\n\n"
        for k in self.ingredientes.keys():
            self.string += f"{k}\n"
            for v in range(len(self.ingredientes[k])):
                self.string += f"{v+1}) {self.ingredientes[k][v]}\n"

        self.string += "\nModo de Preparo\n"

        for c in range(len(self.preparo)):
            self.string += f"{c+1}) {self.preparo[c]}\n"

    def __str__(self):
        return self.string
    
    def to_txt(self):
        """Escreve o texto em um arquivo .txt
        """
        with open(f"{self.nome}.txt", "w", encoding="utf-8") as f:
            f.write(self.string)


class Receitaria:
    def __init__(self):
        self.url = "https://www.receiteria.com.br/?s={}&post_type=receita"
        self.headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}
    
    def search_recipe(self, recipe_name: str, /) -> Receita:
        """Procura uma receita com o nome especificado

        Args:
            recipe_name (str): Nome da receita

        Returns:
            Receita: Retorna o primeiro item da busca e o retorna
        """
        recipe_name = unidecode(recipe_name.replace(" ", "+"))
        recipe = {}

        html = urlopen(Request(self.url.format(recipe_name), headers=self.headers))
        soup = BeautifulSoup(html.read(), features="html.parser")

        product_div = soup.find('div', class_ = "col-6 col-sm-3 col-md-3 mb-4 newbox")
        recipe["link"] = product_div.find("a")["href"] # getting just the first one
        recipe["nome"] = str(product_div.find("h3"))[4:-5]

        recipe_html = urlopen(Request(recipe["link"], headers=self.headers))
        soup = BeautifulSoup(recipe_html.read(), features="html.parser")

        ingredients_div = soup.find("div", class_="ingredientes mt-4 mb-4")
        ingredients_title = ingredients_div.find_all("h2")
        ingredients_list = ingredients_div.find_all("ul")

        for i in range(len(ingredients_title)):
            li_list = [li.get_text() for li in ingredients_list[i]]
            filtered_li_list = [item for item in li_list if "\n" != item]
            filtered_li_list = [item.replace("\n", "") for item in filtered_li_list]

            recipe.update({str(ingredients_title[i])[5:-6] : filtered_li_list})

        prepare_div = soup.find("ol", class_="lista-preparo-1")
        li_list = [item.get_text() for item in prepare_div.find_all("li")]
        filtered_li_list = [item.replace("\n", "") for item in li_list]
        filtered_li_list = [item.replace("Receiteria", "") for item in filtered_li_list]

        recipe["preparo"] = filtered_li_list

        return Receita(recipe)