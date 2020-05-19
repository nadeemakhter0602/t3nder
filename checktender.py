from datetime import datetime
import re
import os
import cv2
import requests
import re
import base64
from PIL import Image
from bs4 import BeautifulSoup
import numpy as np
now=datetime.now()
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

s=requests.session()
response=s.get('https://wbtenders.gov.in/nicgep/app',headers=headers)
cookies=response.cookies.get_dict()
params = (
    ('page', 'FrontEndAdvancedSearch'),
    ('service', 'page'),
)
response1 = s.get('https://wbtenders.gov.in/nicgep/app;jsessionid='+str(cookies['JSESSIONID']), headers=headers, params=params, cookies=cookies)
soup=BeautifulSoup(response1.content,features='html.parser')
image=soup.find('img',{'name':'captchaImage'})['src']
image=image.replace('data:image/png;base64,',"")
imgdata=base64.b64decode(image)
with open('captcha.png','wb') as f:
    f.write(imgdata)
imbg = Image.open("white.png")
imfg = Image.open("captcha.png")
imbg_width, imbg_height = imbg.size
imfg_resized = imfg.resize((imbg_width, imbg_height), Image.LANCZOS)
imbg.paste(imfg_resized, None,imfg_resized)
imbg.save("captcha.png")
os.system('python ocr.py --image captcha.png  --preprocess blur>text')
with open('text','r') as f:
    text=f.readline()
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://wbtenders.gov.in/nicgep/app;jsessionid='+str(cookies['JSESSIONID'])+'?page=FrontEndAdvancedSearch&service=page',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

soup=BeautifulSoup(response1.content,features='html.parser')
seedids=soup.find('input',{'name':'seedids'})['value']
component=soup.find('input',{'name':'component'})['value']
page=soup.find('input',{'name':'page'})['value']
service=soup.find('input',{'name':'service'})['value']
session=soup.find('input',{'name':'session'})['value']
submitmode=soup.find('input',{'name':'submitmode'})['value']
submitname=soup.find('input',{'name':'submitname'})['value']
If_17=soup.find('input',{'name':'If_17'})['value']
tokenSecret=soup.find('input',{'name':'tokenSecret'})['value']
If_0_21=soup.find('input',{'name':'If_0_21'})['value']
If_19=soup.find('input',{'name':'If_19'})['value']
If_21=soup.find('input',{'name':'If_21'})['value']
If_23=soup.find('input',{'name':'If_23'})['value']
If_25=soup.find('input',{'name':'If_25'})['value']
If_27=soup.find('input',{'name':'If_27'})['value']
If_29=soup.find('input',{'name':'If_29'})['value']
orname=soup.find('option',string='<Organisation Name>')['value']
tendertype=soup.find('option',string='<Tender Type>')['value']
data = {
  'formids': 'If_17,tokenSecret,TenderType,tenderId,If_0_21,If_19,OrganisationName,tenderRefNo,If_21,Department,workItemTitle,If_23,Division,tenderCategory,If_25,SubDivision,ProductCategory,If_27,Branch,formContract,If_29,Block,pinCode,PaymentMode,valueCriteria,valueParameter,FromValue,ToValue,dateCriteria,fromDate,toDate,twoStageAllowed,ndaAllowed,prefBidAllowed,chkGteAllowed,chkIteAllowed,chkTfeAllowed,chkEfeAllowed,captchaText,captcha,submit',
  'seedids': seedids,
  'component': component,
  'page': page,
  'service': service,
  'session': session,
  'submitmode': submitmode,
  'submitname': submitname,
  'If_17': If_17,
  'tokenSecret': tokenSecret,
  'If_0_21': If_0_21,
  'If_19': If_19,
  'If_21': If_21,
  'If_23': If_23,
  'If_25': If_25,
  'If_27': If_27,
  'If_29': If_29,
  'TenderType': tendertype ,
  'tenderId': '',
  'OrganisationName': orname,
  'tenderRefNo': '',
  'Department': '<Department Value from Page Source>',
  'workItemTitle': '',
  'Division': '<Division Value from Page Source>',
  'tenderCategory': '0',
  'SubDivision': '0',
  'ProductCategory': '0',
  'Branch': '0',
  'formContract': '0',
  'Block': '0',
  'pinCode': '',
  'PaymentMode': '0',
  'valueCriteria': '0',
  'valueParameter': '0',
  'FromValue': '',
  'ToValue': '',
  'dateCriteria': '0',
  'fromDate': '',
  'toDate': '',
  'captchaText': text,
  'submit': 'Search'
}
response2 = s.post('https://wbtenders.gov.in/nicgep/app', headers=headers, cookies=cookies, data=data)
print(text)
time=now.strftime('%d-%b-%Y')
#<td align="center">8.</td>
#<td align="center">14-Jan-2020 04:00 PM</td>
pub_date=re.findall(r'\<td align\=\"center\"\>[0-9][0-9]-\w\w\w-[0-9]{4} [0-9][0-9]\:[0-9][0-9] [AP]M\<\/td\>',str(response2.content))
print(pub_date)
print(time)
l=0

for i in pub_date:
    if time in pub_date:
        l=1
if(l==1):
    print('Things Released')
else:
    print('Nothing Released')


        


