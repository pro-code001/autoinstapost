from instagrapi import Client

# ⛔️ Pastdagi login va parolni o'zingniki bilan almashtir!
USERNAME = "ishowuz"
PASSWORD = "76835710."

cl = Client()

# Login qilish
cl.login(USERNAME, PASSWORD)

# Sessiyani settings.json fayliga saqlash
cl.dump_settings("settings.json")

print("✅ Login muvaffaqiyatli. Sessiya settings.json fayliga saqlandi.")
