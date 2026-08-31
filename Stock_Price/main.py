    import requests
    from config import *
    from datetime import datetime, timedelta
    import smtplib
    azi_date = datetime.now()
    ieri_date = azi_date - timedelta(days=1)
    azi_str: str= azi_date.strftime('%Y-%m-%d')
    ieri_str: str= ieri_date.strftime('%Y-%m-%d')
    maxim_value_gain: float = 1.1
    maxim_value_loss: float = 0.9

    response_price=requests.get(stock_end_point,params=param_stock_price)
    response_price.raise_for_status()
    data=response_price.json()
    time_se=data.get("Time Series (Daily)",{})
    response_news=requests.get(stock_news_endpoint,params=param_stock_news)
    response_news.raise_for_status()
    data_news=response_news.json()
    zile_disponibile = list(time_se.keys())
    articole_relevante=[]
    for i in data_news.get("articles",[]):
        titlu=i.get("title",[])
        if "apple" in titlu.lower():
            articole_relevante.append(titlu)
        if len(articole_relevante)==3:
            break
    if len(zile_disponibile) >= 2:
        azi_str: str= zile_disponibile[0]
        ieri_str:str= zile_disponibile[1]
        if azi_str in time_se and ieri_str in time_se:
            today_close_value: float=float(time_se[azi_str]["4. close"])
            yesterday_close_value:float=float(time_se[ieri_str]["4. close"])
            if today_close_value >maxim_value_gain * yesterday_close_value:
                procent_crestere: int=round( ((today_close_value - yesterday_close_value)/ yesterday_close_value) *100,2)
                with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                    connection.starttls()
                    connection.login(user=my_email, password=password)
                    for i in range(len(articole_relevante)):
                        email_body = f"Subject:Stocks\n\n{symbol} a crescut cu: :🔺{procent_crestere} din cauza {articole_relevante[i]}"
                        connection.sendmail(from_addr=my_email, to_addrs="dimarobert7788@gmail.com", msg=email_body.encode("utf8"))
            elif today_close_value<maxim_value_loss * yesterday_close_value:
                with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                    procent_crestere: int = ((today_close_value - yesterday_close_value) / yesterday_close_value) * 100
                    connection.starttls()
                    connection.login(user=my_email, password=password)
                    for i in range(len(articole_relevante)):
                        email_body = f"Subject:Stocks\n\n{symbol} a scazut cu: :🔻{procent_crestere} din cauza {articole_relevante[i]}"
                        connection.sendmail(from_addr=my_email, to_addrs="dimarobert7788@gmail.com", msg=email_body.encode("utf8"))

