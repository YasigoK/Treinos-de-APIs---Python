# Pesquisa de dados baseado no CEP

A proposta do repositório é para servir como estudo sobre usos de APIs, mais precisamente sobre a api da [VIACEP](https://viacep.com.br/)

A ideia e base do exercício veio do vídeo [
API de CEP e Busca de Endereços com Python](https://www.youtube.com/watch?v=m72WIejruxI) do canal do youtube [Hashtag Programação](https://www.youtube.com/@HashtagProgramacao)

Como mencionado, a ideia é fornecer os dados de uma requisição a API do viacep partidon de um cep digitado, o resultado sairia como uma tabela json semelhante a esta

```
JSON
URL: viacep.com.br/ws/01001000/json/

    {
      "cep": "01001-000",
      "logradouro": "Praça da Sé",
      "complemento": "lado ímpar",
      "unidade": "",
      "bairro": "Sé",
      "localidade": "São Paulo",
      "uf": "SP",
      "estado": "São Paulo",
      "regiao": "Sudeste",
      "ibge": "3550308",
      "gia": "1004",
      "ddd": "11",
      "siafi": "7107"
    }
          
```

O programa vai passar como ref o cep digitado na interface, buscar da mesma forma que o exemplo acima faz, e exibir dentro da interface as informações fornecidas pela api

### Exemplo de execução :


