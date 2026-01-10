import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from supabase import create_client, Client

load_dotenv()

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
Nama Toko: Toko Tani A
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

st.title("Chatbot Toko Tani A (Supabase Connected)")

with st.chat_message("assistant"):
    st.write("Selamat Datang di Toko Tani A. Ada yang bisa Saya Bantu?")

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
        response = model.generate_content(prompt)
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
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Apa yang ingin Anda tanyakan?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        response = model.generate_content(prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response.text)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"An error occurred: {e}")