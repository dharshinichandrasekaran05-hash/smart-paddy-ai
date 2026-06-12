def chatbot_response(disease, query=""):

    d = disease.lower()

    response = {
        "blast": {
            "desc": "Rice Blast is a fungal disease caused by Magnaporthe oryzae affecting leaves, stems and panicles.",
            "solution": "Use Tricyclazole fungicide, avoid excess nitrogen, maintain proper field drainage."
        },

        "brown spot": {
            "desc": "Brown Spot is a fungal disease caused by Bipolaris oryzae due to poor soil nutrition.",
            "solution": "Apply balanced NPK fertilizer and improve soil health with organic compost."
        },

        "tungro": {
            "desc": "Rice Tungro is a viral disease spread by green leafhoppers.",
            "solution": "Remove infected plants immediately and control insect vectors using neem-based sprays."
        },

        "healthy": {
            "desc": "Your crop is healthy and shows no visible disease symptoms.",
            "solution": "Maintain proper irrigation and balanced fertilization to keep crop healthy."
        }
    }

    for key in response:
        if key in d:
            return response[key]

    return {
        "desc": "Disease not clearly identified.",
        "solution": "Please upload a clearer image or consult agriculture expert."
    }