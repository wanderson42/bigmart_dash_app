=======================================
  INSTRUÇÕES DE INSTALAÇÃO
=======================================

Para rodar essa aplicação Dash em uma máquina local, siga os passos abaixo:

------------------------------------------------------
1. CRIE UM AMBIENTE VIRTUAL
------------------------------------------------------

Primeiro, crie um ambiente virtual para garantir que as dependências sejam instaladas de forma isolada. No terminal do VS Code, dentro do diretório do seu projeto, execute o seguinte comando:

python -m venv BigMartDashenv


Isso criará uma pasta chamada `BigMartDashenv` onde o ambiente virtual será armazenado.

------------------------------------------------------
2. ATIVE O AMBIENTE VIRTUAL
------------------------------------------------------

Agora, ative o ambiente virtual para que as dependências sejam instaladas nesse ambiente isolado.

- No **Windows**, execute o comando:

.\dashenv\Scripts\activate


- No **Linux/macOS**, execute o comando:

source dashenv/bin/activate

------------------------------------------------------
4. INSTALE AS DEPENDÊNCIAS
------------------------------------------------------

Com o ambiente virtual ativado e o arquivo `requirements.txt` pronto, execute o seguinte comando para instalar todas as dependências listadas no arquivo:

pip install -r requirements.txt

Esse comando vai instalar todas as bibliotecas necessárias para rodar a aplicação.

------------------------------------------------------
5. VERIFIQUE A INSTALAÇÃO
------------------------------------------------------

Após a instalação, verifique se tudo foi instalado corretamente com o comando:

pip list

Isso exibirá uma lista com todas as dependências instaladas no ambiente virtual. Verifique se todas as bibliotecas que você adicionou no `requirements.txt` estão presentes.

------------------------------------------------------
Agora você pode rodar a aplicação localmente com a certeza de que tudo está configurado corretamente! 🚀

