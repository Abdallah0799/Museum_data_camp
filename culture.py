# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 17:19:38 2022

@author: Cynthia
"""

import pandas as pd

df = pd.read_csv('MetObjects.csv',sep=",", low_memory="False")
df2 = df[df['Culture'].notna()]

liste = []

for val in df2['Culture']:
    temp = val.split()
    if len(temp)==1:
        liste.append(val)
    elif 'for ' in val :
        temp = val.split(',')
        if 'ilt' in val:
            temp = temp[1].split()
            liste.append(temp[0])
        else :        
            temp = temp[0].split('(')
            temp = temp[0].split('with') 
            temp = temp[0].split('for') 
            temp = temp[0].split()
            if 'robably' in temp[0] or 'ossibly' in temp[0]:     
                liste.append(" ".join(temp[1:]))
            else : liste.append(temp[0])             
    elif len(temp)==2 and ('robably' in val or 'ossibly' in val):
        if 'robably' not in temp[0] and 'ossibly' not in temp[0]:
            temp = temp[0].split(',')
            liste.append(temp[0])
        else : liste.append(temp[1])     
    elif len(temp)==2:
        temp = temp[0].split(',')
        liste.append(temp[0])
    elif '(' in val and 'arket' not in val and 'or ' not in val:
        temp = val.split('(')
        temp = temp[0].split(',')
        temp = temp[0].split(';')
        temp = temp[0].split()
        if 'robably' in temp[0] or 'ossibly' in temp[0]:     
            liste.append(" ".join(temp[1:]))
        else : liste.append(temp[0])       
    elif ' or ' in val and '(' not in val: #several cultuer given
        temp = val.split(', ')
        
        if 'robably' in temp[0] or 'ossibly' in temp[0]: 
            temp = temp[0].split()
            liste.append(" ".join(temp[1:]))
        elif 'ilt' not in temp[0] : 
            liste.append(temp[0])
        else:
            temp = temp[1].split(';')
            liste.append(temp[0])
            
    elif 'arket' in val : #to remove the market and keep the original culture
        temp = val.split(',')
        temp = temp[0].split('(') 
        temp = temp[0].split('for')
        temp = temp[0].split('with')  
        temp = temp[0].split()
        if 'robably' in temp[0] or 'ossibly' in temp[0]:                 
            liste.append(" ".join(temp[1:]))
        else : liste.append(temp[0]) 

    else :    
        temp = val.split(';')
        temp = temp[0].split(', ')       
        if 'ilt' in temp[0]: 
            if 'robably' in (" ".join(temp[1:])) or 'ossibly' in (" ".join(temp[1:])):
                temp = (" ".join(temp[1:])).split()
                if 'robably' in temp[0] or 'ossibly' in temp[0]:                 
                    liste.append(" ".join(temp[1:]))
                else : liste.append(temp[0])
            else : liste.append(" ".join(temp[1:]))
            
        else : 
            temp = temp[0].split('(') 
            temp = temp[0].split(':') 
            temp = temp[0].split('with') 
            temp = temp[0].split() 
            if 'robably' in temp[0] or 'ossibly' in temp[0]:                 
                liste.append(" ".join(temp[1:]))
            else : liste.append(temp[0])


df2['Culture'] = liste
a = df2['Culture'].unique()

#df.drop_duplicates(subset ="Customer id", keep = 'first', inplace=True)
df2.to_csv("data_cynthia.csv", index=False)