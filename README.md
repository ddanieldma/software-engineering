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

##### Caso de uso
**Envio de mensagens privadas entre usuários**
(Ref. 24 da Antônia)

| **Atributo** | **Detalhes** |
|--------------|--------------|
| **Atores**   | Usuário |
| **Descrição**  | O usuário, pela tela inicial do aplicativo, entra numa aba com uma lista das pessoas que ele segue e pode escolher uma das pessoas dessa lista. Essa escolha leva pra uma tela de chat onde os usuários podem enviar mensagens um para o outro. Essas mensagens são poderão ser vistas pelos dois usuários presentes no chat |
| **Dados**  | Mensagens |
| **Estímulo**   | O usuário entra no chat, escreve uma mensagem e pressiona o botão de enviar |
| **Resposta**   | O sistema coloca a mensagem no chat, visível para ambos os usuários |
| **Comentários**| O sistema deve armazenar o histórico de mensagens por um tempo definido. Usuários devem poder apagar mensagens enviadas. |

##### Estória de Usuário
**Usuário escolhe entre cartão de débito ou crédito como forma de pagamento dentro do aplicativo**
(Ref. 01 do Klebson)

Como **Usuário do aplicativo**, preciso de **escolher entre cartão de crédito ou débito** como **forma de pagamento para adição de moedas virtuais à minha conta no sistema**

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

<img src="imgs\Caso de Uso - Cadastro de Conta.jpg" alt="Diagrama de caso de uso do cadastro de conta de Usuário">

##### Estória de Usuário

**Gerar Relatório de Vendas**
(Ref. 20 ou 21 do Klebson)

Como **dono de uma empresa de vending machines**, gostaria de **gerar um relatório de vendas personalizável em formato CSV**, para que, em seguida, **possa enviá-lo à minha equipe de analistas, facilitando o processo de análise de vendas**.

#### Lívia

##### Caso de Uso 
**Criação de grupos com interesses em comum** 
(Ref. 25 da Antônia)

| **Atributo** | **Detalhes** |
|--------------|--------------|
| **Atores**   | Usuário |
| **Descrição**  | O usuário acessa a tela principal. Ao clicar em “Novo grupo” no menu, irá aparecer outra tela. Nela, ele vai adicionar o nome do grupo, tags relacionadas ao tema do grupo e selecionar se ele será público ou privado. |
| **Dados**  | Não se aplica. |
| **Estímulo**   | O usuário seleciona o ícone de criação de grupo na página inicial. |
| **Resposta**   | O sistema confirma a criação do grupo com uma mensagem de sucesso e disponibiliza um link de convite do grupo. Em seguida, redireciona o usuário para o grupo. Caso o grupo seja público, ele poderá ser apresentado para outros usuários com interesses em comum. |

<img src="imgs\Caso - Novo grupo.jpeg" alt="Diagrama de caso de criação de novo grupo">

##### Estória de Usuário

**Notificações que o usuário recebe**
(Ref. 18 do Klebson)

Como **usuário**, gostaria de **receber notificações com promoções de itens que eu gosto e ter recomendações baseadas no meu histórico**, para que **eu possa consumir pagando menos.**.

#### Lunardon

(Ref. 26 Opção de privacidade do histórico de uso da aplicação)
| Atributo | Detalhes |
|--------------|--------------|
| Atores   | Usuário, Sistema |
| Descrição  | O usuário autenticado acessa as configurações de privacidade, em um local adequado da aplicação e escolhe se deseja tornar público ou privado seu histórico de uso.  Por padrão, o histórico é público, conforme descrito nos termos de uso. Após cada escolha do usuário, o sistema deve enviar essa informação para um servidor central.|
| Dados  | Estado do histórico de uso (público ou privado) |
| Estímulo   | O usuário, após criar sua conta e se autenticar, entra na seção de configurações de privacidade.|
| Resposta   | O sistema confirma a alteração das configurações de privacidade, enviando uma notificação para o usuário. Caso haja erro, o sistema solicita que o usuário tente novamente. |
| Comentários| Todas as informações do usuário devem ser armazenadas com segurança, em conformidade com as normas de proteção de dados.|

<img src="imgs\Use case Lunardon.png" alt="Diagrama de caso de uso das opções de privacidade do histórico">

Estória de usuário.

Como cliente, desejo receber sugestões de produtos personalizadas com base no meu histórico de compras para encontrar facilmente produtos que correspondam aos meus interesses e melhorar minha experiência de compra.

## 5. Conclusão
Este documento descreveu as principais funcionalidades que o sistema deve apresentar para atender às expectativas dos usuários e garantir a segurança e privacidade dos dados.

