from operator import index
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import Similar
from PIL import Image
import plotly.express as px


image = Image.open('Images//ourl.jpg')
st.image(image, use_column_width=True)
st.title("Resume Matcher")


# Reading the CSV files prepared by the fileReader.py
Resumes = pd.read_csv('Resume_Data.csv')
Jobs = pd.read_csv('Job_Data.csv')

############################### JOB DESCRIPTION CODE ######################################
# Checking for Multiple Job Descriptions
# If more than one Job Descriptions are available, it asks user to select one as well.
if len(Jobs['Name']) <= 1:
    st.write(
        "There is only 1 available Job Descrition present. It will be used to create scores.")
else:
    st.write("There are ", len(Jobs['Name']),
             "Job Descriptions available. Please select one.")


# To Print the Job Desciption Names
index = [a for a in range(len(Jobs['Name']))]
fig = go.Figure(data=[go.Table(header=dict(values=["Job No.", "Job Desc. Name"], line_color='darkslategray',
                                                   fill_color='lightskyblue'),
                                       cells=dict(values=[index, Jobs['Name']], line_color='darkslategray',
                                                  fill_color='black'))
                              ])
fig.update_layout(width=700, height=400)
st.write(fig)

    
# Asking to chose the Job Description
index = st.slider("Which JD to select ? : ", 0,
                  len(Jobs['Name'])-1, 1)


option_yn = st.selectbox("Show the Job Description ?", options=['YES', 'NO'])
if option_yn == 'YES':
    st.markdown("---")
    st.markdown("### Job Description :")
    fig = go.Figure(data=[go.Table(
        header=dict(values=["Job Description"],
                    fill_color='#f0a500',
                    align='center', font=dict(color='white', size=16)),
        cells=dict(values=[Jobs['Context'][index]],
                   fill_color='#262730',
                   align='left'))])

    fig.update_layout(width=800, height=500)
    st.write(fig)
    st.markdown("---")


#################################### SCORE CALCUATION ################################
@st.cache()
def calculate_scores(resumes, job_description):
    scores = []
    for x in range(resumes.shape[0]):
        score = Similar.match(
            resumes['TF_Based'][x], job_description['TF_Based'][index])
        scores.append(score)
    return scores


Resumes['Scores'] = calculate_scores(Resumes, Jobs)

Ranked_resumes = Resumes.sort_values(
    by=['Scores'], ascending=False).reset_index(drop=True)

Ranked_resumes['Rank'] = pd.DataFrame(
    [i for i in range(1, len(Ranked_resumes['Scores'])+1)])

###################################### SCORE TABLE PLOT ####################################

fig1 = go.Figure(data=[go.Table(
    header=dict(values=["Rank", "Name", "Scores"],
                fill_color='#00416d',
                align='center', font=dict(color='black', size=16)),
        cells=dict(values=[Ranked_resumes.Rank, Ranked_resumes.Name, Ranked_resumes.Scores],
               fill_color='#d6e0f0',
               align='left', font=dict(color='black' )))])

fig1.update_layout(title="Top Ranked Resumes", width=600, height=500)
st.write(fig1)
 #For bar plot-----------------------------------------------------------------------------------------
fig2 = px.bar(Ranked_resumes,
              x=Ranked_resumes['Name'], y=Ranked_resumes['Scores'], color='Scores',
              color_continuous_scale='haline', title="Score and Rank Distribution")
# fig.update_layout(width=700, height=700)
st.write(fig2)


st.markdown("---")

############################## RESUME PRINTING #############################

option_2 = st.selectbox("Show the Best Matching Resumes?", options=[
    'YES', 'NO'])
if option_2 == 'YES':
    indx = st.slider("Which resume to display ?:",
                     1, Ranked_resumes.shape[0], 1)

    st.write("Displaying Resume with Rank: ", indx)
    st.markdown("---")
    st.markdown("## **Resume** ")
    value = Ranked_resumes.iloc[indx-1, 2]


    st.write("With a Match Score of :", Ranked_resumes.iloc[indx-1, 6])
    fig = go.Figure(data=[go.Table(
        header=dict(values=["Resume"],
                    fill_color='#f0a500',
                    align='center', font=dict(color='black', size=16)),
        cells=dict(values=[str(value)],
                   fill_color='#f4f4f4',
                   align='left',font=dict(color='black')))])

    fig.update_layout(width=800, height=1200)
    st.write(fig)
    # st.text(df_sorted.iloc[indx-1, 1])
    st.markdown("---")

   