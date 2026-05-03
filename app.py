import streamlit as st
from rembg import remove
from PIL import Image
import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# 1. Page Configuration
st.set_page_config(page_title="MMPS Fun Fair Photo Booth", page_icon="📸")
st.title("📸 MMPS Fun Fair 2026")
st.subheader("AI Photo Booth - Search & Email")

# 2. Sidebar Setup
st.sidebar.header("Background Gallery")

bg_options = {
    "MMPS Fun Fair 2026": "fair2026.jpg",
    "Brainrot": "brainrot.png",
    "Space Station": "space.jpg",
    "Tropical Beach": "beach.jpg",
    "Cyberpunk City": "cyber.jpg",
    "Minecraft World": "mc.png"
}

search_query = st.sidebar.text_input("🔍 Search backgrounds:", "")
filtered_options = [name for name in bg_options.keys() if search_query.lower() in name.lower()]

if filtered_options:
    selection = st.sidebar.selectbox("Choose your vibe:", filtered_options)
else:
    st.sidebar.warning("No backgrounds found!")
    selection = list(bg_options.keys())[0]

# 3. Main Camera Interface
img_file = st.camera_input("Take a photo!")

if img_file:
    input_image = Image.open(img_file)
    
    with st.spinner('AI is processing...'):
        try:
            # 4. Remove Background
            output_image = remove(input_image)
            
            # 5. Composite Image
            bg_path = bg_options[selection]
            background = Image.open(bg_path).convert("RGBA")
            background = background.resize(output_image.size)
            final_image = Image.alpha_composite(background, output_image)
            
            st.image(final_image, caption=f"Looking good in the {selection}!")
            
            # 6. Email Functionality
            st.divider()
            st.write("### 📧 Send to your phone")
            email_target = st.text_input("Enter email:")
            
            if st.button("Send Photo"):
                if email_target:
                    # Check if secrets are set in Streamlit Dashboard
                    if "SENDER_EMAIL" in st.secrets and "SENDER_PASSWORD" in st.secrets:
                        try:
                            # Prepare the email
                            msg = MIMEMultipart()
                            msg['Subject'] = f"Your MMPS Fun Fair Photo - {selection}"
                            msg['From'] = st.secrets["SENDER_EMAIL"]
                            msg['To'] = email_target
                            
                            text = MIMEText("Check out your AI photo from the MMPS Fun Fair 2026!")
                            msg.attach(text)
                            
                            # Convert PIL image to bytes for the attachment
                            buf = io.BytesIO()
                            final_image.save(buf, format="PNG")
                            img_data = buf.getvalue()
                            
                            image = MIMEImage(img_data, name=f"fun_fair_photo.png")
                            msg.attach(image)
                            
                            # Connect to Gmail Server
                            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                                server.login(st.secrets["SENDER_EMAIL"], st.secrets["SENDER_PASSWORD"])
                                server.sendmail(st.secrets["SENDER_EMAIL"], email_target, msg.as_string())
                            
                            st.success(f"✅ Sent! Check your inbox (and spam folder) {email_target}!")
                        except Exception as e:
                            st.error(f"Email failed: {e}")
                    else:
                        st.error("Secrets not found! Add SENDER_EMAIL and SENDER_PASSWORD to Streamlit Settings.")
                else:
                    st.warning("Please enter a valid email address.")
                    
        except Exception as e:
            st.error(f"Error: {e}")

st.sidebar.write("---")
st.sidebar.write("🎡 Built for MMPS Fun Fair 2026")
