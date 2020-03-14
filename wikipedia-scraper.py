import json, sqlite3
from selenium import webdriver

con = sqlite3.connect("healthcare.db")
cur = con.cursor()
cur.execute("DROP TABLE doencas_wiki;") # use your column names here
cur.execute("CREATE TABLE doencas_wiki (cid varchar, content varchar, cite varchar);") # use your column names here

options1 = webdriver.ChromeOptions()
options1.add_argument("window-size=1920x1080")

browser = webdriver.Chrome(executable_path='C:/chromedriver_win32/chromedriver.exe', port=9515, options=options1)
browser.get("https://pt.wikipedia.org/wiki/Shigelose")
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
    

cur.execute("INSERT INTO doencas_wiki (cid,content,cite) VALUES ('A03',?,?);", [text, cite])

browser.close()

print(cur.execute("select * from doencas_wiki").fetchall())

con.commit()
con.close()