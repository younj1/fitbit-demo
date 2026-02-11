import fitbit
import gather_keys_oauth2 as Oauth2

# Put in your own client ID and secret
CLIENT_ID = '23TSL5'
CLIENT_SECRET = '074c2ac63f4aec53ca7a5f331ce767a1'

server=Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()

ACCESS_TOKEN = str(server.fitbit.client.session.token['eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyM1RTTDUiLCJzdWIiOiJDWlBLSFMiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNzcwMDkwMzg2LCJpYXQiOjE3NzAwNjE1ODZ9.avW20KNGNcquQ-F5e5Gz3YPEB2-j0A-o__glvl45hxQ'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['fbe85e39d9d3c0d9c7f2a59a183390971ee8e06699177d25b0add55fb98fd271'])
print("Access token: ", ACCESS_TOKEN)
print("Refresh token: ", REFRESH_TOKEN)

auth2_client=fitbit.Fitbit(CLIENT_ID,
                           CLIENT_SECRET,
                           oauth2 = True,
                           access_token = ACCESS_TOKEN,
                           refresh_token = REFRESH_TOKEN)
