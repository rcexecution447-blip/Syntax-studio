import discord
from discord.ext import commands
import google.generativeai as genai
import os
import re

# ================= KONFIGURASI =================
# Token & API Key yang sudah kamu berikan
DISCORD_TOKEN = "MTUwMzY5NjMzMjg1NzI3ODUyNA.GVQaN-.GBwnIBnDNHvB06jlHR1YitqOCkqAF1ofvp8nsE"
GEMINI_KEY = "AIzaSyAUplT6Z2KyzN-J21QIkRfpfcfpSFv0A_g"

# Inisialisasi AI (Gemini 1.5 Pro - Level Tertinggi)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

# Inisialisasi Bot Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Instruksi Sistem (The Singularity Intelligence)
SYSTEM_PROMPT = (
    "Nama kamu adalah Syntax AI (Singularity). Kamu adalah AI paling cerdas dan serba bisa.\n"
    "KEUNGGULAN UTAMA:\n"
    "- Melibas semua bahasa pemrograman: Python, Luau (Roblox Studio), JS, C++, PHP, dll.\n"
    "- Ahli dalam membuat Script Executor, Website Dashboard, dan Otomasi.\n"
    "- Mampu mengerjakan tugas sekolah/kuliah apapun dengan penjelasan yang keren.\n"
    "- Bisa membuat konsep visual, prompt thumbnail, dan alur video YouTube.\n"
    "INSTRUKSI KHUSUS:\n"
    "- Jika user ketik 'Ping', balas: 'Jarvis siap melayani kebutuhan anda'.\n"
    "- Selalu sertakan nama file di atas blok kode dengan format '### FILE: nama_file.ext'.\n"
    "- Gunakan gaya bicara yang profesional, dingin, namun sangat membantu (Cyberpunk Style)."
)

# ================= EVENT LOGIC =================

@bot.event
async def on_ready():
    # Tampilan di Terminal/Logs saat bot nyala
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"\033[1;36m")
    print(f"┌──────────────────────────────────────────┐")
    print(f"│      SYNTAX AI : SINGULARITY v2.0        │")
    print(f"├──────────────────────────────────────────┤")
    print(f"│ STATUS  : ONLINE (IMMORTAL MODE)         │")
    print(f"│ USER    : {bot.user}             │")
    print(f"│ SERVICE : READY TO SERVE MASTER          │")
    print(f"└──────────────────────────────────────────┘\033[0m")

@bot.event
async def on_message(message):
    # Respon Khusus: Ping
    if message.content.lower() == "ping":
        await message.channel.send("Jarvis siap melayani kebutuhan anda")
        return
    
    await bot.process_commands(message)

@bot.command()
async def syntax(ctx, *, prompt):
    """Perintah Utama: !syntax [instruksi]"""
    async with ctx.typing():
        try:
            # Mengirim permintaan ke AI
            full_prompt = f"{SYSTEM_PROMPT}\n\nUser Request: {prompt}"
            response = model.generate_content(full_prompt)
            ai_reply = response.text

            # Deteksi File Otomatis
            file_pattern = r"### FILE:\s*([\w\.-]+)\n+```(?:\w+)?\n(.*?)\n
```"
            extracted_files = re.findall(file_pattern, ai_reply, re.DOTALL)

            if extracted_files:
                # Kirim teks penjelasan
                clean_text = re.sub(file_pattern, "", ai_reply, flags=re.DOTALL).strip()
                if clean_text:
                    await ctx.send(clean_text[:2000])

                # Kirim file kodenya satu per satu
                for filename, code in extracted_files:
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(code.strip())
                    await ctx.send(f"✅ **Script Tercipta:** `{filename}`", file=discord.File(filename))
                    os.remove(filename) # Hapus dari server setelah dikirim
            else:
                # Jika hanya berupa teks (tugas sekolah atau penjelasan)
                if len(ai_reply) > 2000:
                    with open("syntax_response.txt", "w", encoding="utf-8") as f:
                        f.write(ai_reply)
                    await ctx.send("⚠️ Respons sangat panjang, silakan baca file ini:", file=discord.File("syntax_response.txt"))
                    os.remove("syntax_response.txt")
                else:
                    await ctx.send(ai_reply)

        except Exception as e:
            await ctx.send(f"❌ **System Error:** {str(e)}")

# Jalankan Bot
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)