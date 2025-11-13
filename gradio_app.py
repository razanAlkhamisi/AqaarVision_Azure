import json
import requests
import gradio as gr
import os
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

# ------------------ CONFIG ------------------
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
UNIQUE_VALUES_PATH = "unique_values.json"

# ------------------ LOAD DROPDOWNS ------------------
with open(UNIQUE_VALUES_PATH, "r", encoding="utf-8") as f:
    unique_values = json.load(f)

regions = unique_values.get("المنطقة", [])
cities = unique_values.get("المدينة", [])
districts = unique_values.get("المدينة / الحي", [])
property_types = unique_values.get("تصنيف العقار", [])

# ------------------ PREDICTION FUNCTION ------------------
def predict_price(region, city, district, property_type, area, num_properties):
    payload = [
        {
            "المساحة": area,
            "عدد العقارات": num_properties,
            "المنطقة": region,
            "المدينة": city,
            "المدينة / الحي": district,
            "تصنيف العقار": property_type
        }
    ]
    
    response = requests.post(AZURE_ENDPOINT, json=payload)
    
    try:
        intermediate = json.loads(response.text)
        result_list = json.loads(intermediate)
        price = float(result_list[0])
        return f"Predicted Price: {price:,.0f} SAR"
    
    except Exception as e:
        return f"Error: {e}\nResponse content: {response.text}"

# ------------------ GRADIO INTERFACE ------------------
with gr.Blocks() as demo:
    gr.Markdown("## 🏡 Real Estate Price Prediction")
    
    with gr.Row():
        region_input = gr.Dropdown(label="المنطقة", choices=regions)
        city_input = gr.Dropdown(label="المدينة", choices=cities)
        district_input = gr.Dropdown(label="المدينة / الحي", choices=districts)
        property_type_input = gr.Dropdown(label="تصنيف العقار", choices=property_types)
    
    with gr.Row():
        area_input = gr.Number(label="المساحة (م²)", value=100)
        num_properties_input = gr.Number(label="عدد العقارات", value=1)
    
    output_text = gr.Textbox(label="Predicted Price")
    
    predict_button = gr.Button("Predict Price")
    predict_button.click(
        fn=predict_price,
        inputs=[region_input, city_input, district_input, property_type_input, area_input, num_properties_input],
        outputs=output_text
    )

# ------------------ FASTAPI WRAPPER ------------------
app = FastAPI()
app.mount("/", WSGIMiddleware(demo.server))  # Wrap Gradio as WSGI 

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
