
import streamlit as st
import requests
from urllib.parse import quote

# =====================================
# GITHUB CONFIGURATION
# =====================================

GITHUB_USERNAME = "KrishnaSarovar"
REPO_NAME = "ml"
BRANCH = "main"

API_URL = (
    f"https://api.github.com/repos/"
    f"{GITHUB_USERNAME}/{REPO_NAME}/git/trees/{BRANCH}"
    "?recursive=1"
)

RAW_URL = (
    f"https://raw.githubusercontent.com/"
    f"{GITHUB_USERNAME}/{REPO_NAME}/{BRANCH}"
)

# =====================================
# STREAMLIT PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="Krishna - GitHub File Downloader",
    page_icon="📥",
    layout="wide"
)

st.title("📥 GitHub Repository File Downloader")

st.write(
    "Browse and download files directly "
    "from my GitHub repository."
)

st.markdown("---")

# =====================================
# FETCH FILES FROM GITHUB
# =====================================

@st.cache_data(ttl=60)
def fetch_github_files():

    response = requests.get(
        API_URL,
        headers={"Accept": "application/vnd.github+json"},
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    if data.get("truncated"):
        raise RuntimeError(
            "Repository is too large for a complete tree listing."
        )

    files = [
        item for item in data.get("tree", [])
        if item["type"] == "blob"
    ]

    return files


# =====================================
# DOWNLOAD FILE CONTENT
# =====================================

@st.cache_data(ttl=60)
def download_github_file(file_path):

    encoded_path = quote(file_path, safe="/")

    file_url = f"{RAW_URL}/{encoded_path}"

    response = requests.get(
        file_url,
        timeout=60
    )

    response.raise_for_status()

    return response.content


# =====================================
# MAIN APPLICATION
# =====================================

try:

    with st.spinner("Fetching files from GitHub..."):

        files = fetch_github_files()

    st.success(
        f"Successfully fetched {len(files)} files!"
    )

    st.markdown(
        f"**Repository:** "
        f"[{GITHUB_USERNAME}/{REPO_NAME}]"
        f"(https://github.com/{GITHUB_USERNAME}/{REPO_NAME})"
    )

    st.markdown("---")

    # =================================
    # SEARCH AND FILTER
    # =================================

    search = st.text_input(
        "🔍 Search File",
        placeholder="Enter file name..."
    )

    file_types = sorted(
        set(
            file["path"].split(".")[-1].lower()
            if "." in file["path"] else "no extension"
            for file in files
        )
    )

    selected_type = st.selectbox(
        "Filter by File Type",
        ["All Files"] + file_types
    )

    filtered_files = files

    if search:
        filtered_files = [
            file for file in filtered_files
            if search.lower() in file["path"].lower()
        ]

    if selected_type != "All Files":

        filtered_files = [
            file for file in filtered_files
            if (
                file["path"].split(".")[-1].lower()
                if "." in file["path"] else "no extension"
            ) == selected_type
        ]

    st.markdown("---")

    st.subheader("📂 Available Repository Files")

    st.write(
        f"Showing {len(filtered_files)} files"
    )

    # =================================
    # DISPLAY DOWNLOAD BUTTONS
    # =================================

    for index, file in enumerate(filtered_files):

        file_path = file["path"]

        file_name = file_path.split("/")[-1]

        file_size = file.get("size", 0)

        col1, col2, col3 = st.columns([5, 2, 2])

        with col1:

            st.write(f"📄 **{file_path}**")

        with col2:

            st.caption(
                f"{file_size / 1024:.2f} KB"
            )

        with col3:

            if st.button(
                "📥 Fetch",
                key=f"fetch_{index}"
            ):

                try:

                    with st.spinner(
                        f"Fetching {file_name}..."
                    ):

                        content = download_github_file(
                            file_path
                        )

                    st.session_state[
                        f"content_{index}"
                    ] = content

                    st.session_state[
                        f"filename_{index}"
                    ] = file_name

                except requests.exceptions.RequestException as e:

                    st.error(
                        f"Download error: {e}"
                    )

        # Display download button after fetching

        if f"content_{index}" in st.session_state:

            st.download_button(
                label=f"⬇️ Download {file_name}",
                data=st.session_state[
                    f"content_{index}"
                ],
                file_name=st.session_state[
                    f"filename_{index}"
                ],
                mime="application/octet-stream",
                key=f"download_{index}",
                use_container_width=True
            )

        st.markdown("---")


except requests.exceptions.RequestException as e:

    st.error(
        f"Unable to connect to GitHub: {e}"
    )

except Exception as e:

    st.error(
        f"Application Error: {e}"
    )


# =====================================
# FOOTER
# =====================================

st.caption(
    "Powered by Python, Streamlit and GitHub API"
)
