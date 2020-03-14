import json, sqlite3
from selenium import webdriver

con = sqlite3.connect("healthcare.db")
cur = con.cursor()
cur.execute("DROP TABLE doencas;") # use your column names here
cur.execute("CREATE TABLE doencas (cid varchar, description varchar);") # use your column names here

options1 = webdriver.ChromeOptions()
options1.add_argument("window-size=1920x1080")

browser = webdriver.Chrome(executable_path='C:/chromedriver_win32/chromedriver.exe', port=9515, options=options1)
browser.get("http://www.medicinanet.com.br/categorias/lista_cid10.htm")
results = browser.find_elements_by_css_selector("div#texto > ul > li > div > a")

for result in results:
    doenca = result.text.strip().split(' - ')
    cur.execute("INSERT INTO doencas (cid,description) VALUES (?,?);", [doenca[0], doenca[1]])

browser.close()

print(cur.execute("select * from doencas").fetchall())

con.commit()
con.close()


