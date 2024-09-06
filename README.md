# software-engineering

Repositório para a disciplina de Engenharia de Software na Fundação Getúlio Vargas.

Grupo: 

- Bruno Kauan Lunardon - 221708016
- Daniel de Miranda Almeida - 241708065
- Gustavo Reis Rocha - 221708011
- Lívia Machado da Silveira Verly - 221708029

# Especificação de Requisitos de Software

## 1. Introdução

### 1.1. Propósito
Este documento descreve os requisitos funcionais e não funcionais do sistema, detalhando as funcionalidades necessárias para garantir o sucesso do projeto.

### 1.2. Escopo
O sistema permitirá que os usuários realizem compras de produtos, criem perfis, interajam com outros usuários e recebam notificações sobre novos produtos e promoções, respeitando a privacidade e segurança dos dados.

## 2. Requisitos Funcionais

### 2.1. Funcionalidades de Pagamento

- **RF01**: O sistema deve permitir que o usuário escolha um cartão de crédito ou débito como forma de pagamento.
- **RF02**: O sistema deve permitir que o usuário selecione a bandeira do cartão no momento do pagamento.

### 2.2. Fidelização e Perfil de Compras

- **RF15**: O sistema deve oferecer sugestões de produtos personalizadas com base no perfil de compras do cliente, utilizando técnicas de machine learning para melhorar a fidelização.

### 2.3. Notificações e Promoções

- **RF18**: O sistema deve enviar notificações sobre novos produtos e promoções para os usuários.

### 2.4. Relatório de Vendas e Avaliações

- **RF20**: O sistema deve permitir que o usuário escolha produtos com base nos resultados de um relatório de vendas.
- **RF21**: O sistema deve possibilitar que o relatório de vendas e avaliações seja exportado nos formatos **CSS** e **Excel**.

### 2.5. Interação e Privacidade de Perfis

- **RF23**: O sistema deve permitir que o usuário envie mensagens privadas para outros usuários.
- **RF24**: O sistema deve permitir que o usuário visualize o histórico de compras de outro perfil, caso este esteja configurado como público.
- **RF25**: O sistema deve permitir a criação de grupos com interesses em comum entre os usuários.
- **RF26**: O usuário deve poder escolher entre ter um perfil privado ou público. Se o perfil for público, o histórico de compras será exibido.

## 3. Requisitos Não Funcionais

### 3.1. Segurança e Privacidade

- **RNF22**: O sistema deve garantir a proteção dos dados pessoais dos usuários, incluindo fotos, nome e histórico de compras, de acordo com as melhores práticas de segurança e legislação de proteção de dados.

## 4. Tarefa de casos de uso e histórias de usuário

Tarefa: criação de um caso de uso e uma história de usuário de um determinado requisito para cada membro do grupo.

### Trabalhos

#### Daniel

#### Gustavo

##### Caso de Uso 
**Cadastro de Conta de Usuário** 
(Ref. 22 da Antônia)

| **Atributo** | **Detalhes** |
|--------------|--------------|
| **Atores**   | Aluno (usuário) |
| **Descrição**  | O usuário acessa a tela de cadastro do aplicativo e preenche seus dados pessoais. Após confirmar o preenchimento, o sistema verifica se uma conta com aquela matrícula já existe. Se não houver duplicidade, o sistema cria uma nova conta e envia uma confirmação de sucesso ao usuário. |
| **Dados**  | Foto (em formato quadrangular .jpg ou .png), nome e número de matrícula (9 dígitos). |
| **Estímulo**   | O usuário preenche todos os campos e envia o formulário de criação de conta. |
| **Resposta**   | O sistema confirma o cadastro com uma mensagem de sucesso e redireciona o usuário para a página do seu perfil. |
| **Comentários**| O sistema deve garantir que nenhuma conta com o número de matrícula fornecido já exista. Caso uma duplicata seja detectada, o cadastro será rejeitado, informando ao usuário. Todas as informações fornecidas devem ser armazenadas de forma segura. |

##### Estória de Usuário

**Gerar Relatório de Vendas**
(Ref. 20 ou 21 do Klebson)

Como **dono de uma empresa de vending machines**, gostaria de **gerar um relatório de vendas personalizável em formato CSV**, para que, em seguida, **possa enviá-lo à minha equipe de analistas, facilitando o processo de análise de vendas**.

#### Lívia

### Lunardon

(Ref. 26 Opção de privacidade do histórico de uso da aplicação)
| **Atributo** | **Detalhes** |
|--------------|--------------|
| **Atores**   | Aluno (usuário), Sistema |
| **Descrição**  | O usuário acessa as configurações de privacidade, em um local adequado da aplicação e escolhe se deseja tornar público ou privado seu histórico de uso. Por padrão o histórico deve ser público e isso deve estar descrito nos termos de uso. Após cada escolha do usuário o sistema deve enviar essa informação para um servidor central.|
| **Dados**  | N\A |
| **Estímulo**   | O usuário preenche todos os campos e envia o formulário de criação de conta. |
| **Resposta**   | O sistema confirma o cadastro com uma mensagem de sucesso e redireciona o usuário para a página do seu perfil. |
| **Comentários**| O sistema deve garantir que nenhuma conta com o número de matrícula fornecido já exista. Caso uma duplicata seja detectada, o cadastro será rejeitado, informando ao usuário. Todas as informações fornecidas devem ser armazenadas de forma segura. |

## 5. Conclusão
Este documento descreveu as principais funcionalidades que o sistema deve apresentar para atender às expectativas dos usuários e garantir a segurança e privacidade dos dados.
