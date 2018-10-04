import json
"""
module init tests
"""

token_user = {
    "user_name": "admin",
    "email": "admin@gmail.com",
    "password": "12345678",
}
OTHER_USER = {
    "user_name": "mukasa",
    "email": "mukasa@gmail.com",
    "password": "12345678",
}
EMPTY_NAME = {
    "user_name": "       ",
    "email": "a4a@gmail.com",
    "password": "0123456789",
}

LOGIN = {
    "email": "a4a@gmail.com",
    "password": "0123456789",

}
LOGIN_OTHER_USER = {
    "email": "admin@gmail.com",
    "password": "0123456789",
}
ORDER = {
    "item_id": 1,
    
}
EMPTY_ITEM = {
    "item": "     ",
}
NEW_ITEM = {
    "item_name": "matooke",
}
ORDER_NOW = {
    "order_NOW": "Complete"
}

def get_token(client):
    result = client.post('/api/v1/auth/signup',content_type="application/json",data=json.dumps(token_user))
    if result.status_code != 201:
        raise Exception("failed to signup user")
    result = client.post('/api/v1/auth/login',content_type="application/json",data=json.dumps(token_user))
    if result.status_code != 200:
        raise Exception("failed to login user")
    response = json.loads(result.data.decode())
    # print(response ['access_token'])
    return response ['access_token']

def post_auth_header(client):
    token = get_token(client)
    return{
        "authorization": "Bearer {}".format(token) 
    }

def get_auth_header(client):
    token = get_token(client)
    return{
        'Content_type':"application/json",
        "token": token
    }
   