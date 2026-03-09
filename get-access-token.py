import fitbit
import gather_keys_oauth2 as Oauth2

# Put in your own client ID and secret
CLIENT_ID = '23TSL5'
CLIENT_SECRET = '074c2ac63f4aec53ca7a5f331ce767a1'

server=Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()

ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
print("Access token: ", ACCESS_TOKEN)
print("Refresh token: ", REFRESH_TOKEN)

auth2_client=fitbit.Fitbit(CLIENT_ID,
                           CLIENT_SECRET,
                           oauth2 = True,
                           access_token = ACCESS_TOKEN,
                           refresh_token = REFRESH_TOKEN)
