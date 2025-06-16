import streamlit as st
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
from detect_utils import load_models, detect_and_predict_mask
import av

st.set_page_config(page_title="Face Mask Detector", layout="centered")

# Title and description
st.title("🛡️ Real-Time Face Mask Detector")
st.markdown("""
Welcome to the real-time **Face Mask Detection** app!  
This app uses a webcam feed and a deep learning model to identify whether you're wearing a mask.

### 🔍 How it works:
- Detects faces using OpenCV DNN
- Classifies each face with a MobileNetV2-based model
- Works right from your **browser** using Streamlit + WebRTC

---
**👨‍💻 Built by:** Fahim Rahman  
**🧠 Model:** TensorFlow / Keras  
**📦 Tech Stack:** OpenCV, Streamlit, streamlit-webrtc  
""")

# Sidebar controls
st.sidebar.title("Controls")
run_camera = st.sidebar.checkbox("📷 Start Webcam", value=False)

# Load models only once
@st.cache_resource
def get_models():
    return load_models()

with st.spinner("Loading face detection and mask classification models..."):
    faceNet, maskNet = get_models()

# Define the WebRTC transformer
class MaskDetector(VideoTransformerBase):
    def transform(self, frame):
        image = frame.to_ndarray(format="bgr24")
        image = cv2.resize(image, (1080, 720))
        locs, preds = detect_and_predict_mask(image, faceNet, maskNet)

        for (box, pred) in zip(locs, preds):
            (startX, startY, endX, endY) = box
            (mask, withoutMask) = pred

            label = "Mask" if mask > withoutMask else "No Mask"
            confidence = max(mask, withoutMask)
            color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

            cv2.putText(image, f"{label}: {confidence*100:.2f}%", 
                        (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.7, color, 2)
            cv2.rectangle(image, (startX, startY), (endX, endY), color, 2)

        return image

# Start webcam
if run_camera:
    st.info("✅ Please select a device to turn on your video!")
    webrtc_streamer(
        key="mask-detect",
        video_transformer_factory=MaskDetector,
        media_stream_constraints={"video": True, "audio": False},
        async_transform=True,
    )
else:
    st.warning("📷 Webcam is turned off. Use the sidebar to enable it.")
    st.image(np.zeros((480, 640, 3), dtype=np.uint8), caption="Waiting for webcam...")
