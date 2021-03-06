#!/usr/bin/env python
# coding: utf-8

# ## Scrappons WebDeleuze.com

# In[1]:


import requests
import bs4
import os
import json


# Tout d'abord après observation du site webdeleuze, on obtient l'url contenant un tableau récapitulatif de tous les textes du philosophe :

# In[2]:


token = 'https://www.webdeleuze.com/textes/1'


# A présent je peux aller chercher le code source de l'url.

# In[3]:


response = requests.get(token)


# Après observation du code source de l'url, nous allons naviguer dans le DOM (Document Object Model) pour extraire les balises correspondantes aux lignes du tableau récapitulatif contenant les textes de chaque cours du philosophe en français. Pour cela, utilisons le package python *BeautifulSoup* (site officiel https://www.crummy.com/software/BeautifulSoup/)

# In[4]:


soup = bs4.BeautifulSoup(response.text, 'html.parser')
tr_boxes = soup.find_all("tr")

print(len(tr_boxes),'lignes extraites.')


# La variable tr_boxes fonctionne comme une liste de dictionnaires. Nous pouvons alors extraire les lignes correspondant à chaque cours en français et obtenir ainsi l'url contenant le texte correspondant.

# In[5]:


urls = []
for tr_box in tr_boxes:
    elt = tr_box.find("td")
    if 'Français' in str(elt):
        urls.append(elt.find('a')["href"])
print(len(urls),'urls extraites en français.')
#230 pages extraites le 20/01/2021


# In[6]:


get_ipython().run_cell_magic('time', '', 'responses = []\nfor url in urls:\n    responses.append(requests.get(url))')


# A présent nous pouvons extraire le contenu de chaque cours dans un dictionnaire contenant les clés suivantes:
#     
#     {'Cours': 'Bibliographie et mondes inédits','Date': 'Cours du 18/02/2006','Titre': 'Hommage hivernal à Gilles Deleuze', 'contains': 'Hommage hivernal à Gilles Deleuze\r\n ..........'
#     }

# In[10]:


with open('urls_deleuze.txt', 'w') as f:
    for item in urls:
        f.write("%s\n" % item)


# In[11]:


#TEST avant la construction des fichiers json
nb_char = 0
print("----------TEST----------")
for k,response in enumerate(responses[:10]):
    print('-----extract url '+str(k),urls[k])
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    elt = soup.find("div", {"class":"form-group"})
    print('Cours:',elt.find('h2').text)
    div_date = elt.find('div','mb-4')
    print('Date:',div_date.text)
    div_title = elt.find('div','mt-4')
    print('Titre:',div_title.text)
    if len(str(elt))<1000:
        if elt.find('a') is not None:
            if 'pdf' in elt.find('a')["href"]:
                print('url:',elt.find('a')["href"])
            else:
                print('No pdf')
        else:
            print('No pdf')
    else:
        for div in elt.find_all('div','mt-4'):
            if len(str(div))>1000:
                #print('Contains',div.text)
                if len(div.text)>100:
                    a = len(div.text)
                    print('url:',urls[k])
                    print('ok avec',a,'caractères')
                    nb_char += a
print('*************',nb_char,'caractères collectées')         


# In[12]:


#ECRITURE DES JSON avec ou sans pdf
nb_char = 0
for k,response in enumerate(responses):
    current_source = {}
    print('---extract url '+str(k)+'---',urls[k])
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    elt = soup.find("div", {"class":"form-group"})
    print('Cours:',elt.find('h2').text)
    current_source['Cours'] = elt.find('h2').text
    div_date = elt.find('div','mb-4')
    print('Date:',div_date.text)
    current_source['Date'] = div_date.text
    div_title = elt.find('div','mt-4')
    print('Titre:',div_title.text)
    current_source['Titre'] = div_title.text
    if len(str(elt))<1000:
        if elt.find('a') is not None:
            if 'pdf' in elt.find('a')["href"]:
                print('url:',elt.find('a')["href"])
                current_source['url'] = urls[k]
                current_source['contains'] = 'pdf only'
                with open('../data/'+str(k)+'.json', 'w') as outfile:
                    json.dump(current_source, outfile)
            else:
                print('No pdf')
                current_source['url'] = urls[k]
                current_source['contains'] = 'Nothing'
                with open('../data/'+str(k)+'.json', 'w') as outfile:
                    json.dump(current_source, outfile)
        else:
            print('No pdf')
            current_source['url'] = urls[k]
            current_source['contains'] = 'Nothing'
            with open('../data/'+str(k)+'.json', 'w') as outfile:
                json.dump(current_source, outfile)
    else:
        for div in elt.find_all('div','mt-4'):
            if len(str(div))>1000:
                #print('Contains',div.text)
                if len(div.text)>100:
                    current_source['contains'] = div.text
                    a = len(div.text)
                    print('url:',urls[k])
                    current_source['url'] = urls[k]
                    with open('../data/'+str(k)+'.json', 'w') as outfile:
                        json.dump(current_source, outfile)
                    print('ok avec',a,'caractères')
                    nb_char += a
print('*************',nb_char,'caractères collectées')


# In[ ]:




