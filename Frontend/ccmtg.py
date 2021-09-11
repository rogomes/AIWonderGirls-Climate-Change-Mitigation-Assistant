import streamlit as st
import altair as alt

import pandas as pd
import numpy as np
import json
import base64

import re
import requests
import streamlit.components.v1 as components
import SessionState
import plotly.figure_factory as ff

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator






st.set_option('deprecation.showPyplotGlobalUse', False)
#Function definitions
    
dd_df= ildf= pd.DataFrame() 
sector = dd_catg = ''
sectors = []


ildf = pd.read_csv('data/il_article_content_v2.csv')
ildf['abstract'].replace('', np.nan, inplace=True)
ildf.dropna(subset=['abstract'], inplace=True)

sectors = ildf['category'].unique()
sector = sectors[0]
dd_df = pd.read_csv('data/dd_solutions_data_v3.csv')
dd_catg = dd_df['map_topic'].unique()
dd_df = dd_df.fillna('')
sector_map_dict = { 'climateScience': 'Industry', 'socialCost':'Industry', 'health':'Health', 
                    'agriculture':'Agriculture', 'labour':'Transportation',
                    'energy':'Electricity', 'conflict':'industry', 
                    'coastal': 'Transportation', 'migration':'Industry'
                   }


#### Application starts
st.sidebar.image('images/main.jpeg')
st.sidebar.write('Climate Change   ')
selection = st.sidebar.selectbox("Go to page:", [ 'Climate Change Effects', 'Climate Change Studies' , 'Climate Mitigation Solutions', 'Analysis'])


#Main Window

session_state = SessionState.get(sector='')
sess_topics = SessionState.get(topics=[])
sess_ddtopics = SessionState.get(ddtopics=[])

st.title('Climate Change Mitigation Assistant ')
if selection == 'Climate Change Effects':
        st.image('images/cce1.jpeg')
        st.header('Climate Change Effects ')
        st.write("greenhouse gases , global warming")

elif selection == 'Climate Change Studies':
        st.image('images/cl2.jpeg')
        st.header('Climate Change Studies')
        st.write(' Climate Change effects in various sectors and areas studied by ImpactLab are taken for analysis')
        sector = st.selectbox( 'Climate Change Impact sectors ', sectors)
        session_state.sector = sector
        #st.write('from session:', session_state.sector)
        cltopics = ildf["header"].loc[ildf["category"] == sector]
        sess_topics.topics= cltopics.tolist()

        topic = st.selectbox( 'Climate Change Impact Topic ', sess_topics.topics)
        ildf_sec = ildf[ildf['category'] ==sector]
        topic_row = ildf_sec.loc[ ildf_sec['header'] == topic]

        abstract = topic_row['abstract'].tolist()
        #st.write(abstract)
        if(abstract):
            if( len(abstract)>> 0):
                st.write('Abstract:')
                st.write(abstract[0])
                text = abstract[0]
                wordcloud = WordCloud(max_font_size=50, max_words=30, background_color="white").generate(text)
                # Display the generated image:
                fig, ax = plt.subplots()
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis("off")
                plt.show()
                st.pyplot(fig)




elif selection == 'Climate Mitigation Solutions':
        st.header('CLimate Change Mitigation Solutions')
        st.image('images/ccmit3.jpeg')
        
        st.write('Climate Change mitigation solutions from drawdown portal are analysed here') 

        categ = st.selectbox( 'Climate Mitigition Catgories ', dd_catg)
        catg_df = dd_df[dd_df['map_topic'] == categ]

        node1_counts = catg_df['node1'].value_counts()
        node1chart  = node1_counts.sort_values()
        node1chart =node1chart.rename("Area")

        st.subheader('Contributes to Area')
        alch1 = alt.Chart(catg_df).mark_bar().encode( alt.Y('node1:N'), alt.X('count(node1):Q'))
        alch1.encoding.x.title = 'Solutions'
        alch1.encoding.y.title = 'Mitigation Area'
        st.write(alch1) 

        st.subheader('Mitigation Type')
        alch = alt.Chart(catg_df).mark_bar().encode( alt.Y('node2:N'), alt.X('count(node2):Q'))
        alch.encoding.x.title = 'Solutions'
        alch.encoding.y.title = 'Mitigation Type'
        st.write(alch) 



        #ddtopics = dd_df[dd_df['map_topic'] == categ]['title']
        ddtopics = dd_df["title"].loc[dd_df["map_topic"] == categ]
        sess_ddtopics.ddtopics=ddtopics.tolist()

        sol = st.selectbox( 'Climate Solutions ', sess_ddtopics.ddtopics)
        #st.write('You selected:', sol)      
        sol_row = dd_df.loc[ dd_df['title'] == sol]
        
        area = sol_row['area'].tolist()
        node1 = sol_row['node1'].tolist()
        node2 = sol_row['node2'].tolist()
        pr_node2 = ''
        if (len(node2) ==0 ):
            pr_node2=''
        else:
            pr_node2=node2[0]
      
        short_def = sol_row['short_def'].tolist()
        if(short_def):
            if(( len(short_def) > 0) & (short_def[0] != '')):
                st.write(short_def[0])
        st.write(area[0],"->", node1[0],"->", pr_node2) 
        st_label1 = sol_row['st_label1'].tolist()
        st_unit1 = sol_row['st_unit1'].tolist()
        st_val1 = sol_row['st_value1'].tolist()

        if(st_label1[0] != '0'):
            st.write(st_label1[0], st_val1[0], st_unit1[0]) 
        showtype = st.selectbox( 'Climate Solution Detail ', ['Impact', 'Summary'])
     
        impact_str = summary_str = ''
        summary = sol_row['summary'].tolist()
        impact = sol_row['impact'].tolist()
        if(impact):
            if( len(impact) > 0):
                impact_str = impact[0]

        tech_summary = sol_row['tech_summary'].tolist()[0]
        if(summary):
            if( len(summary) > 0):
                text = summary[0]
                summary_str = text
                newsol = "Solution SummaryThis is a new solution;"
                if( newsol in text):
                    text=tech_summary
        if(showtype=='Impact'):
             st.write(impact_str)
        else:
             st.write(summary_str)
        wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(tech_summary)
        # Display the generated image:
        fig, ax = plt.subplots()
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot(fig)



elif selection == 'Analysis':
        st.header('Analysis on Climate Change Effects , Mitigation ')
        st.image('images/ccmit3.jpeg')






