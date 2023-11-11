import json
import time
import base64
import openai
import requests
import streamlit as st

from streamlit_option_menu import option_menu


st.set_page_config(page_title="Recipe Recommender")

with st.sidebar:
    choose = option_menu("Recipe Recommender", ["Home", "Starter", "Main Course", "Dessert"],
                         icons=["house", "dot", "dot", "dot"],
                         menu_icon="justify", default_index=0,
                         styles={"container": {"padding": "5!important", "background-color": "#000000"},
                                 "icon": {"color": "black", "font-size": "25px"}, 
                                 "nav-link": {"font-size": "16px","color": "#fafafa", "text-align": "left", "margin":"0px", "--hover-color": "grey"},
                                 "nav-link-selected": {"background-color": "#7EB02E"},
                                }
                        )

def header(Q1=None, Q2=None, Q3=None, Q4=None, food_type=None):

    header = st.container()
    model_training = st.container()
    form = st.form("Preference")

    with header:        
        
        with form:
            flavor = form.text_input(Q1)
            desired_ingredients = form.text_input(Q2)
            allergies = form.text_input(Q3)
            calorie = form.slider(Q4, min_value=10, max_value=1500, value=200, step=1)   
            submitted = form.form_submit_button("Get recipe!")

        if submitted == True:
            with model_training:
                
                prompt = f"Can you suggest a recipe with {flavor} flavor in type of {food_type}, that contains the ingredients: {desired_ingredients} but not including the {allergies}, approximately {calorie} calorie for one meal? Write name of the recipe at first lines, than ingredients with  list and preparation with step by step."
                # use your openai API key
                API_KEY = ""
                openai.api_key = API_KEY
                model = "text-davinci-002"
                response = openai.Completion.create(prompt = prompt, 
                                                    model = model,
                                                    max_tokens = 1000,
                                                    temperature = 0.2,
                                                    n = 1)
               
                st.subheader("Your recipe is:")

                progress_bar = st.progress(0)

                for percent_complete in range(100):
                    time.sleep(0.1)
                    progress_bar.progress(percent_complete + 1)
                
                for result in response.choices:
                    st.write(result.text)

question_1 = "Input the flavor you crave"
question_2 = "Mention ingredients"
question_3 = "Specify allergic ingredients if any"
question_4 = "Set calorie limit"


def Main_page():
    header = st.container()
    with header:
    
        st.markdown("<h1 style='text-align: center; color: #FFFF00;'>KITCHEN ASSISTANT</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: grey;'>List out ingredients and get your recipe <3</h3>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center; color: #6FAC0D;'>Select food type from sidebar</h5>", unsafe_allow_html=True)


def Starter():
    st.markdown("<h1 style='text-align: center; color: #FFFF00;'>STARTER RECOMMENDER</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: grey;'>Please make your selections for your starter recipe.</h3>", unsafe_allow_html=True) 
    header(Q1=question_1, Q2=question_2, Q3=question_3, Q4=question_4, food_type="starter")


def Main_Course():
    st.markdown("<h1 style='text-align: center; color: #FFFF00;'>MAIN COURSE RECOMMENDER</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: grey;'>Please make your selections for your main course recipe.</h3>", unsafe_allow_html=True)    
    header(Q1=question_1, Q2=question_2, Q3=question_3, Q4=question_4, food_type="main course")


def Dessert():
    st.markdown("<h1 style='text-align: center; color: #FFFF00;'>DESSERT RECOMMENDER </h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: grey;'>Please make your selections for your dessert recipe.</h3>", unsafe_allow_html=True)
    header(Q1=question_1, Q2=question_2, Q3=question_3, Q4=question_4, food_type="dessert")


page_names_to_funcs = {"MAIN PAGE": Main_page,
                       "STARTER": Starter, 
                       "MAIN COURSE": Main_Course, 
                       "DESSERT": Dessert
                      }

if choose == "Home":
    page_names_to_funcs["MAIN PAGE"]()

elif choose == "Starter":
    page_names_to_funcs["STARTER"]()

elif choose == "Main Course":
    page_names_to_funcs["MAIN COURSE"]()

elif choose == "Dessert":
    page_names_to_funcs["DESSERT"]()
