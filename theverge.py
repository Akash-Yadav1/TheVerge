from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import time

class TheVerge():
    browser=webdriver.Chrome(executable_path='Chromedriver\\chromedriver.exe')
    browser.get('https://www.theverge.com/')

    time.sleep(5)#time required to load the page
    html=browser.page_source
    browser.close()

    global soup
    soup = BeautifulSoup(html,'html.parser')


    def pandacr(self,headlinelink,headline,authorsl,datesl):
        #Creating the dataframes for smooth working
        authorsdf= pd.DataFrame(authorsl) 
        datesdf= pd.DataFrame(datesl)        
        headlinedf=pd.DataFrame(headline)        
        headlinelinkdf=pd.DataFrame(headlinelink)    
        pg=pd.concat([headlinedf,headlinelinkdf,authorsdf,datesdf],axis=1)
        pg.columns=['Headline',"Link","Author","Dates"]
        compactol=soup.find(class_="styled-counter w-full lg:mt-20 lg:w-[320px] styled-counter-compact")
        df=pd.DataFrame()
        for i in compactol:
            df1= pd.DataFrame({'1':i.a.text,"2":"https://www.theverge.com/"+i.a['href'],"3":i.p.span.text,"4":i.p.find(class_='mr-8 font-light text-gray-ef').text},index=range(1))
            df= pd.concat([df,df1],axis=0)
        df.columns=['Headline',"Link","Author","Dates"]
        pg=pd.concat([pg,df],axis=0)
        pg.index=range(len(pg))
        pg.index.name="id"
        pg.drop_duplicates(keep='first')
        pg.to_csv('theverge.csv')
        return self.sqlcr(pg)
        
    def sqlcr(self,pg):
        #SQL lite creation
        sql=sqlite3.connect('theverge.db')
        pg.to_sql(name="theverge",con=sql,if_exists="replace",index=False)
        sql.commit()
        return "work done"

    
    def listcr(self,csslist,headlinelink,headline,authorsl,datesl):
        for css in csslist:
            tcells=soup.find_all(class_=css)
            for i in tcells:
                try:
                    authorsl.append(i.find('a',class_='text-gray-31 hover:shadow-underline-inherit dark:text-franklin mr-8').text)
                    headline.append(i.h2.a.text)
                    headlinelink.append("https://www.theverge.com/"+i.h2.a["href"])
                    datesl.append(i.find("span",class_="text-gray-63 dark:text-gray-94").text)
                except:
                    continue
        return self.pandacr(headlinelink,headline,authorsl,datesl)
if __name__=='__main__':
    headlinelink=[]
    headline=[]
    authorsl=[]
    datesl=[]
    a=TheVerge()
    print(a.listcr(['relative border-b border-gray-31 pb-20 md:pl-80 lg:border-none lg:pl-[165px] -mt-20 sm:-mt-40',"max-w-content-block-standard md:w-content-block-compact md:max-w-content-block-compact lg:w-[240px] lg:max-w-[240px] lg:pr-10","max-w-content-block-standard md:w-content-block-compact md:max-w-content-block-compact lg:w-[240px] lg:max-w-[240px] lg:pr-10","max-w-content-block-mobile sm:w-content-block-compact sm:max-w-content-block-compact"],headlinelink,headline,authorsl,datesl))
