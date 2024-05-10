import pandas as pd
import json
import psycopg2
import plotly_express as px
import requests
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import webbrowser


mydb=psycopg2.connect(user="postgres",
                      password="ajai",
                      database="phonepey",
                      port=5432,
                      host="localhost")
cursor=mydb.cursor()

#aggricated insurence table
cursor.execute("SELECT * FROM AGGRECATED_INSURENCE")
mydb.commit()
table1=cursor.fetchall()
#converting to DataFrame
aggrecated_insurence_table=pd.DataFrame(table1,columns=("state","year","quarter","transaction_type","transaction_count","transaction_amount"))

#aggrecated transaction table
cursor.execute("SELECT * FROM AGGRECATED_TRANSACTION")
mydb.commit()
table2=cursor.fetchall()
#convertingh to Data Frame
aggrecated_transaction_table=pd.DataFrame(table2,columns=("state","year","quarter","transaction_type","transaction_count","transaction_amount"))

#aggrecated user table
cursor.execute("SELECT * FROM AGGRECATED_USER")
mydb.commit()
table3=cursor.fetchall()
#converting to dataFrame
aggrecated_user_table=pd.DataFrame(table3,columns=("state","year","quarter","brand","count","percentage"))

#map insurence table
cursor.execute("SELECT * FROM MAP_INSURENCE")
mydb.commit()
table4=cursor.fetchall()
#converting to dataFrame
map_insurence_table=pd.DataFrame(table4,columns=("state","year","quarter","district_name","transaction_count", "transaction_amount"))

#map insurence table
cursor.execute("SELECT * FROM MAP_TRANSACTION")
mydb.commit()
table5=cursor.fetchall()
#converting to dataFrame
map_transaction_table=pd.DataFrame(table5,columns=("state","year","quarter","district_name","transaction_count", "transaction_amount"))

#map insurence table
cursor.execute("SELECT * FROM MAP_USER")
mydb.commit()
table6=cursor.fetchall()
#converting to dataFrame
map_user_table=pd.DataFrame(table6,columns=("state","year","quarter","district_name","registered_users", "app_opens"))

#top insurence table
cursor.execute("SELECT * FROM TOP_INSURENCE")
mydb.commit()
table7=cursor.fetchall()
#converting to DataFrame
top_insurence_table=pd.DataFrame(table7,columns=("state","year","quarter","pincode","transaction_count","transaction_amount"))

#top transaction table
cursor.execute("SELECT * FROM TOP_TRANSACTION")
mydb.commit()
table8=cursor.fetchall()
#converting to DataFrame
top_transaction_table=pd.DataFrame(table8,columns=("state","year","quarter","pincode","transaction_count","transaction_amount"))

#top user table
cursor.execute("SELECT * FROM TOP_USER")
mydb.commit()
table9=cursor.fetchall()
#converting to DataFrame
top_user_table=pd.DataFrame(table9,columns=("state","year","quarter","pincode","registered_users"))


#top chart 


def top_chart_count(df):
    cursor.execute(f'''select state,sum(transaction_count) as transaction_count from {df}
                   group by state 
                   order by transaction_count desc
                   limit 10''')
    mydb.commit()
    table=cursor.fetchall()
    df=pd.DataFrame(table,columns=("state","transaction_count"))
    fig=px.bar(df,x="state",y="transaction_count",color_discrete_sequence=px.colors.sequential.Agsunset,title="top_chart_transaction_count")
    st.plotly_chart(fig)
    
def top_chart_amount(df):
    cursor.execute(f'''select state,sum(transaction_amount) as transaction_amount from {df}
                   group by state 
                   order by transaction_amount desc
                   limit 10''')
    mydb.commit()
    table=cursor.fetchall()
    df=pd.DataFrame(table,columns=("state","transaction_amount"))
    fig=px.bar(df,x="state",y="transaction_amount",color_discrete_sequence=px.colors.sequential.Agsunset,title="top_chart_transaction_amount")
    st.plotly_chart(fig)  

def top_chart_user(df):
    cursor.execute(f'''select state,sum(count) as user_count from aggrecated_user
                    group by state
                    order by user_count desc
                    limit 10;''')
    mydb.commit()
    table=cursor.fetchall()
    df=pd.DataFrame(table,columns=("state","user_count"))
    fig=px.bar(df,x="state",y="user_count",color_discrete_sequence=px.colors.sequential.Agsunset,title="top_chart_user_count")
    st.plotly_chart(fig)  

def top_chart_registred_user(df):
    cursor.execute(f'''select state,sum(registred_users) as registred_users from {df}
                    group by state
                    order by registred_users desc
                    limit 10;''')
    mydb.commit()
    table=cursor.fetchall()
    df=pd.DataFrame(table,columns=("state","registred_users"))
    fig=px.bar(df,x="state",y="registred_users",color_discrete_sequence=px.colors.sequential.Agsunset,title="top_chart_registred_users_count")
    st.plotly_chart(fig)      
def top_chart_app_opens(df):
    cursor.execute(f'''select state,sum(appopens) as app_opens from map_user
                    group by state
                    order by app_opens desc
                    limit 10;''')
    mydb.commit()
    table=cursor.fetchall()
    df=pd.DataFrame(table,columns=("state","app_opens"))
    fig=px.bar(df,x="state",y="app_opens",color_discrete_sequence=px.colors.sequential.Agsunset,title="top_chart_app_opens")
    st.plotly_chart(fig) 



#data visualization part
def transaction_amount_count_y(df,year):

    tacy=df[df["year"]==year]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("state")[["transaction_count","transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig=px.bar(tacyg,x="state",y="transaction_count",color_discrete_sequence=px.colors.sequential.Agsunset,title=f"{year} , TRANSACTION COUNT",height=650,width=600)
        st.plotly_chart(fig)
    with col2:
        fig1=px.bar(tacyg,x="state",y="transaction_amount",color_discrete_sequence=px.colors.sequential.Agsunset,title=f"{year} , TRANSACTION AMOUNT",height=650,width=600)
        st.plotly_chart(fig1)


    #geo visualization

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)

    data1=json.loads(response.content)
    
    
    col1,col2=st.columns(2)
    with col1:
        fig_india=px.choropleth(tacyg, geojson=data1, locations="state",featureidkey="properties.ST_NM",color="transaction_count",color_continuous_scale="Viridis",
                                range_color=(tacyg["transaction_count"].min(),tacyg["transaction_count"].max()),hover_name="state",title=f"{year} , TRANSACTION COUNT",
                                fitbounds="locations",height=650,width=500)

        st.plotly_chart(fig_india) 

    with col2:    

        fig_india1=px.choropleth(tacyg, geojson=data1, locations="state",featureidkey="properties.ST_NM",color="transaction_amount",color_continuous_scale="Viridis",
                                range_color=(tacyg["transaction_amount"].min(),tacyg["transaction_amount"].max()),hover_name="state",title=f"{year} , TRANSACTION AMOUNT",
                                fitbounds="locations",height=650,width=500)

        st.plotly_chart(fig_india1)

    return tacy

def transaction_amount_count_yq(df,quarter):

    tacy=df[df["quarter"]==quarter]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("state")[["transaction_count","transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:
        fig=px.bar(tacyg,x="state",y="transaction_count",color_discrete_sequence=px.colors.sequential.Agsunset,title=f"QUARTER NO:{quarter} , TRANSACTION COUNT",height=650,width=600)
        st.plotly_chart(fig)
    with col2:
        fig1=px.bar(tacyg,x="state",y="transaction_amount",color_discrete_sequence=px.colors.sequential.Agsunset,title=f"QUARTER NO:{quarter} ,  TRANSACTION AMOUNT",height=650,width=600)
        st.plotly_chart(fig1)


    #geo visualization

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)

    data1=json.loads(response.content)
    col1,col2=st.columns(2)
    with col1:
        fig_india=px.choropleth(tacyg, geojson=data1, locations="state",featureidkey="properties.ST_NM",color="transaction_count",color_continuous_scale="Viridis",
                                range_color=(tacyg["transaction_count"].min(),tacyg["transaction_count"].max()),hover_name="state",title=f"QUARTER NO:{quarter} , TRANSACTION COUNT",
                                fitbounds="locations",height=650,width=500)

        st.plotly_chart(fig_india) 

    with col2:
        fig_india1=px.choropleth(tacyg, geojson=data1, locations="state",featureidkey="properties.ST_NM",color="transaction_amount",color_continuous_scale="Viridis",
                                range_color=(tacyg["transaction_amount"].min(),tacyg["transaction_amount"].max()),hover_name="state",title=f"QUARTER NO:{quarter} , TRANSACTION AMOUNT",
                                fitbounds="locations",height=650,width=500)

        st.plotly_chart(fig_india1)
    return tacy

    #transaction type
   

def transaction_type_count_amount(df,states):
    tacy=df[df["state"]==states]
    tacy.reset_index(inplace=True)

    tacyg=tacy.groupby("transaction_type")[["transaction_count","transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    pie=px.pie(data_frame=tacyg,names="transaction_type",values="transaction_count",title=f"{states.upper()} STATE , TRANSACTION COUNT",hole=0.4)
    st.plotly_chart(pie)

    pie1=px.pie(data_frame=tacyg,names="transaction_type",values="transaction_amount",title=f"{states.upper()} STATE , TRANSACTION AMOUNT",hole=0.4)
    st.plotly_chart(pie1)    

def user_analysis(df,year):
    auca=df[df["year"]==year]
    auca.reset_index(drop=True,inplace=True)

    aucag=auca.groupby("brand")[["count","percentage"]].sum()
    aucag.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    with col1:

        fig=px.bar(aucag,x="brand",y="count",color_discrete_sequence=px.colors.sequential.Agsunset,title=f"{year} , TRANSACTION COUNT",height=650,width=600)
        st.plotly_chart(fig)

    with col2:

        fig=px.bar(aucag,x="brand",y="percentage",color_discrete_sequence=px.colors.sequential.Agsunset,title=f"{year} , TRANSACTION PERCENTAGE",height=650,width=600)
        st.plotly_chart(fig)    

    return auca

def user_analysis_q(df,quarter):
    aucaq=df[df["quarter"]==quarter]
    aucaq.reset_index(drop=True,inplace=True)

    aucaqg=aucaq.groupby("brand")[["count","percentage"]].sum()
    aucaqg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig=px.bar(aucaqg,x="brand",y="count",color_discrete_sequence=px.colors.sequential.Agsunset,title=f"QUARTER NO:{quarter} , TRANSACTION COUNT",hover_name="brand",height=650,width=600)
        st.plotly_chart(fig)

    with col2:

        fig=px.bar(aucaqg,x="brand",y="percentage",color_discrete_sequence=px.colors.sequential.Agsunset,title=f"QUARTER NO:{quarter} , TRANSACTION PERCENTAGE",hover_name="brand",height=650,width=600)
        st.plotly_chart(fig)

    return aucaq

def user_analysis_s(df,state):
    uas=df[df["state"]==state]
    uas.reset_index(inplace=True)

    uasg=uas.groupby("brand")[["count","percentage"]].sum()
    uasg.reset_index(inplace=True)

    pie=px.pie(data_frame=uasg,values="count",title=f"{states.upper()} STATE , TRANSACTION COUNT",hole=0.4,hover_name="brand")
    st.plotly_chart(pie)

    pie1=px.pie(data_frame=uasg,values="percentage",title=f"{states.upper()} STATE , TRANSACTION PERCENTAGE",hole=0.4,hover_name="brand")
    st.plotly_chart(pie1)    

def map_state_analylis(df,state):
    micas=df[df["state"]==state]
    micas.reset_index(drop=True,inplace=True)

    micasgs=micas.groupby("district_name")[["transaction_count","transaction_amount"]].sum()
    micasgs.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:
        fig=px.bar(micasgs,x="transaction_count",y="district_name",color_discrete_sequence=px.colors.sequential.Agsunset,title=f"{states.upper()} STATE , TRANSACTION COUNT",hover_name="district_name",orientation="h",height=650,width=600)
        st.plotly_chart(fig)
    with col2:
        fig=px.bar(micasgs,x="transaction_amount",y="district_name",color_discrete_sequence=px.colors.sequential.Agsunset,title=f"{states.upper()} STATE , TRANSACTION AMOUNT",hover_name="district_name",orientation="h",height=650,width=600)
        st.plotly_chart(fig)  



def map_user(df,year):
    mua=df[df["year"]==year]
    mua.reset_index(drop=True,inplace=True)

    muag=mua.groupby("state")[["registered_users","app_opens"]].sum()
    muag.reset_index(inplace=True)


    fig=px.line(muag,x="state",y=["registered_users","app_opens"],color_discrete_sequence=px.colors.sequential.Agsunset,title=f"{year} , USER ANALYSIS")
    st.plotly_chart(fig) 

    return mua
    

def map_user_state_analylis1(df,state):
    micas=df[df["state"]==state]
    micas.reset_index(drop=True,inplace=True)

    micasgs=micas.groupby("district_name")[["registered_users","app_opens"]].sum()
    micasgs.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig=px.bar(micasgs,x="registered_users",y="district_name",color_discrete_sequence=px.colors.sequential.Agsunset,title=f"{states.upper()} STATE , REGISTRED USERS",hover_name="district_name",orientation="h",height=650,width=600)
        st.plotly_chart(fig)

    with col2:

        fig=px.bar(micasgs,x="app_opens",y="district_name",color_discrete_sequence=px.colors.sequential.Agsunset,title=f"{states.upper()} STATE , APP OPENS",hover_name="district_name",orientation="h",height=650,width=600)
        st.plotly_chart(fig)

def map_user_q_analylis(df,quarter):
    mcqa=df[df["quarter"]==quarter]
    mcqa.reset_index(drop=True,inplace=True)

    mcqag=mcqa.groupby("state")[["registered_users","app_opens"]].sum()
    mcqag.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
    
        fig=px.bar(mcqag,x="state",y="registered_users",color_discrete_sequence=px.colors.sequential.Agsunset,title=f"QUARTER NO:{quarter} STATE , REGISTRED USERS",hover_name="state",height=650,width=600)
        st.plotly_chart(fig)

    with col2:

        fig=px.bar(mcqag,x="state",y="app_opens",color_discrete_sequence=px.colors.sequential.Agsunset,title=f"QUARTER NO:{quarter}  , APP OPENS",hover_name="state",height=650,width=600)
        st.plotly_chart(fig)    

    return mcqa

def top_insurence_s(df,state):

    tisq=df[df["state"]==state]
    tisq.reset_index(drop=True,inplace=True)

    col1,col2=st.columns(2)
    with col1:


        fig=px.bar(tisq,x="quarter",y="transaction_count",color_discrete_sequence=px.colors.sequential.Agsunset,title=f"{states.upper()} STATE , TRANSACTION COUNT",hover_data="pincode",height=650,width=600)
        st.plotly_chart(fig)
    with col2:

        fig=px.bar(tisq,x="quarter",y="transaction_amount",color_discrete_sequence=px.colors.sequential.Agsunset,title=f"{states.upper()} STATE , TRANSACTION AMOUNT",hover_data="pincode",height=650,width=600)
        st.plotly_chart(fig)

def top_user(df,year):

    tua=df[df["year"]==year]
    tua.reset_index(drop=True,inplace=True)

    tuag=pd.DataFrame(tua.groupby(["state","quarter"])["registered_users"].sum())
    tuag.reset_index(inplace=True)

    fig=px.bar(tuag,x="state",y="registered_users",color="quarter",color_discrete_sequence=px.colors.sequential.Agsunset,hover_name="state",title=f"{year} , USER ANALYSIS")
    st.plotly_chart(fig)

    return tua

def top_user_states(df,state) :

    tuas=df[df["state"]==state]
    tuas.reset_index(drop=True,inplace=True)

    fig=px.bar(tuas,x="quarter",y="registered_users",color="registered_users",hover_data="pincode",color_continuous_scale=px.colors.sequential.Agsunset,title=f"{state.upper()} , USER ANALYSIS",height=900)
    st.plotly_chart(fig)

    

#streamlit part
st.set_page_config(layout ="wide")
st.title("   PHONEPE PULSE DATA VISUALIZATION")


st.image(r"C:\Users\USER\Desktop\phonepey\Screenshot (26).png")
with st.sidebar:
    option=option_menu("SELECT THE OPTIONS BELLOW",["HOME","DATA VISUALIZATION","TOP CHARTS"])
if option=="HOME":
    col1,col2=st.columns(2)
    with col1:
        st.image(r"C:\Users\USER\Desktop\phonepey\evw5ce98p6flvjemp1bq.png")
        st.title("Simple, Fast & Secure")
        st.header("One app for all things money.")
        st.write("Pay bills, recharge, send money, buy gold, invest and shop at your favourite stores.")
        st.write("...............................................................................................................")
        st.header("Pay whenever you like, wherever you like.")
        st.write("Choose from options like UPI, the PhonePe wallet or your Debit and Credit Card.")
        st.write("...............................................................................................................")
        st.header("Find all your favourite apps on PhonePe Switch.")
        st.write("Book flights, order food or buy groceries. Use all your favourite apps without downloading them.")
        
    with col2:
        st.video(r"C:\Users\USER\Desktop\phonepey\Introducing PhonePe Pulse.mp4")
        st.markdown("Keep Doing. Keep Progressing.")
        st.image(r"C:\Users\USER\Desktop\phonepey\194697894-54351b95-e9ab-4321-80a8-baa4845510d7.png",width=450)
      


elif option=="DATA VISUALIZATION":
    tab1,tab2,tab3=st.tabs(["AGGRECATED ANALYSIS","MAP ANALYSIS","TOP ANALYSIS"])
    with tab1:
        select=st.radio("SELECT THE OPTIONS BELLOW",["AGGRECATED INSURENCE ","AGGRECATED TRANSACTION ","AGGRECATED USER"])
        if select=="AGGRECATED INSURENCE ":
            col1,col2=st.columns(2)
            with col1:
                years=st.slider("SELECT THE YEAR",aggrecated_insurence_table["year"].min(),aggrecated_insurence_table["year"].max(),aggrecated_insurence_table["year"].min())
            q_analysis=transaction_amount_count_y(aggrecated_insurence_table,years)
            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("SELECT THE QUARTER",q_analysis["quarter"].min(),q_analysis["quarter"].max(),q_analysis["quarter"].min())
            transaction_amount_count_yq(q_analysis,quarters)
    
        if select=="AGGRECATED TRANSACTION ":
            years=st.slider("SELECT THE YEAR",aggrecated_transaction_table["year"].min(),aggrecated_transaction_table["year"].max(),aggrecated_transaction_table["year"].min())
            q_analysis=transaction_amount_count_y(aggrecated_transaction_table,years)

            states=st.selectbox("SELECT THE STATE",aggrecated_transaction_table["state"].unique())
            transaction_type_count_amount(q_analysis,states)

            quarters=st.slider("SELECT THE QUARTER",q_analysis["quarter"].min(),q_analysis["quarter"].max(),q_analysis["quarter"].min())
            quarted_df=transaction_amount_count_yq(q_analysis,quarters)

            states=st.selectbox("SELECT THE STATES",aggrecated_transaction_table["state"].unique())
            transaction_type_count_amount(quarted_df,states)

        if select=="AGGRECATED USER":
            years=st.slider("SELECT THE YEAR",aggrecated_user_table["year"].min(),aggrecated_user_table["year"].max(),aggrecated_user_table["year"].min())
            q_analysis=user_analysis(aggrecated_user_table,years)


            states=st.selectbox("SELECT THE STATE",aggrecated_user_table["state"].unique()) 
            user_analysis_s(q_analysis,states)
             
            quarters=st.slider("SELECT THE QUARTER",q_analysis["quarter"].min(),q_analysis["quarter"].max(),q_analysis["quarter"].min()) 
            quarted_df=user_analysis_q(q_analysis,quarters)
             
            states=st.selectbox("SELECT THE STATES",aggrecated_user_table["state"].unique()) 
            user_analysis_s(quarted_df,states)

    with tab2:
        select1=st.radio("SELECT THE OPTIONS BELLOW",["MAP INSURENCE","MAP TRANSACTION ","MAP USER"])        
        if select1=="MAP INSURENCE":
            years=st.slider("SELECT THE YEARS",map_insurence_table["year"].min(),map_insurence_table["year"].max(),map_insurence_table["year"].min())
            q_analysis=transaction_amount_count_y(map_insurence_table,years)

            states=st.selectbox("SELECT THE STATE",q_analysis["state"].unique()) 
            map_state_analylis(q_analysis,states)
            
            quarters=st.slider("SELECT THE QUARTERS",q_analysis["quarter"].min(),q_analysis["quarter"].max(),q_analysis["quarter"].min())
            quarted_df=transaction_amount_count_yq(q_analysis,quarters)

            states=st.selectbox("SELECT THE STATE",quarted_df["state"].unique()) 
            map_state_analylis(quarted_df,states)

        if select1=="MAP TRANSACTION ":    

            years=st.slider("SELECT THE YEAR",map_transaction_table["year"].min(),map_transaction_table["year"].max(),map_transaction_table["year"].min())
            q_analysis=transaction_amount_count_y(map_transaction_table,years)

            states=st.selectbox("SELECT THE STATE",q_analysis["state"].unique()) 
            map_state_analylis(q_analysis,states)
            
            quarters=st.slider("SELECT THE QUARTERS",q_analysis["quarter"].min(),q_analysis["quarter"].max(),q_analysis["quarter"].min())
            quarted_df=transaction_amount_count_yq(q_analysis,quarters)

            states=st.selectbox("SELECT THE STATES",quarted_df["state"].unique()) 
            map_state_analylis(quarted_df,states)

        if select1=="MAP USER":   
            years=st.slider("SELECT THE YEAR",map_user_table["year"].min(),map_user_table["year"].max(),map_user_table["year"].min())
            q_analysis=map_user(map_user_table,years) 

            states=st.selectbox("SELECT THE STATE",q_analysis["state"].unique()) 
            map_user_state_analylis1(q_analysis,states) 

            quarters=st.slider("SELECT THE QUARTERS",q_analysis["quarter"].min(),q_analysis["quarter"].max(),q_analysis["quarter"].min())
            quarted_df=map_user_q_analylis(q_analysis,quarters)

            states=st.selectbox("SELECT THE STATES",quarted_df["state"].unique()) 
            map_user_state_analylis1(quarted_df,states)


   

  
    with tab3:
        select=st.radio("SELECT THE OPTIONS BELLOW",["TOP INSURENCE","TOP TRANSACTION ","TOP USER"])

        if select=="TOP INSURENCE":
            years=st.slider("SELECT THE YEAR.",top_insurence_table["year"].min(),top_insurence_table["year"].max(),top_insurence_table["year"].min())
            q_analysis=transaction_amount_count_y(top_insurence_table,years)
           
            states=st.selectbox("SELECT THE STATESS",q_analysis["state"].unique())
            top_insurence_s(q_analysis,states)

            quarters=st.slider("SELECT THE QUARTER.",q_analysis["quarter"].min(),q_analysis["quarter"].max(),q_analysis["quarter"].min())
            quarted_df=transaction_amount_count_yq(q_analysis,quarters)
          

        if select=="TOP TRANSACTION ":  

            years=st.slider("SELECT THE YEARS",top_transaction_table["year"].min(),top_transaction_table["year"].max(),top_transaction_table["year"].min())
            q_analysis=transaction_amount_count_y(top_transaction_table,years)
           
            states=st.selectbox("SELECT THE STATES.",q_analysis["state"].unique())
            top_insurence_s(q_analysis,states)

            quarters=st.slider("SELECT THE QUARTER.",q_analysis["quarter"].min(),q_analysis["quarter"].max(),q_analysis["quarter"].min())
            quarted_df=transaction_amount_count_yq(q_analysis,quarters)
  
        if select=="TOP USER":   
            
            years=st.slider("SELECT THE YEAR.",top_user_table["year"].min(),top_user_table["year"].max(),top_user_table["year"].min())
            q_analysis=top_user(top_user_table,years)


            states=st.selectbox("SELECT THE STATE.",q_analysis["state"].unique())
            top_user_states(q_analysis,states)       

elif option=="TOP CHARTS":
    questions=st.selectbox("select the questions",["1.TRANSACTION COUNT AND AMOUNT OF AGGRECATED INSURENCE",
                                                   "2.TRANSACTION COUNT AND AMOUNT OF MAP INSURENCE",
                                                   "3.TRANSACTION COUNT AND AMOUNT OF TOP INSURENCE",
                                                   "4.TRANSACTION COUNT AND AMOUNT OF AGGRECATED TRANSACTION",
                                                   "5.TRANSACTION COUNT AND AMOUNT OF MAP TRANSACTION",
                                                   "6.TRANSACTION COUNT AND AMOUNT OF TOP TRANSACTION",
                                                   "7.TRANSACTION COUNT OF AGGRECATED USER",
                                                   "8.REGISTRED USERS OF MAP USER",
                                                   "9.APP OPENS OF MAP USER",
                                                   "10.REGISTRED USERS OF TOP USER"])  
    
    if questions=="1.TRANSACTION COUNT AND AMOUNT OF AGGRECATED INSURENCE":   
        top_chart_count("aggrecated_insurence")
        top_chart_amount("aggrecated_insurence")
    
    if questions=="2.TRANSACTION COUNT AND AMOUNT OF MAP INSURENCE":
        top_chart_count("map_insurence")
        top_chart_amount("map_insurence")

    if questions=="3.TRANSACTION COUNT AND AMOUNT OF TOP INSURENCE":
        top_chart_count("top_insurence")
        top_chart_amount("top_insurence")    

    
    if questions=="4.TRANSACTION COUNT AND AMOUNT OF AGGRECATED TRANSACTION":
        top_chart_count("aggrecated_transaction")
        top_chart_amount("aggrecated_transaction")     

    if questions== "5.TRANSACTION COUNT AND AMOUNT OF MAP TRANSACTION":
        top_chart_count("map_transaction")
        top_chart_amount("map_transaction")

    if questions=="6.TRANSACTION COUNT AND AMOUNT OF TOP TRANSACTION":
        top_chart_count("top_transaction")
        top_chart_amount("top_transaction")     


    if questions=="7.TRANSACTION COUNT OF AGGRECATED USER":
        top_chart_user("aggrecated_user")   

 
    if questions== "8.REGISTRED USERS OF MAP USER":
        top_chart_registred_user("map_user")

    if questions== "9.APP OPENS OF MAP USER":
        top_chart_app_opens("map_user")

    if questions=="10.REGISTRED USERS OF TOP USER":
        top_chart_registred_user("top_user")     

st.image(r"C:\Users\USER\Desktop\phonepey\194697815-623f0cd5-bbf0-4c2c-89d6-f46dfb56cec4.png")
col1,col2,col3,col4=st.columns(4)

with col1:
    if st.button("HOME"):         
        webbrowser.open("https://www.phonepe.com/")    
      
with col2:
    if st.button("REGISTER"):
        webbrowser.open("https://www.phonepe.com/")
with col3:
    if st.button("CONTACT US"):
        webbrowser.open("https://www.phonepe.com/contact-us/")       
with col4:
    if st.button("ABOUT US"):
        webbrowser.open("https://www.phonepe.com/about-us/")




    








      
