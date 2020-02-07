# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 01:46:38 2017

@author: optimusqp
https://habr.com/ru/post/332700/
"""
import urllib



def quotes(code,year_start,month_start,day_start,year_end,month_end,day_end,e,market,em,df,mf,yf,dt,mt,yt,p,dtf,tmf,MSOR,mstimever,sep,sep2,datf,at):
    
    page = urllib.urlopen('http://export.finam.ru/'+str(code)+'_'+str(year_start)+str(month_start)+str(day_start)+'_'+str(year_end)+str(month_end)+str(day_end)+str(e)+'?market='+str(market)+'&em='+str(em)+'&code='+str(code)+'&apply=0&df='+str(df)+'&mf='+str(mf)+'&yf='+str(yf)+'&from='+str(day_start)+'.'+str(month_start)+'.'+str(yf)+'&dt='+str(dt)+'&mt='+str(mt)+'&yt='+str(yt)+'&to='+str(day_end)+'.'+str(month_end)+'.'+str(yt)+'&p='+str(p)+'&f='+str(code)+'_'+str(year_start)+str(month_start)+str(day_start)+'_'+str(year_end)+str(month_end)+str(day_end)+'&e='+str(e)+'&cn='+str(code)+'&dtf='+str(dtf)+'&tmf='+str(tmf)+'&MSOR='+str(MSOR)+'&mstimever='+str(mstimever)+'&sep='+str(sep)+'&sep2='+str(sep2)+'&datf='+str(datf)+'&at='+str(at))
    f = open("company_quotes.txt", "w")
    content = page.read()
    f.write(content)
    f.close()

def getLastYearQuotes(name, quoteId):
    code='NOK';
    e='.txt';
    market='1'
    em='874609';
    e='.txt';
    p='8';
    yf='2019';
    yt='2020';
    month_start='02';
    day_start='07';
    month_end='02';
    day_end='07';
    dtf='1';
    tmf='1';
    MSOR='1';
    mstimever='0'
    sep='1';
    sep2='3';
    datf='1';
    at='1';

    year_start=yf[2:];
    year_end=yt[2:];
    mf=(int(month_start.replace('0','')))-1;
    mt=(int(month_end.replace('0','')))-1;
    df=(int(day_start.replace('0','')))-1;
    dt=(int(day_end.replace('0','')))-1;

    qq = quotes(code,year_start,month_start,day_start,year_end,month_end,day_end,e,market,em,df,mf,yf,dt,mt,yt,p,dtf,tmf,MSOR,mstimever,sep,sep2,datf,at)
