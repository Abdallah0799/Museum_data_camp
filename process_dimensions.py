import pandas as pd
import numpy as np

# df = pd.read_csv('MetObjects.txt',sep=",", low_memory="False")
df = pd.read_csv('data_loic.txt',sep=",", low_memory="False")

#print(df["Dimensions"][:10])
n = df.shape[0]


#print(len(df["Dimensions"].unique())) # 259820 unique values

# print("Percentage of unavailable dimensions:", 100 * len(df[df["Dimensions"]=="Dimensions unavailable"]) / n)  # 0.08%



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
    


# test

# H. 11 3/16 in. (28.5 cm); W. 8 7/8 in. (22.53 cm); Wt. 2 lb. 6 oz. (1092 g)
""" for dim_description in df["Dimensions"][:10]:
    print(dim_description)
    print(find_dims(dim_description))
    print("*"*50) """

# ------------------------------------------------------------------------------------------------------------

df["height"] = [-1]*n
df["width"] = [-1]*n
df["depth"] = [-1]*n
df["diam"] = [-1]*n

#df.loc[0,"width"] = 3

""" for i,description in enumerate(df["Dimensions"]):
    print(i+1)
    found_dims = find_dims(description) # dico
    for k in found_dims.keys():
        if k in ["height", "width", "depth", "diam"]: # just in case {} or {"radius"}
            df.loc[i,k] = found_dims[k]
        if k=="radius":
            print(k) """


#print(df["height"].head())
#print(df["width"].head())
#print(df["depth"].head(10))
#print(df["diam"].head(10))
#df.to_csv("data_loic_terence.csv", index=False)
print(n)






