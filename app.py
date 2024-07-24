import requests

class SECEdgar:
    def __init__(self, urlfile):
        self.urlfile = urlfile ## URLs that contain the data
        self.dictname = {} ## Company names
        self.tickerdict = {} ## Stock Ticker
        self.headers = {'user-agent': 'MLT CP salahm2130@gmail.com'}
        req = requests.get(self.urlfile, headers=self.headers)
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
    
    def findFillings(self, cik): ## Finding through the submission files with JSON dictionaries 
        url = f"https://data.sec.gov/submissions/CIK{cik.zfill(10)}.json"
        reqUrl = requests.get(url, headers=self.headers)
        print(reqUrl.status_code)
        if reqUrl.status_code == 200:
            reqUrlJSON = reqUrl.json()
            return reqUrlJSON
        else:
            return None
    
    def annual_filing(self, cik, year): 
        totalFilings = self.findFillings(cik)
        if totalFilings:
            regFilings = totalFilings['filings']['recent']
            fileDate = regFilings['filingDate'] ## Year of Document File 
            accessionNum = regFilings['accessionNumber'] ## Accession Number
            primaryDoc = regFilings['primaryDocument'] ## Name of the Document
            primaryDocDescript = regFilings['primaryDocDescription'] ## Description of Doc (10-K or 10-Q)
            for i in range(len(fileDate)):
                filingYear = fileDate[i] 
                accessNum = accessionNum[i]
                primDocYear = primaryDoc[i] 
                primDocDes = primaryDocDescript[i]
                if filingYear.startswith(year) and '10-K' in primDocDes: ## If it matches given year and Annual Filing Document
                    doc_url = f"https://www.sec.gov/Archives/edgar/data/{cik.zfill(10)}/{accessNum.replace('-','')}/{primDocYear}" ## Document Specific to Company depending on yearly or quarterly.
                    reqDoc = requests.get(doc_url, headers=self.headers)
                    return reqDoc.content
    
    def quarterly_filing(self, cik, year, quarter):
        totalFilings = self.findFillings(cik)
        if totalFilings:
            regFilings = totalFilings['filings']['recent']
            fileDate = regFilings['filingDate'] ## Year of Document File 
            accessionNum = regFilings['accessionNumber'] ## Accession Number
            primaryDoc = regFilings['primaryDocument'] ## Name of the Document
            primaryDocDescript = regFilings['primaryDocDescription'] ## Description of Doc (10-K or 10-Q)
            quarter_Yr = {1: ('01', '02', '03'), 2: ('04', '05', '06'), 3: ('07', '08', '09'), 4: ('10', '11', '12')} ## Representation of Months in quarter of yr categories.
            for i in range(len(fileDate)):
                filingYear = fileDate[i] 
                filingMonth = fileDate[i].split('-')[1]
                accessNum = accessionNum[i]
                primDocYear = primaryDoc[i] 
                primDocDes = primaryDocDescript[i]
                if filingYear.startswith(year) and '10-Q' in primDocDes and filingMonth in quarter_Yr[quarter]:
                    doc_url = f"https://www.sec.gov/Archives/edgar/data/{cik.zfill(10)}/{accessNum.replace('-','')}/{primDocYear}" ## Document Specific to Company depending on yearly or quarterly.
                    reqDoc = requests.get(doc_url, headers=self.headers)
                    return reqDoc.content
                

            
                
                
            
                   
       
    
    
        
        
        

            
            
        
    
        

x = SECEdgar('https://www.sec.gov/files/company_tickers.json')  
print(x.quarterly_filing('320193', '2023', 2))     
