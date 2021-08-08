import requests
from auth import auth, headers

credentials = 'credentials.json'
access_token = auth(credentials) # Authenticate the API
headers = headers(access_token)

#Fazer requisição na API
def user_info(headers):
    #Obter informações de usuario
    response = requests.get('https://api.linkedin.com/v2/me', headers = headers)
    user_info = response.json()
    return user_info

#Obtendo informação do ID para criar uma UGC Post
user_info = user_info(headers)
urn = user_info['id']

#Utilizando a API UGC para shares
api_url = 'https://api.linkedin.com/v2/ugcPosts'
author = f'urn:li:person:{urn}'

#Criando um corpo de texto para a postagem
message_bot = "Hello World, this is a LinkedIn bot in Python!"
#link = "https://www.linkedin.com/company/74678824/"
link_text = "Requisições na API do LinkedIn com Python"

#Marcar uma pagina ou empresa na publicação
mention_name = 'DoWhileAlive'
msg_mention = f'A Microempresa {mention_name}, fundada no dia 25/06/2021, tem como objetivo divulgar automações e programas desenvolvidos em Python na intenção de trazer ainda mais membros para essa comunidade, nos importamos com o seu sucesso e a nossa conquista, é o seu progresso! #VemConosco'
mention_id = '74678824'
mention_urn = f'urn:li:organization:{mention_id}'
link = 'https://www.linkedin.com/company/74678824/'

#Encontrar a posição que se encontra a referencia
def find_pos(mention_name, message):
    index = 0
    if mention_name in message:
        c = mention_name[0]
        for ch in message:
            if ch == c:
                if message[index:index+len(mention_name)] == mention_name:
                    return index
            index += 1
    return -1

#Armazenar a atribuição
len_uname = len(mention_name)
start = find_pos(mention_name, msg_mention)

#Configurações e permissões do Post
post_data = {
    "author": author,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "attributes": [
                        {
                            "length": len_uname,
                            "start": start,
                            "value": {
                                "com.linkedin.common.CompanyAttributedEntity": {
                                    "company": mention_urn
                                }
                            }
                        }
                    ],
                    "text": msg_mention
                },
                "shareMediaCategory": "ARTICLE",
                "media": [
                    {
                        "status": "READY",
                        "description": {
                            "text": message_bot
                        },
                        "originalUrl": link,
                        "title": {
                            "text": link_text
                        }
                    }
                ]
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "CONNECTIONS"
        }
    }

#Chamada da função main
if __name__ == '__main__':
    r = requests.post(api_url, headers=headers, json=post_data)
    r.json()
