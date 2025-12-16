# ussd_simulator.py - FULL OFFLINE USSD SIMULATOR FOR MSAIDIZI MKONONI
# No AT, No Twilio, No Internet — 100% Local
import sqlite3

DB_PATH = "data/services.db"

# === DATABASE HELPERS ===
def search_hospitals(county, level):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, phone FROM hospitals WHERE county = ? AND level = ?", (county, f"Level {level}"))
    results = c.fetchall()
    conn.close()
    return results

def get_kra_step(service):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT steps_sw FROM kra WHERE service LIKE ?", (f"%{service}%",))
    result = c.fetchone()
    conn.close()
    return result[0][:120] + "..." if result else "Hakuna maelezo."

def get_shif_info(topic):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT info_sw FROM shif WHERE topic LIKE ?", (f"%{topic}%",))
    result = c.fetchone()
    conn.close()
    return result[0][:120] + "..." if result else "Hakuna maelezo."

# === USSD MENU LOGIC ===
def ussd_menu(text=""):
    if not text:
        return "CON Karibu Msaidizi Mkononi! 🇰🇪\n1. Hospitali\n2. KRA\n3. Huduma\n4. SHIF\n0. Toka"
    
    if text == "1":
        return "CON Tafuta Hospitali:\n1. Nairobi\n2. Kisumu\n0. Rudi"
    
    if text == "1.1":
        return "CON Nairobi Level:\n1. Level 5\n2. Level 6\n0. Rudi"
    
    if text == "1.1.1":
        hospitals = search_hospitals("Nairobi", 5)
        menu = "CON Hospitali Nairobi Level 5:\n"
        for name, phone in hospitals[:3]:
            menu += f"• {name[:22]}... {phone}\n"
        menu += "0. Rudi"
        return menu
    
    if text == "2":
        return "CON KRA:\n1. PIN\n2. Ushuru\n0. Rudi"
    
    if text == "2.1":
        return f"END {get_kra_step('PIN')}"
    
    if text == "2.2":
        return f"END {get_kra_step('Ushuru')}"
    
    if text == "4":
        return "CON SHIF:\n1. Michango\n2. Kujiunga\n0. Rudi"
    
    if text == "4.1":
        return f"END {get_shif_info('Michango')}"
    
    if text == "4.2":
        return f"END {get_shif_info('kujiunga')}"
    
    if text == "0":
        return "END Asante! Karibu tena. 🇰🇪"
    
    return "CON Samahani, sielewi. 0. Rudi"

# === SIMULATOR LOOP ===
print("=" * 50)
print("   MSAIDIZI MKONONI USSD SIMULATOR")
print("   Dial: *711#  |  Offline | No Internet")
print("=" * 50)

text = ""
while True:
    menu = ussd_menu(text)
    print("\n" + menu)
    
    if "END" in menu:
        break
    
    user_input = input("\nYour choice → ").strip()
    
    if user_input == "0":
        print("\nEND Rudi nyumbani!")
        break
    
    if not text:
        text = user_input
    else:
        text += "." + user_input