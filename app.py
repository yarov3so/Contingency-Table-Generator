import pandas as pd
import numpy as np
import re
import streamlit as st


def comprehend(mystring):
    mystring=mystring.replace(" ", "")
    data_list=mystring.split(",")
    data =[]
    for el in data_list:
        try:
            data.append(float(el))
        except: 
            for i in range(int(re.findall(r'\d+', el)[0])):
                data.append(None)
    return data

def try_int(num):
    
    num_int=None
    try:
        num_int=int(num)
    except:
        return num
    if num==num_int:
        return num_int
    elif (num<=0.1 and num>=0) or (num>=-0.1 and num<=0):
        return "{:.2g}".format(float(num))
    else:
        return round(float(num),2)
    
datapts=pd.DataFrame(columns=['x', 'y'])
current_entry={0}

st.title("Contingency Table Generator")
st.markdown("Produces a contingency table for a set of data points.")

entries={}
i=0
while True:
    
    entries[i]=st.text_input("Enter a pair of coordinates separated by a comma, or write 'done' if you are done: ",key=i)
    if len(entries[i])==0:
        st.stop()
        break
    if "," not in entries[i]:
        break
    try:
        datapts.loc[len(datapts)]=comprehend(entries[i])
    except:
        st.markdown("Cannot parse your entry! Did you make a typo?")
        st.stop()
    i+=1

if len(datapts)==0 or (i==0 and "," not in entries[0]) or (i==0 and entries[0] == ",") :
    st.markdown("You have entered no data points!")
    st.stop()

datapts=datapts.sort_values(by="x")
n=len(datapts)

st.markdown("You have entered the following coordinates:")
st.dataframe(datapts,hide_index=True)

# x_bins = st.number_input(
#     "Select the number of subintervals for the x-variable (recommended value: 5):",
#     min_value=1,
#     max_value=100,
#     value=5,
#     step=1
# )

# y_bins = st.number_input(
#     "Select the number of subintervals for the y-variable (recommended value: 5)",
#     min_value=1,
#     max_value=100,
#     value=5,
#     step=1
# )

x_bins=st.text_input("Select the number of subintervals for the x-variable (recommended value: 5)",value="5",key="x_bins")
y_bins=st.text_input("Select the number of subintervals for the x-variable (recommended value: 5)",value="5",key="y_bins")

if x_bins=="" or y_bins=="":
    st.stop()

x_bins=int(x_bins)
y_bins=int(y_bins)

max_x=max(datapts["x"])
min_x=min(datapts["x"])

max_y=max(datapts["y"])
min_y=min(datapts["y"])

invlwidth_x=(max_x-min_x)/x_bins
invlwidth_y=(max_y-min_y)/x_bins

def nearest_mag(width):
    width_str=str(width)
    first_nonzero_pos=0
    for i in range(len(width_str)):
        if width_str[i]!="0" and width_str[i]!=".":
            break
        i+=1
    start=int(width_str.index(".") - first_nonzero_pos)
    while width+10**start>2*width:
        start-=1
    return 10**start

max_x=(int(max_x//(nearest_mag(invlwidth_x))) + 1)*nearest_mag(invlwidth_x)
min_x=(int(min_x//(nearest_mag(invlwidth_x))) - 1)*nearest_mag(invlwidth_x)

invlwidth_x=(max_x-min_x)/x_bins
invlwidth_y=(max_y-min_y)/x_bins

bds_x=[min_x+i*invlwidth_x for i in range(x_bins)]
bds_x.append(max_x)
bds_y=[max_x+i*invlwidth_y for i in range(x_bins)]
bds_y.append(max_y)

subinvls_x=[]
subinvls_y=[]

for i in range(len(bds_x[:-1])):
    subinvls_x.append(f"[{try_int(bds_x[i])},{try_int(bds_x[i+1])})")
for i in range(len(bds_y[:-1])):
    subinvls_y.append(f"[{try_int(bds_y[i])},{try_int(bds_y[i+1])})")

matrix=np.zeros((x_bins,y_bins))
data=datapts.to_numpy()
for pt in data:
    for i in range(x_bins):
        for j in range(y_bins):
            if (bds_x[i]<=pt[0]) and (pt[0]<bds_x[i+1]) and ((bds_y[j]<=pt[1])) and (pt[1]<bds_y[j+1]):
                matrix[i][j]+=1
                break

df=pd.DataFrame(matrix) #,columns=subinvls_y,index=subinvls_x


st.text("")
st.markdown("##### Contingency table: ")

st.dataframe(df)



