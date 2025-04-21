import streamlit as st
import os
import json
from werkzeug.utils import secure_filename

# Paths
DATA_FILE = "data/content.json"
IMAGE_DIR = "uploads/images"
VIDEO_DIR = "uploads/videos"

# Create folders if not exist
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs("data", exist_ok=True)

# Initialize JSON data if file not exist
if not os.path.exists(DATA_FILE) or os.stat(DATA_FILE).st_size == 0:
    with open(DATA_FILE, "w") as f:
        json.dump({"images": [], "videos": [], "facebook": []}, f)

# Load JSON
def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Save JSON
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# 🔒 Security & Styling
st.markdown("""
    <style>
    body {
        background-color: #f0f2f6;
    }
    .gallery-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 15px;
        margin-top: 20px;
    }
    .gallery-item {
        padding: 8px;
        border-radius: 10px;
        background: white;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    iframe {
        width: 100% !important;
        height: 450px !important;
        border-radius: 10px;
    }

    /* Responsive embed scaling for Facebook */
    .fb-wrapper {
        width: 100%;
        overflow: auto;
    }

    @media screen and (max-width: 768px) {
        iframe {
            height: 300px !important;
        }
    }
    </style>

""", unsafe_allow_html=True)

st.title("📸 Video & Image Gallery with Facebook Reactions")
menu = st.sidebar.selectbox("Select Page", ["Home", "Admin Panel"])

data = load_data()

if menu == "Admin Panel":
    st.header("🔐 Admin Panel")
    password = st.text_input("Enter Admin Password", type="password")
    if password == "admin123":

        # Upload Images
        image_files = st.file_uploader("Upload Images", accept_multiple_files=True, type=["jpg", "jpeg", "png"])
        if image_files:
            for file in image_files:
                filename = secure_filename(file.name)
                filepath = os.path.join(IMAGE_DIR, filename)
                with open(filepath, "wb") as f:
                    f.write(file.read())
                if filename not in data["images"]:
                    data["images"].append(filename)
            st.success("✅ Images uploaded successfully!")

                # Delete Image, Video, or Facebook Post (admin only)
        if st.checkbox("Delete Image/Video/Facebook Post"):
            st.subheader("Delete Post")
            
            # Delete images
            delete_image = st.selectbox("Select an image to delete", data["images"])
            if st.button(f"Delete Image {delete_image}"):
                if delete_image in data["images"]:
                    data["images"].remove(delete_image)
                    os.remove(os.path.join(IMAGE_DIR, delete_image))
                    st.success(f"✅ {delete_image} deleted successfully!")

            # Delete videos
            delete_video = st.selectbox("Select a video to delete", data["videos"])
            if st.button(f"Delete Video {delete_video}"):
                if delete_video in data["videos"]:
                    data["videos"].remove(delete_video)
                    os.remove(os.path.join(VIDEO_DIR, delete_video))
                    st.success(f"✅ {delete_video} deleted successfully!")

            # Delete Facebook Post
            delete_facebook = st.selectbox("Select a Facebook post to delete", data["facebook"])
            if st.button(f"Delete Facebook Post {delete_facebook}"):
                if delete_facebook in data["facebook"]:
                    data["facebook"].remove(delete_facebook)
                    st.success(f"✅ Facebook post deleted successfully!")

        save_data(data)

        # Upload Videos
        video_files = st.file_uploader("Upload Videos", accept_multiple_files=True, type=["mp4", "mov", "avi"])
        if video_files:
            for file in video_files:
                filename = secure_filename(file.name)
                filepath = os.path.join(VIDEO_DIR, filename)
                with open(filepath, "wb") as f:
                    f.write(file.read())
                if filename not in data["videos"]:
                    data["videos"].append(filename)
            st.success("✅ Videos uploaded successfully!")

        # Facebook Embed
        fb_code = st.text_area("Add Facebook Embed Code (iframe)")
        if st.button("Add Facebook Post"):
            if fb_code:
                data["facebook"].append(fb_code)
                st.success("✅ Facebook embed added!")

        save_data(data)
    else:
        st.error("❌ Wrong password")

else:
    st.header("🎨 Gallery")

    # Images
    st.subheader("🖼️ Images")
    if data["images"]:
        cols = st.columns(3)
        for index, img in enumerate(data["images"]):
            with cols[index % 3]:
                st.image(os.path.join(IMAGE_DIR, img), use_container_width=True)
    else:
        st.info("No images uploaded yet.")

    # Videos
    st.subheader("🎞️ Videos")
    if data["videos"]:
        cols = st.columns(3)
        for index, vid in enumerate(data["videos"]):
            with cols[index % 3]:
                st.video(os.path.join(VIDEO_DIR, vid))
    else:
        st.info("No videos uploaded yet.")

    # Facebook
    st.subheader("👍 Facebook Reactions")
    if data["facebook"]:
        cols = st.columns(3)
        for index, embed in enumerate(data["facebook"]):
            with cols[index % 3]:
                st.markdown(f'<div class="fb-wrapper">{embed}</div>', unsafe_allow_html=True)
    else:
        st.info("No Facebook posts added.")



