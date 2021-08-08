import json
import requests
import random
import string

#Aplicando as junções das funções criadas
'''
1 - Executar a Autenticação.
2 - Na primeira vez que a função é executada, o navegador abre pedindo que você autentique.
3 - Você terá que colar manualmente o URI redirecionado no prompt.
4 - A URL será analisada para extrair o token de acesso.
5 - Ele salvará o token de acesso
6 - Da próxima vez, ele usará o token de acesso em vez de pedir que você autentique.
'''
def auth(credentials):
    #Setar manualmente a URL de redirecionamento no prompt, para gerar um token primario
    creds = read_creds(credentials)
    print(creds)
    client_id, client_secret = creds['client_id'], creds['client_secret']
    redirect_uri = creds['redirect_uri']
    api_url = 'https://www.linkedin.com/oauth/v2'

    #Verificar se Token existe para autenticação
    if 'access_token' not in creds.keys(): 
        args = client_id,client_secret,redirect_uri
        auth_code = authorize(api_url,*args)
        access_token = refresh_token(auth_code,*args)
        creds.update({'access_token':access_token})
        save_token(credentials,creds)
    else: 
        access_token = creds['access_token']
    return access_token

#Criar o cabeçalho que será usado na solicitação feita à API.headers()
def headers(access_token):
    #Anexar headers na chamada da API
    headers = {
    'Authorization': f'Bearer {access_token}',
    'cache-control': 'no-cache',
    'X-Restli-Protocol-Version': '2.0.0'
    }
    return headers

#criar uma função que lerá o arquivo que criado em .Json com as credenciais 
def read_creds(filename):
    with open(filename) as f:
        credentials = json.load(f)
    return credentials

#Salvar o token de acesso ao arquivo credentials.json, sem precisar fazer multiplos login
def save_token(filename, data):
    #Escrevendo Token nas credenciais em .Json
    data = json.dumps(data, indent=4)
    with open(filename, 'w') as f:
        f.write(data)

#criar uma sequência aleatória de letras para usar como token CSRF.
def create_CSRF_token():
    letters = string.ascii_lowercase
    token = ''.join(random.choice(letters) for i in range(20))
    return token

#Abrir a URL de login no navegador
def open_url(url):
    import webbrowser
    print(url)
    webbrowser.open(url)

#Verificar o redirecionamento url e extrair o token de acesso
def parse_redirect_uri(redirect_response):
    #Analisar redirecionamento em componentes e rxtrair token autorizado
    from urllib.parse import urlparse, parse_qs
 
    url = urlparse(redirect_response)
    url = parse_qs(url.query)
    return url['code'][0]

def authorize(api_url,client_id,client_secret,redirect_uri):
    #Request authentication URL passando os paramentros para o Token
    csrf_token = create_CSRF_token()
    params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'state': csrf_token,
        'scope': 'r_liteprofile,r_emailaddress,w_member_social'
        }
 
    response = requests.get(f'{api_url}/authorization',params=params)
    open_url(response.url)

    #Obter código do verificador de autorização na url de return call
    redirect_response = input('Paste the full redirect URL here:')
    auth_code = parse_redirect_uri(redirect_response)
    return auth_code

#Exchange a Refresh Token for a New Access Token
def refresh_token(auth_code,client_id,client_secret,redirect_uri):
    access_token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
        }
 
    response = requests.post(access_token_url, data=data, timeout=30)
    response = response.json()
    print(response)
    access_token = response['access_token']
    return access_token

#Definindo a função na Main para executar a call do Auth
if __name__ == '__main__':
    credentials = 'credentials.json'
    access_token = auth(credentials)



