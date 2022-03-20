import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


def prep_culture(df):
    
    liste = []
    for val in df['Culture']:
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
                
    return liste


def find_dims(description):
    try:
        n = len(description)
    except TypeError:
        return {}

    try:
        if "cm" in description:
            # try to find spitted dimensions: H. .... (_ cm) .... W. ... (_cm) ... L. ... (_cm)
            dim = {}
            if "H." in description:
                # search height
                i_h = description.index("H.")
                i_open_bracket = description[i_h:n].index("(") + i_h
                i_cm = description[i_open_bracket:n].index("cm") + i_open_bracket
                h = float(description[i_open_bracket+1:i_cm])
                dim["height"] = h
            if "W." in description:
                # search width
                i_w = description.index("W.")
                i_open_bracket = description[i_w:n].index("(") + i_w
                i_cm = description[i_open_bracket:n].index("cm") + i_open_bracket
                w = float(description[i_open_bracket+1:i_cm])
                dim["width"] = w
            if "L." in description:
                # search length
                i_l = description.index("L.")
                i_open_bracket = description[i_l:n].index("(") + i_l
                i_cm = description[i_open_bracket:n].index("cm") + i_open_bracket
                l = float(description[i_open_bracket+1:i_cm])
                dim["depth"] = l
            
            if "Diam." in description:
                # search length
                i_diam = description.index("Diam.")
                i_open_bracket = description[i_diam:n].index("(") + i_diam
                i_cm = description[i_open_bracket:n].index("cm") + i_open_bracket
                diam = float(description[i_open_bracket+1:i_cm])
                dim["diam"] = diam


            if dim!={}: # if the search has been successful
                return dim

            # try to find dimensions in the form (_), (_,_) or (_,_,_)
            i = description.index("(")
            j = description[i:n].index("cm") + i 
            nb_x_utf8 = description[i:j].count('x')
            nb_x_strange = description[i:j].count('×')
            nb_x = max([nb_x_strange, nb_x_utf8])
            is_utf8 = np.argmax([nb_x_strange, nb_x_utf8]) # =1 if x normal, 0 if x strange
            x = ["×", "x"] 

            if nb_x==0: # circle
                return {"diam":float(description[i+1:j])}

            if nb_x==1: # 2D
                x_ind = description.rfind(x[is_utf8],i,j)
                dim1 = float(description[i+1:x_ind])
                dim2 = float(description[x_ind+1:j])
                return {"height":dim1, "width":dim2}

            else: # 3D object
                x_ind2 = description.rfind(x[is_utf8],i,j)
                x_ind1 = description.rfind(x[is_utf8],i,x_ind2)
                dim1 = float(description[i+1:x_ind1])
                dim2 = float(description[x_ind1+1:x_ind2])
                dim3 = float(description[x_ind2+1:j])
                return {"height":dim1, "width": dim2, "depth":dim3}

    except ValueError:
        return {}
    return {} # if unavailable dimension

def prep_classification(df):
    Classification = []
    
    for classification in df["Classification"]:
        without_space = classification.split()[0]
        without_hyphen = without_space.split('-')[0]
        without_bar = without_hyphen.split('|')[0]
        Classification.append(without_bar)
    
    return Classification


def prep_medium(df):
    
    X = df['Medium'].values
    Medium = []
    sep = ","

    vectorizer = CountVectorizer(stop_words="english", max_features=24)
    vectorizer.fit(X)
    vectorized_input = vectorizer.transform(X)
    inv_transform = vectorizer.inverse_transform(vectorized_input)
    
    for arr in inv_transform:
        arr = list(arr)
        arr = sorted(arr)
        arr = sep.join(arr)
        Medium.append(arr)
    
    return Medium

def prep_date(df):
    historical_period = []
    for i in range(df.shape[0]):
        date = df.iloc[i]['Object Begin Date']
        if date <= 476 :
            historical_period.append("Antiquity")
        if date >= 477 and date <= 1492 :
            historical_period.append("Middle Ages")
        if date >= 1493 and date <= 1800 :
            historical_period.append("Modern Times")
        if date >= 1801 :
            historical_period.append("Contemporary Era")
            
    return historical_period
