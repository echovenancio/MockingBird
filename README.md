# Setup do ambiente de desenvolvimento

## Docker

Caso esteja utilizando o windows você tem a opção de utlizar Hyper-V ou WSL 2 como backend, escolha um dos dois e instale.
__Obs: Recomendo utilizar o wsl__. 

### WSL 2

Para [habilitar o wsl 2](https://learn.microsoft.com/en-us/windows/wsl/install)
você vai precisar rodar o seguinte comando em um console powershell como administrador:
```bash
wsl --install
```

### Hyper-V

Se você desejar utilizar [Hyper-V](https://learn.microsoft.com/pt-br/virtualization/hyper-v-on-windows/quick-start/enable-hyper-v)
como backend você consegue habilitar com o seguinte comando no powershell como __administrador__:
```bash
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
```

Você tambem consegue habilitar essa feature através do [painel de controle](https://learn.microsoft.com/pt-br/virtualization/hyper-v-on-windows/quick-start/enable-hyper-v#enable-the-hyper-v-role-through-settings).

### Finalização da instalação

Após habilitar qualquer uma das features você deve reiniciar o computador.

Agora você pode seguir os passos da [instalação interativa](https://docs.docker.com/desktop/install/windows-install/#install-interactively).

## DevContainers

No uso do vscode você vai precisar da extensão [devcontainers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).

Quando você clonar o projeto com:
```bash
git clone https://github.com/echovenancio/MockingBird.git
```
E abrir o projeto no vscode deve aparecer uma notificação avisando que a extensão devcontainers
detectou uma imagem dando a opção de reabir o projeto dentro do container.
Caso a notificação não apareça, você vai clicar em um simbolo de duas setas apontando em
direções opostas no canto inferior esquerdo do editor. Ao clicar no simbolo irá aparecer um menu
popup e você deve clicar na opção "Reabrir no container".

## Desenvolvendo

Antés de implementar uma feature crie um novo braço apartir do braço 'dev'. Ex:
```bash
git switch dev
git pull origin dev
git switch -c nome-feature
# Desenvolvimento da feature ...
git push origin nome-feature
```

Na interface do github você vai criar um pull request para dar um merge de 'nome-feature' para
o braço 'dev'.

## Makefile

make é uma ferramenta onde você define alguns comandos em um arquivo 'Makefile' que realizam uma
série de construir o seu projeto entre outras coisas.

No 'Makefile' do projeto existem algumas definições, sendo elas:
- run -> Cria um servido e roda o tailwind para construir o arquivo de estilo.
- check -> Realiza checks.
- test -> Executa testes.
- format -> Formata os arquivos no projeto com 'ruff'.
- fix -> Aplica sugestões do 'ruff check'.
- normalize -> Executa 'format' e 'fix'. Obs: Rode esse comando toda vez que for fazer um commit.

Exemplo de uso do 'make':
```
make run
```
