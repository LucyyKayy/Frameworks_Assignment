import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Try importing wordcloud
try:
    from wordcloud import WordCloud
    WORDCLOUD_AVAILABLE = True
except ImportError:
    WORDCLOUD_AVAILABLE = False

st.title("CORD-19 Data Explorer")
st.write("Interactive exploration of COVID-19 research papers (Sample Dataset)")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("metadata_sample.csv")
    df = df.dropna(subset=["title", "publish_time"])
    df["year"] = pd.to_datetime(df["publish_time"], errors="coerce").dt.year
    return df

df = load_data()

# --- Sidebar filters ---
years = sorted(df["year"].dropna().unique())
year_range = st.slider("Select year range", int(min(years)), int(max(years)), (2020, 2021))
filtered_df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

st.write(f"Showing {len(filtered_df)} papers between {year_range[0]} and {year_range[1]}")

# --- Visualizations ---
# Publications over time
year_counts = filtered_df["year"].value_counts().sort_index()
fig, ax = plt.subplots()
ax.bar(year_counts.index, year_counts.values)
ax.set_title("Publications by Year")
st.pyplot(fig)

# Top journals
top_journals = filtered_df["journal"].value_counts().head(10)
fig, ax = plt.subplots()
sns.barplot(y=top_journals.index, x=top_journals.values, ax=ax)
ax.set_title("Top Journals")
st.pyplot(fig)

# Word cloud (optional)
if WORDCLOUD_AVAILABLE:
    text = " ".join(filtered_df["title"].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    fig, ax = plt.subplots(figsize=(10,6))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    ax.set_title("Most Common Words in Titles")
    st.pyplot(fig)
else:
    st.warning("⚠️ WordCloud not installed. Skipping word cloud visualization.")

# Show sample data
st.subheader("Sample Data")
st.write(filtered_df.head(20))
