----------------------------------------------------------------------------------------------

Queridos professores, por favor, sigam o passo a passo deste README para rodar a aplicação. Devido ao tamanho elevado do arquivo, não foi possível enviá-lo por completo.

----------------------------------------------------------------------------------------------

Utilizamos o TESSERACT como API de leitura de texto nesse projeto.

Utilizamos o YOLO pré-treinado, mas também treinamos o nosso proprio com o seguinte dataset:

https://universe.roboflow.com/fabricio-torres-cqqus/ciclogenius/dataset/1

Se olharem o codigo teste2.py verão dois modelos sendo utilizados, mas para essa entrega estamos usando só um modelo.

----------------------------------------------------------------------------------------------

* Preferencialmente usar o Visual Studio Code para rodar, mas pode utilizar o PyCharm.

- Caso use o Visual Studio Code ative o ambiente virtual Python no terminal com o seguinte comando:

python -m venv venv

*ative o ambiente virtual*

.\venv\Scripts\activate

- Lembre-se de selecionar a versão no canto inferior direito, caso contrario alguns imports não funcionarão.

Se utilizar o PyCharm, não sera necessario ativar o ambiente virtual.

----------------------------------------------------------------------------------------------

- No terminal fazer das seguintes instalações

pip install flask
pip install flask request
pip install ultralytics
pip install cv2 // pip install opencv-python // pip install opencv-python-headless
pip install cx_Oracle
pip install pytesseract  *aqui tambem sera necessario baixar por fora manualmente no link abaixo*

https://github.com/UB-Mannheim/tesseract/wiki

----------------------------------------------------------------------------------------------

- Em relação ao banco de dados, esta utilizando o meu RM (RM99150, 180101) mas pode alterar para o seu.

----------------------------------------------------------------------------------------------

*O arquivo teste2.py é onde esta o nosso back end
*Na pasta 'templates' é onde esta o nosso front end e esta sendo utilizado JSON e JavaScript.

1 - Ao rodar a aplicação certifique se que as rotas não foram alteradas.
2 - Certifique se que o coco-classes.txt esteja no caminho correto. Ele funcionara como dicionario.
3 - Certifique se que esteja com uma webcam conectada ao rodar a aplicação para poder realizar o reconhecimento utilizando a IA.
4 - Certifique se de que o caminho das pastas esta de acordo com os do seu computador.
5 - Para encerrar a aplicação basta dar CTRL+C.

Obrigado .

----------------------------------------------------------------------------------------------

Integrantes - 1TDSPI

Agatha Pires- RM552247 
Enrico do Nascimento- RM552082 
Fabricio Torres - RM97916 
Guilherme Magalhães - RM551805 
Ming - RM99150







