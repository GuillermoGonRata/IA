enfermedades = {
    "Asma": {
        "regla": lambda datos: datos["sibilancias"] and datos["tos"] == "Seca" and datos["alergias"],
        "certeza": 0.9
    },
    "Neumonía": {
        "regla": lambda datos: datos["fiebre"] and datos["tos"] == "Productiva" and datos["crepitantes"] and datos["edad"] > 65,
        "certeza": 0.85
    },
    "Bronquitis aguda": {
        "regla": lambda datos: datos["tos"] in ["Seca", "Productiva"] and datos["duracion_tos"] == "<3 días" and datos["rx_consolidacion"] == "No",
        "certeza": 0.75
    }
}

casos_prueba = [
    {"datos": {"sibilancias": True, "tos": "Seca", "alergias": True, "edad": 30}, "esperado": "Asma"},
    {"datos": {"fiebre": True, "tos": "Productiva", "crepitantes": True, "edad": 70}, "esperado": "Neumonía"},
    {"datos": {"tos": "Seca", "duracion_tos": "<3 días", "rx_consolidacion": "No"}, "esperado": "Bronquitis aguda"}
]