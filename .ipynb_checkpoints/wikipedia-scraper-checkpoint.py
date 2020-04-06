import json, sqlite3
import requests
from selenium import webdriver

con = sqlite3.connect("healthcare.db")
cur = con.cursor()
cur.execute("DROP TABLE doencas_wiki;") # use your column names here
cur.execute("CREATE TABLE doencas_wiki (cid varchar, content varchar, cite varchar);") # use your column names here

def wikiScrap(cid10, term):    
    
    #browser.get("https://pt.wikipedia.org/wiki/Shigelose")
    browser.get("https://pt.wikipedia.org/w/index.php?sort=relevance&search=" + term + "&title=Especial:Pesquisar&profile=advanced&fulltext=1&advancedSearch-current=%7B%7D&ns0=1&searchengineselect=mediawiki")
    
    input("Press Enter to continue...")
    
    r = browser.find_elements_by_class_name("searchmatch")[0].click()
    
    if(not browser.find_element_by_id("firstHeading").text.startswith("CID-10")):
        results = browser.find_elements_by_css_selector("p, h2 > span.mw-headline, span.reference-text > cite")    

        cite = ''    
        text = ''
        for result in results:
            if result.tag_name == 'span':
                text = text + '# ' + result.text
            if result.tag_name == 'p':
                text = text + result.text    
            if result.tag_name == 'cite':
                cite = cite + result.text                

        cur.execute("INSERT INTO doencas_wiki (cid,content,cite) VALUES (?,?,?);", [cid10, text, cite])
        #print(cur.execute("select * from doencas_wiki").fetchall())
        con.commit()
    
options1 = webdriver.ChromeOptions()
options1.add_argument("window-size=1024x768")
browser = webdriver.Chrome(executable_path='./chromedriver.exe', port=9515, options=options1)


response = requests.get('https://agile-woodland-05541.herokuapp.com/doencas',  stream=True)
for r in response.json():
    cid = r['cid']
    disease = r['description']    
    wikiScrap(cid,disease)
    
browser.close()
con.close()