import pandas as pd
import numpy as np

df = pd.read_csv('MetObjects.txt',sep=",", low_memory="False")
#print(df["Dimensions"][:10])
n = df.shape[0]


#print(len(df["Dimensions"].unique())) # 259820 unique values

# print("Percentage of unavailable dimensions:", 100 * len(df[df["Dimensions"]=="Dimensions unavailable"]) / n)  # 0.08%



def find_dims(description):
    n = len(description)
    if "cm" in description:
        i = description.index("(")
        j = description[i:n].index("cm") + i 
        nb_x_utf8 = description[i:j].count('x')
        nb_x_strange = description[i:j].count('×')
        nb_x = max([nb_x_strange, nb_x_utf8])
        is_utf8 = np.argmax([nb_x_strange, nb_x_utf8]) # =1 if x normal, 0 if x strange
        x = ["×", "x"] 

        if nb_x==0: # circle
            return [float(description[i+1:j])]

        if nb_x==1: # 2D
            x_ind = description.rfind(x[is_utf8],i,j)
            dim1 = float(description[i+1:x_ind])
            dim2 = float(description[x_ind+1:j])
            return [dim1, dim2]

        else: # 3D object
            x_ind2 = description.rfind(x[is_utf8],i,j)
            x_ind1 = description.rfind(x[is_utf8],i,x_ind2)
            dim1 = float(description[i+1:x_ind1])
            dim2 = float(description[x_ind1+1:x_ind2])
            dim3 = float(description[x_ind2+1:j])
            return [dim1, dim2, dim3]

    return [] # if unavailable dimension

# test
for dim_description in df["Dimensions"].unique()[:100]:
    print(dim_description)
    print(find_dims(dim_description))
    print("*"*50)

