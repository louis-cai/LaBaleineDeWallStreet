import requests
import json
import getopt
import discord
import math
import time
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, show
from bokeh.models import LinearAxis, Range1d, PrintfTickFormatter
from bokeh.io import export_png
import pandas as pd
import os
import numpy as np

client = discord.Client()

token = os.environ["DISCORD_TOKEN"]

verif = 0
plt.style.use('ggplot')

aa="\n"
a="\n"+"Quelques règles du discord de la baleine :"+"\n"

b="- Pas de pubs sans une autorisation des admins"+"\n"
c="- Courtoisie et savoir-vivre"+"\n"
d="- Les calls **SANS ARGUMENT** seront suivis par un avertissement et ensuite un bannissement"+"\n"
e="- Pensez aux gens qui vont lire et mettez-vous à leur place"+"\n"
f="- Le flood et le troll sont interdits"+"\n"
g="- Les commandes de prix, conv etc du bot sont uniquement autorisé dans le chan #bot"+"\n"
h="- Les liens de parrainage sont interdits" +"\n"+"\n"+"\n"


i="Commande du bot :"+"\n"+"\n"

j="\t"+"BaleineDeWallStreet :"+"\n"
k="\t"+"prix -> price (market) coin"+"\n"
l="\t"+"conversion -> conv unité coin"+"\n"
m="\t"+"graph -> chart coin"+"\n"
n="\t"+"order book -> book coin"+"\n"+"\n"

o="Lexique :"+"\n"+"\n"
p="\t"+"!helpList "+"\n"
q="\t"+"!help Recherche"+"\n"

rule=aa+a+b+c+d+e+f+g+h+i+j+k+l+m+n+o+p+q

class switch(object):

    value = None
    def __new__(class_, value):
        class_.value = value
        return True

def case(*args):
    return any((arg == switch.value for arg in args))


def calc(boo):

    boo=boo.replace('os.','')
    boo=boo.split()
    boo=boo.remove("calc")
    print(boo)
    return("")  #eval(boo[0])


def traitement(boo): #ICI

    d = 0
    boo = boo.lower()
    print(boo)
    print("Contrôle mot 1")
    if(len(boo.split())>1):
        while switch((boo.split()[0]).lower()):
            if case('prix'):
                d = price(boo.split())
                break
            if case('price'):
                d = price(boo.split())
                break
            if case('conv'):
                d = conv(boo.split())
                break
            if case('volume'):
                print("soon")
                break
            if case('chart'):
                d = chart(boo.split()[1])
                break
            if case('book'):
                d = book(boo.split()[1])
                break
            break

    return d

def price(boo2):

    print("Choix du market")

    if(len(boo2)>=2):
        while switch(boo2[1]):
            if case('polo'):            #polo
                boo2.remove("polo")
                t = poloniex(boo2)
                break
            if case('trex'):            #trex
                boo2.remove("trex")
                t = bittrex(boo2)
                break
            if case('poloniex'):        #polo
                boo2.remove("poloniex")
                t = poloniex(boo2)
                break
            if case('bittrex'):         #trex
                boo2.remove("bittrex")
                t = bittrex(boo2)
                break
            if case('p'):           #polo
                boo2.remove("p")
                t = poloniex(boo2)

                break
            if case('b'):               #trex
                boo2.remove("b")
                t = bittrex(boo2)
                break
            t = lost(boo2)                    # Si market pas indiqué
            break

    return t

def conv(boo2):

    print("CONV")

    print(boo2)
    boo2.remove("conv")

    print(boo2)

    valBtc = btcrecup(0)
    valBtcE = btcrecup(1)
    print(valBtcE)
    print(valBtc)
    try:  #si le nombre + la devise
        float(boo2[0])
        final=polorecup(boo2[1],0)

        if(boo2[1].upper()=="BTC"):
            final=float(valBtc)*float(boo2[0])
            final2=float(valBtcE)*float(boo2[0])
            return ("```"+str(boo2[0])+" "+str(boo2[1]).upper()+" valent "+ str("%.2f" %final)+"$ ou "+str("%.2f" %final2)+"€```")

        if(final==0):
            final=bittrecup(boo2[1],0)
        if(final!=0):
            final2=(float(valBtcE)*(float(final)/float(valBtc)))*float(boo2[0])
            final=float(final)*float(boo2[0])
            final = "```"+str(boo2[0])+" "+str(boo2[1]).upper()+" valent "+ str("%.2f" %final)+"$ ou "+str("%.2f" %final2)+"€  ("+str("%.4f" %(final/valBtc))+"฿)```"

    except : #si la devise + le nombre
        try:
            float(boo2[1])
        except:
            boo2[1]=0

        if(boo2[0].upper()=="BTC"):
            final=float(valBtc)*float(boo2[1])
            final2=float(valBtcE)*float(boo2[1])
            print(1)
            return ("```"+str(boo2[1])+" "+str(boo2[0]).upper()+" valent "+ str("%.2f" %final)+"$ ou "+str("%.2f" %final2)+"€```")

        final=polorecup(boo2[0],0)
        if(final==0):
            final=bittrecup(boo2[0],0)

        if(final!=0):
            final2=(float(valBtcE)*(float(final)/float(valBtc)))*float(boo2[1])
            final=float(final)*float(boo2[1])
            final ="```"+str(boo2[1])+" "+str(boo2[0]).upper()+" valent "+  str("%.2f" %final)+"$ ou "+str("%.2f" %final2)+"€  ("+str("%.4f" %(final/valBtc))+"฿)```"

    return final



def bittrex(boo3):

    print("Trex Selector")

    i = 0
    final = ["","","","","",""]
    boo3.remove("price")

    nbreCase = len(boo3)

    offset = 0

    while nbreCase > i :

        final[offset]=bittrecup(boo3[i],1)

        if(final[offset]!=0):
            offset+=1

        i = 1 + i

    return final

def poloniex(boo3):

    print("Polo Selector")

    i = 0
    final = ["","","","","","","","","","","","","","","",""]

    boo3.remove("price")


    nbreCase = len(boo3)

    offset=0

    while nbreCase > i :

        final[offset]=polorecup(boo3[i],1)

        if(final[offset]!=0):
            offset+=1

        i = 1 + i
    return final

def lost(boo3):

    print("Mot 2 inconnu")

    i = 0
    final = ["","","","","","","","","","","","","","","",""]
    boo3.remove("price")

    nbreCase = len(boo3)



    while nbreCase > i :

        final[i]=polorecup(boo3[i],1)

        if(final[i]==0):
            final[i]=bittrecup(boo3[i],1)

        i = 1 + i


    return final

def polorecup(boo4,all):

    market="BTC_"+boo4.upper()

    valBtc = btcrecup(0)
    valBtcE = btcrecup(1)

    if(market=="BTC_BTC"):
        value = "```1 BTC vaut "+str(valBtc)+"$"+" ou "+str(valBtcE)+"€```"
        return(value)

    url="https://poloniex.com/public?command=returnTicker"
    print("Poloniex Récup")

    content=requests.get(url)
    data=content.json()



    print(market)

    if(market in data):
        if(all):
            return("```"+boo4.upper()+"   "+data[market]["last"]+"฿ ("+str("%.2f" %(float(data[market]["percentChange"])*100))+"%) $"+(str("%.5f" %(float(data[market]["last"])*(float(valBtc)))))+" (Poloniex)"+"```")
        else:
            return(float(data[market]["last"])*valBtc)
    else:
        return 0





def bittrecup(boo4,all):

    print("Bittrex Recup")

    url="https://bittrex.com/api/v1.1/public/getmarketsummary?market="
    valBtc = btcrecup(0)
    market="btc-"+boo4
    print(market)
    content=requests.get(url+market)
    data=content.json()

    print(data["success"])

    if(data["success"]):

        if(all):
            print("all")
            percent1=((data["result"][0]["Last"])-(data["result"][0]["PrevDay"]))
            percent2=(percent1/float(data["result"][0]["PrevDay"]))*100



            return("```"+boo4.upper()+"   "+str(data["result"][0]["Last"])+"฿ ("+str("%.2f" %percent2)+"%) $"+str("%.5f" %(data["result"][0]["Last"]*float(valBtc)))+"  (Bittrex)"+"```")
        else:
            return(data["result"][0]["Last"]*valBtc)
    else:
        return 0

def btcrecup(euro):

    print("Bitcoin Recup")

    if(euro):
        url="https://www.bitstamp.net/api/v2/ticker/btceur/"
    else:
        url="https://www.bitstamp.net/api/v2/ticker/btcusd/"

    content=requests.get(url)
    data=content.json()
    if( "last" in data):
        return (float(data["last"]))

    else:
        return(0)


def renvoie(boo5):

    print("Fonction de renvoie")
    client = discord.Client()
    boucle = len(boo5)

    i=0

    print(boo5[:])
    while boucle > i :

        i += 1

def ema(df, n):
    price = df['close']
    price.fillna(method='ffill', inplace=True)
    price.fillna(method='bfill', inplace=True)
    ema = pd.Series(price.ewm(span=n, min_periods=n - 1).mean(), name='EMA_' + str(n))
    df = df.join(ema)
    return df

def draw_chart(df, params):
    # Computing indicators before triming data
    for i in params["indicators"]:
        if i['name'] is "ema":
            df = ema(df, i['period'])
    df = df.tail(48)
    p = figure(x_axis_type='datetime', plot_width=chart_params['size']['width'],
               plot_height=chart_params['size']['height'], title=chart_params['title'])
    # Visual ajustments
    p.toolbar.logo = None
    p.toolbar_location = None
    p.background_fill_color = "#e5e5e5"
    p.grid.grid_line_color = "white"
    p.grid.minor_grid_line_color = "white"
    p.grid.minor_grid_line_alpha = 0.3
    p.y_range = Range1d(df['low'].min() * 0.995, df['high'].max() * 1.003)
    p.extra_y_ranges = {"foo": Range1d(start=-0, end=3 * df['volume'].max())}
    p.yaxis[0].formatter = PrintfTickFormatter(format="%1.8f")
    # Adding second axis for volume to the plot.
    p.add_layout(LinearAxis(y_range_name="foo"), 'right')
    p.grid[0].ticker.desired_num_ticks = 10
    p.yaxis[1].ticker.desired_num_ticks = 5
    p.xaxis.major_label_text_font_size = "10pt"
    p.yaxis[0].major_label_text_font_size = "10pt"
    p.yaxis[1].bounds = (0, df['volume'].max())
    inc = df['close'] > df['open']
    dec = df['open'] >= df['close']
    half_day_in_ms_width = 20 * 60 * 1000
    # candlesticks
    p.segment(df['date'], df['high'], df['date'], df['low'], color="black")
    p.vbar(df.date[inc], half_day_in_ms_width, df.open[inc], df.close[inc], fill_color="green", line_color="black")
    # volume
    p.vbar(df.date[dec], half_day_in_ms_width, df.open[dec], df.close[dec], fill_color="red", line_color="black")
    p.vbar(df.date[inc], half_day_in_ms_width, 0, df.volume[inc], fill_color="green", line_color="black",
           y_range_name="foo", alpha=0.3)
    p.vbar(df.date[dec], half_day_in_ms_width, 0, df.volume[dec], fill_color="red", line_color="black",
           y_range_name="foo", alpha=0.3)
    for i in params["indicators"]:
        if i['name'] is "ema":
            p.line(df['date'], df['EMA_' + str(i['period'])], line_dash=(4, 4), color=i['color'],
                   legend='EMA ' + str(i['period']), line_width=2)

    p.legend.location = "top_left"
    return p

chart_params = {
        "title": "",
        "colors": {"up": "Green", "down": "Red"},
        "size": {"height": 500, "width": 750},
        "indicators": [
          {"name": "ema", "period": 12, "color": "blue"},
          {"name": "ema", "period": 26, "color": "black"}
          # Need ajustement in api call if period is greater
        ]
}


def chart(strcur):

    cur = strcur.upper()
    end = round(time.time())
    # 48 hours of data, 30 min periods
    start = end - 2 * 86400
    if cur in ('BTC','XBT'):
        chart_params['title']="KRAKEN USD-BTC"
        url = "https://api.kraken.com/0/public/OHLC?pair=XBTUSD&interval=30&since="+str(start)
        content = requests.get(url)
        data = content.json()
        df = pd.DataFrame.from_dict(data['result']['XXBTZUSD'])
        df.rename(columns={0: 'date', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'vwap', 6: 'volume', 7: 'count'},
                  inplace=True)
        df['date'] = pd.to_datetime(df['date'], unit='s')
        df['volume'] = df['volume'].astype(float)
        df['low'] = df['low'].astype(float)
        df['high'] = df['high'].astype(float)
    else:
        url = "https://poloniex.com/public?command=returnChartData&currencyPair=BTC_"+cur+"&start="+str(start)+"&end="+str(end)+"&period=1800"
        content = requests.get(url)
        data = content.json()
        if ('error') in data:
            url = "https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName=BTC-"+cur+"&tickInterval=thirtyMin&_="+str(end)
            content = requests.get(url)
            data = content.json()
            if not data['success']:
                print("error")
                return ""
            chart_params['title']="BITTREX BTC-" + cur
            df = pd.DataFrame.from_dict(data['result'])
            df.rename(columns={'C': 'close', 'H': 'high', 'L': 'low', 'O': 'open', 'T': 'date', 'V': 'volume'},
                      inplace=True)
            df['volume'] = df['volume'] * df['close']
            df['date'] = pd.to_datetime(df['date'])
            df = df.tail(80)

        else:
            chart_params['title']="POLONIEX BTC-" + cur
            df = pd.DataFrame.from_dict(data)
            df['date'] = pd.to_datetime(df['date'], unit='s')

    p = draw_chart(df, chart_params)
    export_png(p, filename=cur + "_chart.png")
    return cur + "_chart.png"

def book(strcur):

    cur = strcur.upper()
    # reduce depth variable for a more focused visualization around center
    url = "https://poloniex.com/public?command=returnOrderBook&currencyPair=BTC_" + cur + "&depth=50"
    content = requests.get(url)
    data = content.json()
    if ('error') in data:
        url = "https://bittrex.com/api/v1.1/public/getorderbook?market=BTC-"+cur+"&type=both&depth=100"
        content = requests.get(url)
        data = content.json()
        if not data['success']:
            print("error")
            return ""
        data = data['result']
        df_asks = pd.DataFrame.from_dict(data['sell'])
        df_asks.rename(columns={'Rate': 'price', 'Quantity': 'ask'}, inplace=True)
        df_bids = pd.DataFrame.from_dict(data['buy'])
        df_bids.rename(columns={'Rate': 'price', 'Quantity': 'bid'}, inplace=True)
        # Cuz bittrex is shit
        df_bids = df_bids.head(100)
        df_asks = df_asks.head(100)

    else:
        df_asks = pd.DataFrame.from_dict(data['asks'])
        df_asks.rename(columns={0: 'price', 1: 'ask'}, inplace=True)
        df_bids = pd.DataFrame.from_dict(data['bids'])
        df_bids.rename(columns={0: 'price', 1: 'bid'}, inplace=True)

    df_asks['ask'] = df_asks['ask']*df_asks['price'].astype(float)
    df_bids['bid'] = df_bids['bid']*df_bids['price'].astype(float)
    df_asks.set_index(['price'], inplace=True)
    df_bids.set_index('price', inplace=True)
    df_asks = df_asks.cumsum()
    df_bids = df_bids.cumsum()
    df_asks = df_asks.join(df_bids, how='outer')

    # better visualization
    fig, ax = plt.subplots()
    if df_asks['ask'].max() > df_asks['bid'].max():
        df_asks['ask'].plot(ax=ax, color='r', kind='area', alpha=0.6)
        df_asks['bid'].plot(ax=ax, color='g', kind='area', alpha=0.6)
    else:
        df_asks['bid'].plot(ax=ax, color='g', kind='area', alpha=0.6)
        df_asks['ask'].plot(ax=ax, color='r', kind='area', alpha=0.6)
    ax.set_xlabel('')
    plt.setp(ax.get_xticklabels(), rotation=-30, horizontalalignment='left')
    plt.tight_layout()


    fig.savefig(cur + "_book.png")
    return cur + "_book.png"



@client.event
async def on_message(message):
    if message.content.startswith(('price', 'Price', 'prix', 'Prix', 'conv', 'Conv', 'chart', 'Chart', 'book', 'Book')):
        if str(message.channel) != "bot":
            roles = [i.name for i in message.author.roles]
            if 'Baleine novice' in roles:
                await client.send_message(message.author, "Es-tu sûr de respecter les règles d'utilisation du bot ? ;)")

    if message.content.startswith(('price','Price','prix','Prix')):
        await client.send_typing(message.channel)
        retour=traitement(message.content)
        print("retour ok")

        boucle = len(retour)

        i=0

        print(retour[0])
        print(retour[1])


        while boucle > i :

            if(retour[i]!=""):
                await client.send_message(message.channel, retour[i])

            i += 1

    if message.content.startswith(('conv','Conv')):
        await client.send_typing(message.channel)
        retour=traitement(message.content)
        print(retour)

        if(retour!=0):
            await client.send_message(message.channel, retour)

    if message.content.startswith(('calc','Calc')):

        retour=calc(message.content)

        await client.send_message(message.channel,"```"+ ((message.content).split())[1]+ " = " + str("%.2f" %retour)+"```")

    if message.content.startswith(('chart','Chart')):
        # https: // poloniex.com / public?command = returnChartData & currencyPair = BTC_XMR & start = 1405699200 & end = 9999999999 & period = 14400
        await client.send_typing(message.channel)
        retour = traitement(message.content)
        if (retour!=""):
            await client.send_file(message.channel,retour )
            os.remove(retour)
        # await client.send_message(message.channel, chart('etc'))

    if message.content.startswith(('book', 'Book')):
        await client.send_typing(message.channel)
        retour = traitement(message.content)
        if (retour!=""):
            await client.send_file(message.channel,retour )
            os.remove(retour)

    if message.content.startswith(('/rules', '!rules', 'rule', '!règles', 'rules', 'Rules')):

        print(message.content)

        await client.send_message(message.author, rule)




@client.event
async def on_ready():

    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    verif=1


client.run(token)
