# Sistema de Gestão de Locação de Veículos
## Integrantes

- **[Suelen Barbosa Marinho](https://github.com/suelenmarinho)** (31923160)
- **[Lelton Pereira Borges](https://github.com/leltonborges)** (27933091)

# Sobre o Projeto

## Responsabilidade
- Suelen, elaborou a modelagem do sistema e o design da solução
- Lelton, codificou a solução e definiu as regras de locação.

## Disponibilização
O Sistema pode ser acessado [Aqui](https://locacao.leltoncrazy.com/) ou o link direto https://locacao.leltoncrazy.com/

Este domínio estará funcionando até 12 de junho de 2025, não é possível acessa-lo usando a rede da UDF.

[Video Youtube](https://youtu.be/zKoxXEzzHNI)

## Qual problema do mundo real nos inspirou?

A gestão de frotas e locação de veículos é um desafio recorrente em empresas, órgãos públicos e locadoras. Muitas vezes, o controle é feito de forma manual, em planilhas, o que gera retrabalho, erros, falta de rastreabilidade e até prejuízos financeiros por mau uso ou falta de manutenção dos veículos. Queríamos criar uma solução que tornasse esse processo mais seguro, transparente e eficiente.

## Quais são os objetivos do sistema?

Nosso objetivo é oferecer uma plataforma web intuitiva para:
- Cadastrar e gerenciar veículos, clientes, setores e marcas
- Controlar a alocação e devolução de veículos, com registro detalhado de quilometragem
- Garantir que apenas veículos disponíveis sejam alocados
- Evitar exclusão acidental de dados importantes
- Fornecer alertas e validações automáticas para evitar erros comuns

Acreditamos que, ao digitalizar e automatizar essas rotinas, ajudamos empresas a economizar tempo, reduzir custos e aumentar a segurança operacional.

## O que aprendemos com este projeto? Quais foram os maiores desafios?

Aprendemos muito sobre regras de negócio reais do setor de frotas, como a importância do controle de quilometragem, da rastreabilidade das alocações e da validação de dados críticos (ex: CNH válida, veículos disponíveis, etc). Os maiores desafios foram:
- Garantir que todas as regras fossem respeitadas sem prejudicar a experiência do usuário
- Lidar com integrações entre diferentes entidades (veículo, frota, cliente, setor)
- Implementar feedbacks claros para o usuário em cada etapa

## Que melhorias podemos fazer no futuro? Onde mais essa ideia pode ser aplicada?

- Adicionar relatórios gerenciais e dashboards
- Integrar com sistemas de manutenção preventiva
- Permitir upload de documentos e fotos dos veículos
- Disponibilizar API para integração com ERPs
- Adicionar autenticação e permissões por perfil de usuário
- Adaptar para locação de outros bens (máquinas, equipamentos, salas, etc)

---

Este projeto é um sistema web para gestão de locação de veículos, desenvolvido em Django. Ele permite o cadastro, controle e acompanhamento de veículos, clientes, setores, alocações e devoluções, com controle detalhado de quilometragem e regras de negócio específicas para o setor de frotas.

## Funcionalidades Principais

- **Cadastro de Marcas, Modelos e Unidades de Frota**
- **Cadastro de Clientes e Setores**
- **Alocação de veículos para clientes/setores**
- **Registro de devolução de veículos**
- **Controle de quilometragem inicial, estimada e rodada**
- **Validação de regras de negócio**:
  - Só é possível alocar veículos disponíveis
  - Só é possível excluir setores sem alocações
  - Só marcas ativas podem ser usadas em novos cadastros de veículos
  - Na devolução, o usuário informa apenas quantos quilômetros rodou (não o odômetro)
  - O sistema alerta se a quilometragem rodada exceder em mais de 20% a estimativa
- **Listagem e detalhamento de todas as entidades**
- **Interface web responsiva e amigável**

## Tecnologias Utilizadas

- Python 3.12+
- Django 5.2+
- SQLite (padrão, mas pode ser adaptado para outros bancos)
- Bootstrap (via CDN)
- Docker (opcional para containerização)

## Estrutura Básica do Projeto

```
rental/
├── models.py         # Modelos principais (Marca, Veículo, Frota, Cliente, Setor, Alocação)
├── views/            # Views organizadas por domínio
├── templates/        # Templates HTML
├── static/           # Arquivos estáticos (css, js, imagens)
├── ...
manage.py
requirements.txt
Dockerfile
```

## Como rodar localmente

1. **Clone o repositório:**
   ```bash
   git clone <url-do-repo>
   cd manage-rental-car
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Aplique as migrações:**
   ```bash
   python manage.py migrate
   ```

5. **(Opcional) Crie um superusuário:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Rode o servidor de desenvolvimento:**
   ```bash
   python manage.py runserver
   ```

7. **Acesse em:**
   - http://localhost:8000/

## Como rodar com Docker

1. **Build da imagem:**
   ```bash
   docker build -t manage-rental-car .
   ```

2. **Rode o container:**
   ```bash
   docker run -it --rm -p 8000:8000 manage-rental-car
   ```

3. **Acesse em:**
   - http://localhost:8000/

> O Dockerfile está configurado para rodar as migrações automaticamente ao iniciar.

## Regras de Negócio

- **Cadastro de veículos:** Só permite marcas ativas.
- **Alocação:** Só permite veículos disponíveis. Quilometragem inicial é registrada automaticamente.
- **Devolução:** Usuário informa apenas os quilômetros rodados. O sistema soma ao KM inicial e atualiza o odômetro da frota.
- **Validação de quilometragem:** Se rodar mais de 20% acima do estimado, o sistema alerta.
- **Exclusão de setores:** Só possível se não houver alocações vinculadas.

## Regras de Negócio Detalhadas por Tela/Módulo

## Alocação
- Só é possível alocar veículos que estejam disponíveis (`disponivel=True` na unidade da frota).
- Ao criar uma alocação:
  - A quilometragem inicial é registrada automaticamente com base no valor atual da unidade da frota.
  - O usuário pode informar uma estimativa de quilômetros a rodar.
  - Não é possível alocar se a unidade da frota não estiver disponível.
- Ao registrar a devolução:
  - O usuário informa apenas os quilômetros rodados (delta), não o odômetro.
  - O sistema soma esse valor ao KM inicial para atualizar o KM final da alocação e o KM atual da frota.
  - Se o valor informado for negativo, a devolução é rejeitada.
  - Se os quilômetros rodados excederem em mais de 20% a estimativa, o sistema exibe um alerta.
  - Não é possível devolver uma alocação já devolvida.
- Não é possível excluir setores, clientes ou marcas que tenham alocações vinculadas.

## Frota
- Cadastro de unidades de frota exige:
  - Placa única.
  - Quilometragem atual não pode ser negativa.
- Só unidades de frota disponíveis aparecem para alocação.
- Ao devolver um veículo, o KM atual da frota é atualizado automaticamente.
- É possível excluir uma unidade de frota a qualquer momento (não há bloqueio por alocação).

## Modelos de Veículo
- Só é possível cadastrar modelos de veículos para marcas ativas.
- Não é possível excluir uma marca que possua veículos cadastrados.
- Não é possível excluir um modelo de veículo se houver unidades de frota vinculadas (regra sugerida, mas pode ser implementada se desejar).

## Clientes
- Cadastro exige CNH única e válida (data de validade maior ou igual à data atual).
- Não é possível excluir clientes que tenham alocações registradas.
- O sistema exibe badge de CNH válida ou vencida na listagem.
- O cliente pode ser editado a qualquer momento.

## Setores
- Cadastro exige sigla única.
- Não é possível excluir setores que tenham alocações registradas.
- O setor pode ser editado a qualquer momento.

## Marcas
- Só marcas ativas aparecem para seleção ao cadastrar modelos de veículos.
- Não é possível excluir marcas que tenham veículos cadastrados.
- Marcas podem ser ativadas/desativadas a qualquer momento.

## Regras Gerais e Validações
- Todos os cadastros possuem validação de campos obrigatórios.
- Não é possível excluir entidades que estejam em uso (relacionadas a outras entidades).
- O sistema utiliza mensagens de sucesso/erro para feedback ao usuário.
- O sistema é responsivo e amigável, com feedback visual para erros de formulário.
- O sistema alerta o usuário quando há inconsistências ou tentativas de ações proibidas (ex: exclusão de setor com alocações).

## Observações

- O sistema pode ser facilmente adaptado para outros bancos de dados (PostgreSQL, MySQL, etc).
- Para outros ambientes, configure variáveis de ambiente e ajuste o `settings.py` conforme necessário.

