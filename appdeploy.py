import streamlit as st
import os
import google.generativeai as genai
from supabase import create_client, Client

# Konfigurasi Halaman (Wajib ditaruh di paling awal setelah import)
st.set_page_config(
    page_title="Toko Tani Suka Maju",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="auto"
)

# Custom CSS
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* Background Pattern (Subtle Agriculture Theme) */
    .stApp {
        background-color: #FFFFFF; /* Base background */
        background-image: radial-gradient(#2E8B57 0.5px, transparent 0.5px), radial-gradient(#2E8B57 0.5px, #F0FFF0 0.5px);
        background-size: 20px 20px;
        background-position: 0 0, 10px 10px;
        color: #262730; /* Text Color */
    }

    /* Sidebar Background */
    [data-testid="stSidebar"] {
        background-color: #F0FFF0; /* Secondary Background */
        border-right: 1px solid #2E8B57;
    }

    /* Menyembunyikan elemen bawaan Streamlit yang tidak perlu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Modifikasi tombol agar lebih estetik */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background-color: #2E8B57; /* Primary Color */
        color: white;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #267345;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }
    
    /* Input Fields Focus Border */
    .stTextInput > div > div > input:focus {
        border-color: #2E8B57;
        box-shadow: 0 0 0 1px #2E8B57;
    }

    /* Chat Bubble Styling */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# Try to load .env file, but pass if module not found (Streamlit Cloud handles secrets differently)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Setup Supabase
try:
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error(f"Error connecting to Supabase: {e}")
    st.stop()

# Function to fetch and format shop data
def get_shop_info():
    # Static Info (Selalu tersedia)
    base_info = """
Nama Toko: Toko Tani Suka Maju
Alamat: Jl. Raya Pertanian No. 123, Desa Subur
Jam Operasional: Senin - Sabtu, 08:00 - 17:00 WIB
Kontak: 0812-3456-7890
"""
    
    # Dynamic Info (Ambil dari database Supabase)
    try:
        response = supabase.table('products').select("*").execute()
        products = response.data
        
        product_list = ""
        for i, p in enumerate(products, 1):
            product_list += f"{i}. Nama: {p['nama_produk']}\n"
            product_list += f"   - Kategori: {p['kategori_produk']} ({p['jenis_produk']})\n"
            # Format price safely (handle potential numeric/float types)
            price = p['harga']
            product_list += f"   - Harga: Rp {price:,} / {p['satuan_jual']}\n"
            product_list += f"   - Stok: {p['stok']}\n"
            
            if p.get('deskripsi'):
                product_list += f"   - Deskripsi: {p['deskripsi']}\n"
            
            if p.get('fungsi_produk'):
                product_list += f"   - Fungsi: {p['fungsi_produk']}\n"
                
            if p.get('peruntukan_produk'):
                product_list += f"   - Peruntukan: {p['peruntukan_produk']}\n"
                
            if p.get('bahan_aktif'):
                product_list += f"   - Bahan Aktif: {p['bahan_aktif']}\n"
                
            if p.get('cara_aplikasi'):
                product_list += f"   - Cara Aplikasi: {p['cara_aplikasi']}\n"
                
            product_list += "\n"
            
        final_info = f"""
{base_info}

Daftar Produk (Data Real-time dari Database):
{product_list}

Instruksi: Jawablah pertanyaan pelanggan dengan ramah berdasarkan data di atas. 
Jika pelanggan bertanya tentang produk yang tidak ada di daftar, katakan stok belum tersedia.
"""
        return final_info

    except Exception as e:
        # Jika database error, tetap kembalikan info toko + pesan error produk
        return f"""
{base_info}

Daftar Produk:
Maaf, data produk sedang tidak dapat diakses saat ini (Error Database).

Instruksi: Jawablah pertanyaan umum tentang toko (alamat, jam, kontak). 
Untuk produk, sampaikan permohonan maaf bahwa sistem sedang gangguan.
Error details: {e}
"""

st.title("Chatbot Toko Tani Suka Maju")

with st.chat_message("assistant", avatar="👨‍🌾"):
    st.write("Selamat Datang di Toko Tani Suka Maju. Ada yang bisa Saya Bantu?")

# Configure the Gemini API
try:
    shop_info = get_shop_info()
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        system_instruction=shop_info
    )
except Exception as e:
    st.error(f"Error configuring Gemini API: {e}")
    st.stop()


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Helper function to process message
def process_message(prompt):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        # 1. Convert Streamlit history to Gemini history format
        gemini_history = []
        for msg in st.session_state.messages[:-1]: # Exclude the just-added prompt
            role = "user" if msg["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": [msg["content"]]})
            
        # 2. Start Chat Session with History
        chat = model.start_chat(history=gemini_history)
        
        # 3. Send the new message
        response = chat.send_message(prompt)
        
        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Quick Chat Buttons
st.write("Pertanyaan Populer:")
if st.button("ℹ️ Informasi Toko (Jam, Alamat, Kontak)"):
    process_message("Tolong tuliskan informasi lengkap toko: Jam Operasional, Alamat, dan Nomor Kontak.")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    avatar = "👨‍🌾" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Apa yang ingin Anda tanyakan?"):
    # Display user message in chat message container
    st.chat_message("user", avatar="👤").markdown(prompt)
    
    # Process message (ini akan handle logic chat dengan memori)
    process_message(prompt)
    
    # Force rerun agar pesan terakhir muncul (karena process_message ubah session state tapi loop display sudah lewat)
    st.rerun()