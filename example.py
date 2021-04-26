from grapp import Grapp

grapp = Grapp()
grapp.load_meta("meta.json")
grapp.init_cache()
grapp.run_server()