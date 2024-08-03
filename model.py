from flask import Flask, request, render_template
import google.generativeai as genai

app = Flask(__name__)

api_key = "AIzaSyBVec6inSuyB7rE4qOPdskMM_UTWQ525GM"
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 2,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def create_feedback_classification(feedback):
    prompt = f'''
    you are a sentiment classification model. refer the below example and classify feedback into "p" or "n" category. return only the category in output.
    ###
    feedback: what a lovely product
    sentiment: p
    ###
    feedback: what a worst product
    sentiment: n
    ###
    feedback: {feedback}
    sentiment:
    '''
    response = model.generate_content(prompt, generation_config={"temperature": 0.5})
    return response.text.strip()

@app.route("/", methods=["GET", "POST"])
def home():
    generated_content = ''
    if request.method == 'POST':
        feedback = request.form['prompt']
        if feedback:
            generated_content = create_feedback_classification(feedback)
    return render_template('home.html', generated_content=generated_content)

if __name__ == "__main__":
    app.run(debug=True)
