import streamlit as st
from scrape import (
    scrape_search,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from analyser import parse_with_ollama

st.set_page_config(page_title="Web Scraper", page_icon=":shopping_cart:")
st.title("E-commerce Scraper")

if "site" not in st.session_state:
    st.session_state.site = None
if "dom_content" not in st.session_state:
    st.session_state.dom_content = None

st.subheader("Select a Website:")
cols = st.columns(5)
sites = ["Amazon", "Flipkart", "Myntra", "Ajio", "Meesho"]
for col, sitename in zip(cols, sites):
    if col.button(sitename, key=f"site_{sitename}"):
        st.session_state.site = sitename
        st.session_state.dom_content = None

if st.session_state.site:
    st.markdown(f"**Selected Site:** {st.session_state.site}")
    query = st.text_input(f"What are you searching for on {st.session_state.site}?")

    if st.button("Go", key="go_button"):
        if not query:
            st.warning("Please enter a search term!")
        else:
            st.write(f"Scraping **{query}** on {st.session_state.site}…")
            raw_html = scrape_search(st.session_state.site, query)
            body = extract_body_content(raw_html)
            clean = clean_body_content(body)

            st.session_state.dom_content = clean

            with st.expander("View Cleaned content"):
                st.text_area("Here is all cleaned content", clean, height=300)

if st.session_state.dom_content:
    st.write("Do you want me to analyze this data?")
    if st.button("Yes, analyze", key="analyse_button"):
        st.write("Analyzing the data…")
        chunks = split_dom_content(st.session_state.dom_content)
        results = parse_with_ollama(chunks)
        st.subheader("Analysis Results")
        st.write(results)
