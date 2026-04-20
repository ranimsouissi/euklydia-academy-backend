# test_veo.py
import google.generativeai as genai

genai.configure(api_key="AIzaSyDgKjt4uRE4P45lOoupc_I0O8QPIYBjZBg")

# Lister les modèles disponibles
for model in genai.list_models():
    if "veo" in model.name.lower() or "video" in model.name.lower():
        print(model.name)
        print(model.supported_generation_methods)
        print("---")