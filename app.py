import streamlit as st


# NLP Pkgs
from textblob import TextBlob
import pandas as pd
from PIL import Image
# Emoji
import emoji

from bokeh.models.widgets import Div

# Web Scraping Pkg
from bs4 import BeautifulSoup
from urllib.request import urlopen

# Fetch Text From Url
@st.cache
def get_text(raw_url):
    page = urlopen(raw_url)
    soup = BeautifulSoup(page)
    fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
    return fetched_text

def get_value( my_key, my_dicts):
    for key, value in my_dicts.items():
        if my_key == key:
            return value

def get_key( my_value, my_dicts):
    for key, value in my_dicts.items():
        if my_value == value:
            return key
@st.cache
def lista_idiomas(idioma_original):
    df_idiomas = pd.read_csv('lista_idiomas.csv')
    dict_idiomas = {}
    linhas = len(df_idiomas)
    for i in range(0, linhas):
        if idioma_original != df_idiomas.iloc[i,1]:
            key = df_idiomas.iloc[i,0] # sigla 'pt'
            value = df_idiomas.iloc[i,1] # valor 'Portuguese'
            dict_idiomas[key] = value
    return dict_idiomas

@st.cache
def lista_idiomas_full():
    df_idiomas = pd.read_csv('lista_idiomas.csv')
    dict_idiomas = {}
    linhas = len(df_idiomas)
    for i in range(0, linhas):
        key = df_idiomas.iloc[i,0] # sigla 'pt'
        value = df_idiomas.iloc[i,1] # valor 'Portuguese'
        dict_idiomas[key] = value
    return dict_idiomas

def area_texto():
    raw_text = st.text_area("Copie e Cole o texto",'cole aqui')
    return raw_text

def main():
    """Text Analysis App """
    
    st.title("Language Detector & Translator")
    
    image = Image.open("people_speaking.jpg")
    st.sidebar.image(image,caption="Different languages", use_column_width=True)

    activities = ["Detector & Translator","About"]
    choice = st.sidebar.selectbox("Menu",activities)


    if choice == 'Detector & Translator':
        st.subheader("Text Area")
        lista_modos = ("For 23 languages","For selected languages")
        modo = st.sidebar.radio("Choose", lista_modos)
        texto_default = 'Text'
        raw_text = st.text_area("Copy&Paste -> Ctrl+Enter",texto_default)
        blob = TextBlob(raw_text)
        if modo == "For selected languages":
            #texto_default = 'Texto'
            #raw_text = st.text_area("Copy&Paste -> Ctrl+Enter",texto_default)
            #blob = TextBlob(raw_text)
            try:

                if (raw_text == " " or raw_text == "  " or raw_text == "   " or raw_text == "    "):
                    st.error("Please write something in the text area")
                elif (raw_text != texto_default) and len(raw_text)  > 0 and (raw_text != " " or raw_text != "  " or raw_text != "   " or raw_text != "    "):
                    dict_idioma_full = lista_idiomas_full()
            
                    idioma_original = get_value(blob.detect_language(),dict_idioma_full)
            
                    dict_idioma = lista_idiomas(idioma_original)
                    options = st.multiselect("Choose a language", tuple(dict_idioma.values()))
            
                    st.write("Original language:",idioma_original)
                    for i in range(len(options)):
                        value = options[i]
                        idioma_final = get_key(value, dict_idioma)
                        if (idioma_original != idioma_final):
                            texto_convertido = blob.translate(to=idioma_final)
                            st.success("Language"+": "+ value + " ("+idioma_final+")")
                            st.text(texto_convertido)
                    
            except:
                st.error("ERROR: text must be at least 3 letters and the word must exist in the formal language")

                    
        else:
            try:

                if (raw_text == " " or raw_text == "  " or raw_text == "   " or raw_text == "    "):
                    st.error("Please write something in the text area")
                elif (raw_text != texto_default) and len(raw_text)  > 0 and (raw_text != " " or raw_text != "  " or raw_text != "   " or raw_text != "    "):
                    dict_idioma_full = lista_idiomas_full()
            
                    idioma_original = get_value(blob.detect_language(),dict_idioma_full)
            
                    dict_idioma = lista_idiomas(idioma_original)
                    options = dict_idioma.values()
            
                    st.write("Original language:",idioma_original)
                    idioma_lista = list(options)
                    for i in range(len(idioma_lista)):
                        value = idioma_lista[i]
                        #st.text(value)
                        idioma_final = get_key(value, dict_idioma)
                        if (idioma_original != idioma_final):
                            texto_convertido = blob.translate(to=idioma_final)
                            st.success("Language"+": "+ value + " ("+idioma_final+")")
                            st.text(texto_convertido)
                    
            except:
                st.error("ERROR: text must be at least 3 letters and the word must exist in the formal language")


    if choice == 'About':
        st.subheader("I hope you enjoy it and use to learn something")
        st.subheader("Built with Streamlit and Textblob")
        st.subheader("by Silvio Lima")
        
        if st.button("Linkedin"):
            js = "window.open('https://www.linkedin.com/in/silviocesarlima/')"
            html = '<img src onerror="{}">'.format(js)
            div = Div(text=html)
            st.bokeh_chart(div)








if __name__ == '__main__':
    main()
