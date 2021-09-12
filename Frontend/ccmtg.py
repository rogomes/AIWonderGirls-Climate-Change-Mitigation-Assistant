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
import plotly.graph_objects as go
import warnings


from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator



warnings.filterwarnings( "ignore")



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
selection = st.sidebar.selectbox("Go to page:", [ 'Climate Change Effects', 'Climate Change Studies' , 'Climate Mitigation Solutions', 'Further Scope & Credits'])


# Main Window

session_state = SessionState.get(sector='')
sess_topics = SessionState.get(topics=[])
sess_ddtopics = SessionState.get(ddtopics=[])

st.title('Climate Change Mitigation Assistant ')
if selection == 'Climate Change Effects':
        st.image('images/cce1.jpeg')
        st.header('Climate Change Effects')
        st.write("It is widely known that human activities especially \
                  the burning of fossil fuels have caused global warming \
                  that eventually causes climate change.")
        st.write("Global warming means rising global temperature, which causes \
                  a number of adverse effects.")
        st.write("This includes rising sea level, melting ice caps, and many more.")

        st.write("Below we can see the rising global temperature anomaly over time.")
        temperature = pd.read_csv("data/global-temperature-annual.csv")
        year_start_temp, year_end_temp = st.slider('Choose year range:', 1880, 2016, (1880, 2016))
        st.write("Global temperature anomaly data are sourced from NASA's GISS Surface Temperature \
                  (GISTEMP) analysis and the global component of Climate at a Glance (GCAG).")
        source = st.selectbox("Select data source:", ['GISTEMP', 'GCAG'])

        fig = go.Figure()
        fig.add_trace(go.Scatter(x = temperature.loc[(temperature['Year'] >= year_start_temp) \
                                 & (temperature['Year'] <= year_end_temp)]['Year'],
                                 y = temperature.loc[(temperature['Year'] >= year_start_temp) \
                                 & (temperature['Year'] <= year_end_temp)][temperature['Source'] == source]['Mean'],
                                 mode = 'lines',
                                 name = 'Global Temperature Change Anomaly'))
        st.plotly_chart(fig, use_container_width=True)

        st.write("Below we can see the rising sea level over time.")
        sealevel = pd.read_csv("data/epa-sea-level.csv")
        year_start_sea, year_end_sea = st.slider('Choose year range:', 1880, 2013, (1880, 2013))
        st.write("Sea level data were sourced from CSIRO Adjusted Sea Level \
                  from the Environmental Protection Agency (EPA), USA.")

        fig = go.Figure()
        fig.add_trace(go.Scatter(x = sealevel.loc[(sealevel['Year'] >= year_start_sea) \
                                 & (temperature['Year'] <= year_end_sea)]['Year'],
                                 y = sealevel.loc[(sealevel['Year'] >= year_start_sea) \
                                 & (temperature['Year'] <= year_end_sea)]['CSIRO Adjusted Sea Level'],
                                 mode = 'lines',
                                 name = 'Global Sea Level Rise'))
        st.plotly_chart(fig, use_container_width=True)


        st.write('Below is a bar chart race showing the top n countries that produce \
                  the most ' + 'CO{}'.format('\u2082') + ' emissions over the years.')
        st.video('carbon-emissions.mp4')




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
                words1 = st.slider('Choose the number of words to display:', min_value=5, max_value=150, value=50, step=5)
                wordcloud = WordCloud(max_font_size=50, max_words=words1, background_color="white").generate(text)
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
        words2 = st.slider('Choose the number of words to display:', min_value=5, max_value=150, value=50, step=5)
        wordcloud = WordCloud(max_font_size=50, max_words=words2, background_color="white").generate(tech_summary)
        # Display the generated image:
        fig, ax = plt.subplots()
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot(fig)



elif selection == 'Further Scope & Credits':
        st.image('images/ccmit3.jpeg')
        st.subheader('Intended Audience:')
        st.write("The mitigation assistant application can be used by industry,policy makers, communities,and general public in adapting to the climate effects relevant to their sector and helps in climate mitigation solution planning implemetation" )
        st.subheader("This application can be enhanced with ")
        st.write("* QnA NLP system for user to query any topic/solution.")
        st.write("* Adding more portals for climate study and solutions.")
        st.write("* Support industries/communities in implementation of solutions.")
        st.write("* Provide rating  for industries/policies on effeciency and impact of solutions.")
        st.write("* Motivate general public in raising awareness on climate solutions.")
        st.write("* Promote public, private partnerships  in implementation of climate solutions.")

        st.subheader("Credits:")
        st.write("* https://impactlab.org")
        st.write("* https://drawdown.org")
        st.write("* https://datahub.io/core/global-temp")
        st.write("* https://www.epa.gov/climate-indicators/climate-change-indicators-sea-level")
        st.write("* https://databank.worldbank.org/source/millennium-development-goals# ") 







