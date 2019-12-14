Busca por informações de vereadores da Frente Parlamentar de Saneamento
Básico da Câmara do Rio de Janeiro, através de *scraping* da página da
Câmara e de consultas à API do [Brasil.io](https://brasil.io). Feita para o
Hackaton do Saneamento, no Segundo Encontro do Saneamento da Maré:

https://medium.com/cocozap/dois-dias-de-articula%C3%A7%C3%A3o-pelo-direito-ao-saneamento-na-mar%C3%A9-fd3bdd032e13


Instalação dos requerimentos (necessário Python3 e Pip):

```python
pip3 install -r requirements.txt```
```

O arquivo `ids_cpf.txt` guarda uma relação de IDs (da base de dados da
Câmara, retirados da URL da página do(a) parlamentar) e CPFs (coletados
manualmente pela equipe do hackaton). Eles são usados respectivamente como
chaves de consulta para puxar os dados da Câmara e do Brasil.io.

```python
python3 vereadores.py
```

Pega dados das seguintes fontes:

- Câmara de Vereadores: dados pessoais, redes sociais, links diretos pras páginas de Frentes, Votações e Mandatos

- BrasilIO: datasets onde o CPF foi encontrado, empresas em que pode ter
  sociedade (busca a partir do nome)

Usa o `brasil.py` tirado do [Python's brasil library: access Brazilian data
through Brasil.IO API](https://github.com/turicas/brasil)
