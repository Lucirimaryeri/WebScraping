import json
import requests
from twilio.rest import Client
import keys
client = Client(keys.accountSID, keys.authToken)
TwilioNumber = "+18333631874" 
myCellPhone = "+19568003101"

def fetch_cryptocurrency_data(api_key):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '5',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    response = requests.get(url, headers=headers, params=parameters)
    
    if response.status_code == 200:
        data = response.json()
        return data['data']
    else:
        print(f"Error: {response.status_code}")
        return None

print()
# display ---------------------------------------------------------------------------------------
def display_cryptocurrency_info(crypto):
    name = crypto['name']
    symbol = crypto['symbol']
    price = crypto['quote']['USD']['price']
    percent_change_24h = crypto['quote']['USD']['percent_change_24h']
    change_price = price * (1 + percent_change_24h / 100)

    formatted_price = "${:,.2f}".format(price)
    formatted_change_price = "${:,.2f}".format(change_price)
    print()
    print(f"Name: {name}")
    print(f"Symbol: {symbol}")
    print(f"Current Price: {formatted_price}")
    print(f"% Change (24h): {percent_change_24h:.2f}%")
    print(f"Corresponding Price (based on % change): {formatted_change_price}")
    print("\n")

#Ethereum alert ---------------------------------------------------------------------------------
    if name == "Ethereum" and price > 2000:
        print(f"Alert: Ethereum value is above $2,000. Consider selling!")
        msg = 'Ethereum value is above $2,000. Consider selling!'
        
        #send text message
        txtmsg = client.messages.create(to=myCellPhone,from_=TwilioNumber,body=msg)

#------------------------------------------------------------------------------------------------
#API
print()
if __name__ == "__main__":
    api_key = "c80820fb-1174-4f71-9bf4-489a5587a4e5"

    data = fetch_cryptocurrency_data(api_key)

    if data:
        for crypto in data:
            display_cryptocurrency_info(crypto)
    else:
        print("Cannot fetch cryptocurrency data at this moment")
