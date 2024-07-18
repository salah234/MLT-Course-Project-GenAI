import requests

class SECEdgar:
    def __init__(self, urlfile):
        self.urlfile = urlfile ## URLs that contain the data
        self.dictname = {} ## Company names
        self.tickerdict = {} ## Stock Ticker
        
        headers = {'user-agent': 'MLT CP salahm2130@gmail.com'}
        req = requests.get(self.urlfile, headers=headers)
        if req.status_code == 200: # If fetching data was successful
            reqjson = req.json() # In JSON format since web written in JavaScript.
            for k, v in reqjson.items():
                if 'cik_str' in v and 'ticker' in v and 'title' in v:
                    cik = v['cik_str']
                    ticker = v['ticker']
                    cmpny_name = v['title']
                    
                    if cmpny_name and cik and ticker: ## If we have those three, store into dicts
                            self.dictname[cmpny_name] = (cik, ticker)
                            self.tickerdict[ticker] = (cik, cmpny_name)
          
    def name_to_cik(self, cmpny_name): ## Lookup by Company Name
        if cmpny_name in self.dictname:
            cik, ticker = self.dictname[cmpny_name]
            return cik, ticker, cmpny_name
    def ticker_to_cik(self, ticker):
        if ticker in self.tickerdict: ## Check our Ticker Dictonary
            cik, cmpny_name = self.tickerdict[ticker]
            return cik, ticker, cmpny_name
        
        

            
            
        
    
        

x = SECEdgar('https://www.sec.gov/files/company_tickers.json')  
print(x.ticker_to_cik("AMGN"))     
