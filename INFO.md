# Requisitos do sistema

Objetivo: Aplicação WEB para gerenciar processos.


### Fluxos e requisitos gerais


- [x] Usuários-administradores possuem visão de todas as telas e todas permissões
- [x] Super-usuários possuem todas as permissões
- [x] Testar código
- [x] Utilização de boas práticas de UX na solução.
- [ ] Responsividade.
- [ ] Liberação da aplicação utilizando Docker.
- [ ] Enviar email para novos usuário cadastrarem senha
- [ ] Adicionar páginas de errors: 404, 403, 500
- [ ] Adicionar logging: criação, remoção, edição
- [ ] Adicionar mensagens de feedback: criação, remoção, edição



##### Tela: Loging

- [x] Possibilitar usuários com email e senha acessar o sistema

---

##### Tela: Home

Requisitos
- [x] Exibir quantidade de usuários
- [x] Exibir quantidade de processos abertos
- [x] Exibir quantidade de processos pendentes de parecer
- [ ] Estatísticas baseando-se no perfil do usuário (adminsitrator, triador ou finalizador)

---

##### Tela: Usuários

Campos:
- Nome
- Sobrenome
- Email
- Senha
- Permissão (Administrador, Triador ou Finalizador)

Requisitos:

- [x] Criar usuários
- [x] Listar usuários
- [x] Editar usuários
- [x] Remover usuários
- [x] Não permitir remover usuários que já criaram Processos ou Parecer no sistema
- [x] Somente usuários-administradores podem criar, visualizar, editar e remover usuários

---

##### Tela: Processos

Campos:

- Título
- Descrição
- Usuários que devem incluir um parecer
- Parecer
- Criado por

Requisitos:

- [x] Criar processos
- [x] Listar processos
  - [x] Possibilitar busca
  - [x] Paginação
- [x] Editar processos
- [x] Remover processos

- [x] Somente usuários-triadores podem criar, visualizar, editar e remover processos
- [x] Somente usuários-triadores podem atribuir um ou mais usuários a realizar um parecer sobre um processo
- [x] Usuários-finalizadores que já publicaram Parecer em um processo, não podem ser removidos de desse processo

- [x] Usuários-finalizadores podem visualizar somente processos que foram associados a ele

- [x] Usuários-finalizadores podem adicionar um ou mais Parecer em processos associados a ele
- [x] Usuários-finalizadores podem editar e remover Parecer criados por ele
- [x] Um Parecer pode somente ser editar e removido por que o criou
