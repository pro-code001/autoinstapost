from instagrapi import Client

cl = Client()
cl.login("ishowuz", "76835710.")  # Email/SMS orqali kod keladi
cl.dump_settings("settings.json")  # Sessiyani JSON faylga saqlaydi
