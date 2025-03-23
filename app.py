import pandas as pd
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

st.markdown(f"Select the number of subintervals for the $x$-variable (recommended value: 5):")
x_bins = st.number_input(
    "",
    min_value=1,
    max_value=100,
    value=5,
    step=1
)

st.markdown(f"Select the number of subintervals for the $y$-variable (recommended value: 5):")
y_bins = st.number_input(
    "",
    min_value=1,
    max_value=100,
    value=5,
    step=1
)

x_bins = pd.cut(datapts['x'], bins=x_bins, right=False)
y_bins = pd.cut(datapts['y'], bins=y_bins, right=False)

conttable=pd.crosstab(x_bins,y_bins)

st.markdown("##### Contingency table: ")

st.dataframe(pd.DataFrame(conttable))



