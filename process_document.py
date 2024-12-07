import os
from application.extract_markdown import ExtractMarkdown

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from groq import Groq

prompt = """
Se te proporcionará el texto de un documento que describe un perfil laboral. El documento contiene las siguientes secciones: **Título**, **Organigrama**, **Funciones**, **Requisitos** y **Condiciones Laborales**. Tu tarea es extraer la información relevante y organizarla en un objeto JSON con el siguiente formato:

```json
{
    'Perfil': 'Nombre del perfil extraído del título del documento',
    'Organigrama': [
        'Item 1 de la sección Organigrama',
        'Item 2 de la sección Organigrama'
    ],
    'Funciones': [
        'Item 1 de la sección Funciones',
        'Item 2 de la sección Funciones'
    ],
    'Requisitos': [
        'Item 1 de la sección Requisitos',
        'Item 2 de la sección Requisitos'
    ],
    'Condiciones_laborales': [
        'Item 1 de la sección Condiciones Laborales',
        'Item 2 de la sección Condiciones Laborales'
    ]
}
```

### Detalles adicionales:
1. **Título:** Extrae el nombre del perfil del título del documento y colócalo en el campo `"Perfil"`.
2. **Organigrama:** Identifica los puntos clave relacionados con la estructura organizacional, como a quién reporta el perfil, personas bajo su cargo o relaciones con otros roles. Inclúyelos como elementos de la lista `"Organigrama"`.
3. **Funciones:** Lista las responsabilidades principales del perfil en forma de ítems claros y concisos en la lista `"Funciones"`.
4. **Requisitos:** Extrae las competencias, habilidades, experiencia y formación requeridas para el perfil, y organízalos en la lista `"Requisitos"`.
5. **Condiciones Laborales:** Identifica aspectos relacionados con horarios, ubicación, beneficios y otros términos laborales, y organízalos en la lista `"Condiciones_laborales"`.
6. No incluyas ningun comentario adicional en el resultado de la extracción, responde unicamente con el objeto JSON

### Ejemplo:
Si el texto proporcionado describe un "Perfil de Analista de Producción" con las siguientes secciones:

**Título:**  
Perfil de Analista de Producción  

**Organigrama:**  
- Reporta Gerencia directa.  
- 5 personas bajo su cargo.  

**Funciones:**  
- Elaborar y controlar el programa de producción semanal.  
- Gestionar el servicio de terceros.  

**Requisitos:**  
- Bachiller de Ingeniería Industrial.  
- 3 años de experiencia.  

**Condiciones Laborales:**  
- Régimen MYPE.  
- Sueldo fijo (2600 máx).  

El resultado JSON debe ser:

```json
{
    "Perfil": "Analista de Producción",
    "Organigrama": [
        "Reporta Gerencia directa.",
        "5 personas bajo su cargo."
    ],
    "Funciones": [
        "Elaborar y controlar el programa de producción semanal.",
        "Gestionar el servicio de terceros."
    ],
    "Requisitos": [
        "Bachiller de Ingeniería Industrial.",
        "3 años de experiencia."
    ],
    "Condiciones_laborales": [
        "Régimen MYPE.",
        "Sueldo fijo (2600 máx)."
    ]
}
```

Genera el objeto JSON siguiendo esta estructura y directrices. Si una sección no está claramente definida, indícalo con una lista vacía para esa sección. Asegúrate de que los resultados sean precisos, completos y estén organizados de manera estructurada.

Texto del documento que describe el perfil laboral a analizar:
{input_user}
"""

# from marker.converters.pdf import PdfConverter
# from marker.models import create_model_dict
# from marker.output import text_from_rendered

def extract_markdown(file_path:str, extractor: ExtractMarkdown):
    # converter = PdfConverter(
    #     artifact_dict=create_model_dict(),
    # )
    # rendered = converter(file_path)
    # # text, _, images = text_from_rendered(rendered)
    # return text_from_rendered(rendered)
    return extractor.extract(file_path)

def extract_json(content: str):
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),)
    
    prompt_formatted = prompt.replace("{input_user}", content)
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": prompt_formatted
            }
        ],
        temperature=1,
        max_tokens=8092,
        top_p=1,
        stream=True,
        stop=None,
    )

    result = ""
    for chunk in completion:
        result += chunk.choices[0].delta.content or ""

    return result

if __name__ == "__main__":
    text, _, images = extract_markdown(file_path="docs/Perfil de Analista de Producción[1].pdf")
    print(text)

    json_result = extract_json(content=text)
    print(json_result)