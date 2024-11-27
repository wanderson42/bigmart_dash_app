=======================================
  INSTRUÇÕES DE INSTALAÇÃO
=======================================

Essa aplicação Dash foi desenvolvida no VScode, cujo o desenvolvimento desse projeto na íntegra pode ser acessada no arquivo DashApp_BigMartSales.ipynb. 
Por conveniência essa aplicação pode ser facilmente executada no Google Colab, realizando o upload do arquivo DashApp_BigMartSales.ipynb e executando as células da seção 5.1 e 5.3.
- As células da seção 5.1 realizam a instalação das dependencias e importação das bibliotecas.
- As células da seção 5.2 contemplam os arquivos helpers.py e app.py. Ao executa-las em ordem a aplicação é renderizada no padrão Dash app.run com redirecionamento automático. 
No caso iniciada no localhost (geralmente no endereço http://127.0.0.1:8050). E ao clicarmos no endereço o Colab detecta que o servidor foi iniciado e cria um link no formato https://<túnel>-colab.googleusercontent.com para acesso público.

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



