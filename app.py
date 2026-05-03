import streamlit as st
from rembg import remove
from PIL import Image
import io

# 1. Page Setup
st.set_page_config(page_title="MMPS Fun Fair Photo Booth", page_icon="📸")
st.title("📸 MMPS Fun Fair 2026")
st.subheader("AI Photo Booth - Custom Backgrounds")

# 2. Sidebar - Search and Selection
st.sidebar.header("Background Gallery")

# The list of backgrounds - Make sure these match your GitHub filenames exactly!
bg_options = {
    "MMPS Fun Fair 2026": "fair2026.jpg",
    "Brainrot": "brainrot.png",
    "Space Station": "space.jpg",
    "Tropical Beach": "beach.jpg",
    "Cyberpunk City": "cyber.jpg",
    "Minecraft World": "mc.png"
}

# Add a Search Bar in the sidebar
search_query = st.sidebar.text_input("🔍 Search backgrounds:", "")

# Filter the list based on the search query
filtered_options = [name for name in bg_options.keys() if search_query.lower() in name.lower()]

if filtered_options:
    selection = st.sidebar.selectbox("Choose your vibe:", filtered_options)
else:
    st.sidebar.warning("No backgrounds found with that name!")
    selection = list(bg_options.keys())[0] # Default to the first one if search is empty

# 3. Camera Input
img_file = st.camera_input("Take a photo!")

if img_file:
    input_image = Image.open(img_file)
    
    # Progress bar and spinner to keep the connection alive
    with st.spinner('AI is waking up and removing background... (Hold tight!)'):
        try:
            # 4. Remove Background
            output_image = remove(input_image)
            
            # 5. Load the Background
            bg_path = bg_options[selection]
            background = Image.open(bg_path).convert("RGBA")
            
            # Resize background to match photo
            background = background.resize(output_image.size)
            
            # Composite (Put the person on the background)
            final_image = Image.alpha_composite(background, output_image)
            
            # Display Result
            st.image(final_image, caption=f"Looking good in the {selection}!")
            
            # 6. Save/Email Section
            st.divider()
            email_target = st.text_input("Enter your email to get your photo:")
            if st.button("Email Me My Photo"):
                if email_target:
                    # Check if Secrets are configured in Streamlit Dashboard
                    if "SENDER_EMAIL" in st.secrets:
                        st.success(f"Sending to {email_target}...")
                        # Your email logic would go here
                    else:
                        st.error("Secrets not found! Check your Streamlit Dashboard Settings.")
                else:
                    st.warning("Please enter an email address.")
                    
        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.info("Try refreshing the page—the AI brain is still warming up.")

st.sidebar.write("---")
st.sidebar.write("Built for MMPS Fun Fair 2026 🎡")
