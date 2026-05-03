import streamlit as st
from rembg import remove
from PIL import Image
import io
import smtplib
from email.message import EmailMessage
# --- CONFIGURATION ---
st.set_page_config(page_title="Coding Club Photo Booth", layout="centered")
st.title("🎡 Fun Fair AI Photo Booth")

# --- 1. SETTINGS & BACKGROUNDS ---
# Update these names to match the files in your 'backgrounds' folder!
bg_options = {
    "Space Station": "space.jpg",
    "Tropical Beach": "beach.jpg",
    "Cyberpunk City": "cyber.jpg",
    "Tung Tung Tung Sahur": "brainrot.png"
}

# SENDER EMAIL SETTINGS
SENDER_EMAIL = "mmpsfunfairbooth2026@gmail.com"  # <--- Put your Gmail here
SENDER_PASSWORD = "jiygbxfynjxubrnv"         # <--- Put your 16-digit App Password here

# --- 2. USER INTERFACE ---
with st.sidebar:
    st.header("Booth Settings")
    bg_choice = st.selectbox("Pick a Background:", list(bg_options.keys()))
    student_id = st.text_input("Enter Student ID Number:")

st.write("---")
picture = st.camera_input("Smile for the camera!")
st.write("---")

# --- 3. THE MAGIC LOGIC ---
if picture:
    if not student_id:
        st.warning("Please enter your Student ID before taking the photo!")
    else:
        # Step A: Load the photo
        input_image = Image.open(picture)
        
        with st.spinner("🤖 AI is swapping your background..."):
            try:
                # Step B: Remove the background (creates a transparent cutout)
                # First time running this can take 30-60 seconds to download AI model
                no_bg = remove(input_image)
                
                # Step C: Load and prepare the chosen background
                background = Image.open(bg_options[bg_choice]).convert("RGBA")
                background = background.resize(no_bg.size)
                
                # Step D: Composite (Merge) the images
                final_img = Image.alpha_composite(background, no_bg)
                
                # Display the result to the student
                st.image(final_img, caption="You look awesome!")
                
                # Step E: Prepare the image for emailing (convert to JPEG)
                img_byte_arr = io.BytesIO()
                final_img.convert("RGB").save(img_byte_arr, format='JPEG')
                final_image_bytes = img_byte_arr.getvalue()
                
                # --- 4. THE EMAIL SYSTEM ---
                recipient_email = f"{student_id}@gapps.yrdsb.ca" # <--- Update domain
                
                if st.button("📨 Send to My School Email"):
                    try:
                        msg = EmailMessage()
                        msg['Subject'] = "Your Fun Fair AI Photo! 🎡"
                        msg['From'] = SENDER_EMAIL
                        msg['To'] = recipient_email
                        msg.set_content(f"Hi {student_id}!\n\nAttached is your custom AI photo from the Fun Fair. Thanks for visiting the Coding Club Photo Booth!")
                        
                        msg.add_attachment(final_image_bytes, maintype='image', subtype='jpeg', filename=f"fun_fair_{student_id}.jpg")
                        
                        # Connect to Gmail Server
                        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
                            smtp.send_message(msg)
                            
                        st.success(f"Success! Photo sent to {recipient_email}")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Error sending email: {e}")
                        
            except FileNotFoundError:
                st.error(f"Background image not found! Check your 'backgrounds' folder for {bg_options[bg_choice]}")
            except Exception as e:
                st.error(f"Something went wrong with the AI: {e}")

else:
    st.info("Tip: Choose a background in the sidebar before you snap!")
