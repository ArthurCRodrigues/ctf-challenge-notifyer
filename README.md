CTF Watcher com Notificações Pushover 🛰️Um script em Python que monitora uma plataforma CTF (baseada em CTFd) em busca de novos desafios. Quando um novo conteúdo é detectado, ele dispara um alerta sonoro local e envia uma notificação instantânea para seus dispositivos via Pushover.Nunca mais perca o first blood de um desafio! 🩸✨ RecursosMonitoramento Automático: Verifica continuamente uma plataforma CTF em intervalos definidos.Detecção Inteligente: Detecta qualquer novo arquivo ou pasta adicionado à competição, mesmo em subdiretórios.Notificações Instantâneas: Usa o serviço Pushover para enviar alertas customizáveis para seu celular ou desktop.Alerta Sonoro Local: Toca um som no seu computador para garantir que você perceba a novidade.Altamente Configurável: Permite ajustar URL, nome do CTF, diretórios e intervalo via linha de comando.Seguro: Mantém suas chaves e tokens sensíveis como variáveis de ambiente, fora do código-fonte.🚀 Como ConfigurarSiga estes passos para colocar o watcher para funcionar.1. Pré-requisitosPython 3.7 ou superior.pip (gerenciador de pacotes do Python).(Opcional, para Linux) alsa-utils para o alerta sonoro. Instale com sudo apt-get install alsa-utils em sistemas baseados em Debian/Ubuntu.2. InstalaçãoPrimeiro, clone este repositório para a sua máquina local:git clone <URL_DO_SEU_REPOSITORIO>
cd <NOME_DO_SEU_REPOSITORIO>
Em seguida, instale as dependências Python necessárias:pip install -r requirements.txt
(Crie um arquivo requirements.txt com o seguinte conteúdo)requests
ctfd-downloader
3. Obtenção das Chaves e TokensVocê precisará de 3 chaves para o script funcionar. Elas devem ser configuradas como variáveis de ambiente.a) CTF Token (CTF_TOKEN)Acesse a plataforma CTF que você deseja monitorar.Faça login e vá para Settings (Configurações) ou seu perfil.Procure por uma seção de Access Tokens ou similar.Crie um novo token. Copie o valor gerado.b) Pushover User Key (PUSHOVER_USER_KEY)Crie uma conta no site Pushover.net e faça login.Na página principal, você verá sua User Key. Copie-a.Instale o aplicativo do Pushover no seu celular (Android/iOS) e faça login para receber as notificações.c) Pushover API Token (PUSHOVER_API_TOKEN)Ainda no site do Pushover, vá para a seção Apps & Plugins.Clique em Create a New Application / API Token.Preencha os campos:Name: Dê um nome, como CTF Watcher.Description: Notificador de desafios de CTF.Marque a caixa de termos de serviço.Clique em Create Application.A página irá recarregar e mostrar o API Token/Key da sua nova aplicação. Copie-o.4. Configuração do Ambientea) Criar o Som de AlertaCrie ou baixe um arquivo de som curto (formato .wav é o mais compatível) e salve-o na pasta do projeto com o nome alert.wav.b) Definir as Variáveis de AmbienteNo seu terminal, execute os seguintes comandos, substituindo os valores de exemplo pelas suas chaves:# Cole aqui o Access Token do CTF
export CTF_TOKEN='seu_token_aqui_gerado_no_ctfd'

# Cole aqui a sua User Key do Pushover
export PUSHOVER_USER_KEY='sua_user_key_do_pushover'

# Cole aqui o API Token da sua aplicação Pushover
export PUSHOVER_API_TOKEN='seu_api_token_da_app_pushover'
Dica: Para não ter que digitar isso toda vez, adicione essas linhas ao seu arquivo de configuração do shell (como .bashrc, .zshrc ou .profile).🏃 Como UsarCom tudo configurado, você pode iniciar o script.Uso Básico(Usará a URL padrão e salvará os desafios na pasta ctf_name dentro do diretório atual)python3 ctfd_watcher.py
Uso Avançado com ArgumentosVocê pode customizar a execução com os seguintes argumentos:--url: A URL da plataforma CTF.--ctf-name: O nome que será usado para a pasta do CTF.--dir: O diretório onde a pasta do CTF será criada.--interval: O intervalo em segundos entre cada verificação.--sound: O caminho para um arquivo de som de alerta customizado.Exemplo: Monitorar o DiceCTF 2024, salvando os desafios na pasta ~/CTFs e verificando a cada 30 segundos.python3 ctfd_watcher.py \
  --url [https://dicec.tf](https://dicec.tf) \
  --ctf-name "DiceCTF_2024" \
  --dir ~/CTFs \
  --interval 30
Para parar o monitoramento, pressione Ctrl+C no terminal.📂 Estrutura do Projeto.
├── ctfd_watcher.py     # O script principal
├── requirements.txt    # As dependências Python
├── alert.wav           # O arquivo de som para o alerta
└── README.md           # Este guia
Aproveite e bons CTFs!