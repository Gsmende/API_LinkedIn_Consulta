import requests
from auth import auth, headers

#Fazer solicitação na API do usuario usando a URL
def user_info(headers):
    #Obter informações sobre perfil do usuario
    response = requests.get('https://api.linkedin.com/v2/me', headers = headers)
    user_info = response.json()
    return user_info

#Conceder acesso a API e executar função
if __name__ == '__main__':
    credentials = 'credentials.json' #Armazenar credenciais de acesso
    access_token = auth(credentials) #Function da Auth API
    headers = headers(access_token) #Construir cabeçalho na chamada da API
    user_info = user_info(headers) #Requisitar informações de usuario
    print(user_info)