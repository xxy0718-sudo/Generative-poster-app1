import streamlit as st
import requests

# -----------------------------
# 🌍 Page Setup
# -----------------------------
st.set_page_config(page_title="Hyeongwol's Global Art Explorer", layout="centered")

st.title("🎨 Hyeongwol's Global Art Explorer")
st.markdown("Explore artworks from world-famous museums using open APIs.")

# -----------------------------
# 🎛️ Museum Selection
# -----------------------------
museum = st.selectbox(
    "Choose a Museum:",
    ["Metropolitan Museum of Art (New York)", "Rijksmuseum (Netherlands)", "Harvard Art Museums (USA)"]
)

query = st.text_input("🔍 Search for Artworks:", "flower")

# -----------------------------
# 🏛️ MET Museum
# -----------------------------
if museum == "Metropolitan Museum of Art (New York)" and query:
    st.subheader("🗽 MET Museum Results")
    search_url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?q={query}"
    response = requests.get(search_url).json()

    if response["total"] == 0:
        st.warning("No artworks found at the MET.")
    else:
        for object_id in response["objectIDs"][:5]:
            data = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}").json()
            st.image(data.get("primaryImageSmall"), width=300)
            st.markdown(f"**Title:** {data.get('title', 'Untitled')}")
            st.markdown(f"**Artist:** {data.get('artistDisplayName', 'Unknown')}")
            st.markdown(f"**Year:** {data.get('objectDate', 'Unknown')}")
            st.markdown(f"**Medium:** {data.get('medium', 'Unknown')}")
            st.divider()

# -----------------------------
# 🇳🇱 Rijksmuseum
# -----------------------------
elif museum == "Rijksmuseum (Netherlands)" and query:
    st.subheader("🇳🇱 Rijksmuseum Results")
    api_key = "0fiuZFh4"  # public demo key
    url = f"https://www.rijksmuseum.nl/api/en/collection?key={api_key}&q={query}&imgonly=True"
    response = requests.get(url).json()

    if "artObjects" not in response or len(response["artObjects"]) == 0:
        st.warning("No artworks found at the Rijksmuseum.")
    else:
        for item in response["artObjects"][:5]:
            st.image(item.get("webImage", {}).get("url"), width=300)
            st.markdown(f"**Title:** {item.get('title', 'Untitled')}")
            st.markdown(f"**Artist:** {item.get('principalOrFirstMaker', 'Unknown')}")
            st.markdown(f"**Link:** [View on Rijksmuseum Website]({item.get('links', {}).get('web')})")
            st.divider()

# -----------------------------
# 🏫 Harvard Art Museums
# -----------------------------
elif museum == "Harvard Art Museums (USA)" and query:
    st.subheader("🎓 Harvard Art Museums Results")
    api_key = "apikey=DEMO_KEY"  # Harvard allows demo usage
    url = f"https://api.harvardartmuseums.org/object?{api_key}&q={query}&size=5"
    response = requests.get(url).json()

    if "records" not in response or len(response["records"]) == 0:
        st.warning("No artworks found at Harvard Art Museums.")
    else:
        for rec in response["records"]:
            st.image(rec.get("primaryimageurl"), width=300)
            st.markdown(f"**Title:** {rec.get('title', 'Untitled')}")
            st.markdown(f"**Artist:** {rec.get('people', [{}])[0].get('name', 'Unknown') if rec.get('people') else 'Unknown'}")
            st.markdown(f"**Date:** {rec.get('dated', 'Unknown')}")
            st.markdown(f"**Medium:** {rec.get('medium', 'Unknown')}")
            st.divider()

# -----------------------------
# 🌸 Footer
# -----------------------------
st.markdown("---")
st.caption("Created by Hyeongwol • Powered by Streamlit + Open Museum APIs")
