import streamlit as st
from scrape import (
    scrape_search,
    extract_product_sections,
    clean_body_content,
    split_dom_content,
)
from analyser import parse_with_ollama

st.set_page_config(page_title="E-commerce Scraper")
st.title("E-commerce Scraper")

if "site" not in st.session_state:
    st.session_state.site = None
if "chunks" not in st.session_state:
    st.session_state.chunks = None
if "preview_data" not in st.session_state:
    st.session_state.preview_data = None

st.subheader("Select a Website:")
cols = st.columns(5)
sites = ["Amazon", "Flipkart", "Myntra", "Ajio", "Meesho"]
for col, name in zip(cols, sites):
    if col.button(name, key=f"site_{name}"):
        st.session_state.site = name
        st.session_state.chunks = None
        st.session_state.preview_data = None

if st.session_state.site:
    st.markdown(f"**Selected Site:** {st.session_state.site}")
    query = st.text_input(f"What are you searching for on {st.session_state.site}?")
    if st.button("Go", key="go_button"):
        if not query:
            st.warning("Please enter a search term!")
        else:
            with st.spinner(f"Searching for '{query}' on {st.session_state.site}..."):
                raw_html = scrape_search(st.session_state.site, query)
                sections = extract_product_sections(st.session_state.site, raw_html)
                st.write(f"Found {len(sections)} product cards on {st.session_state.site}")
                if not sections:
                    st.error("No cards found—check selector or page markup.")
                else:
                    cleaned_texts = [
                        clean_body_content(card_html)
                        for card_html in sections
                    ]
                    preview_data = "\n\n".join(cleaned_texts)
                    st.session_state.preview_data = preview_data
                    st.session_state.chunks = split_dom_content(preview_data, max_length=10000)

                    with st.expander("Preview All Cleaned Data"):
                        st.text_area("All Cleaned Product Data", preview_data, height=400)

if st.session_state.chunks:
    st.write("Do you want me to analyze this combined data?")
    if st.button("Yes, analyze", key="analyse_button"):
        print("Analyzing the data...")
        results = []
        total = len(st.session_state.chunks)
        with st.spinner("Analyzing combined data with Ollama..."):
            for i, chunk in enumerate(st.session_state.chunks, start=1):
                print(f"Analyzing chunk {i}/{total}...")
                st.write(f"Analyzing chunk {i}/{total}…")
                res = parse_with_ollama([chunk])
                if res:
                    results.append(res)
        final_output = "\n\n".join(results)
        print("Analysis complete.")
        print("you can now view the results.")
        st.subheader("Analysis Results")
        if final_output:
            st.write("Here are the extracted product details:")
            st.write(final_output)
        else:
            st.info("No relevant data found in the combined sections.")
