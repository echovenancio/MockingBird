# Setup do ambiente de desenvolvimento

## Docker

Caso esteja utilizando o windows você tem a opção de utlizar Hyper-V ou WSL 2 como backend.

### Hyper-V

Se você desejar utilizar [Hyper-V](https://learn.microsoft.com/pt-br/virtualization/hyper-v-on-windows/quick-start/enable-hyper-v)
como backend você consegue habilitar com o seguinte comando no powershell como __administrador__:
```bash
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
```

Você tambem consegue habilitar essa feature através do [painel de controle](https://learn.microsoft.com/pt-br/virtualization/hyper-v-on-windows/quick-start/enable-hyper-v#enable-the-hyper-v-role-through-settings).

### WSL 2

Para [habilitar o wsl 2](https://learn.microsoft.com/en-us/windows/wsl/install)
você vai precisar rodar o seguinte comando em um console powershell como administrador:
```bash
wsl --install
```

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
