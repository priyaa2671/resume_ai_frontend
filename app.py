import openai
from flask import Flask, request, render_template

app = Flask(__name__)


def generate_description(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or the appropriate model
            messages=[{"role": "system", "content": f"Generate a detailed description for the following: {prompt}"}],
            max_tokens=150
        )
        return response.choices[0].message['content'].strip()
    except openai.error.RateLimitError as e:
        print(f"Rate limit exceeded: {e}")
        return "Rate limit exceeded. Please try again later."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_resume', methods=['POST'])
def create_resume():
    name = request.form['name']
    contact_info = request.form['contact_info']
    experience_prompt = request.form['experience']
    education_prompt = request.form['education']
    skills_prompt = request.form['skills']

    experience = generate_description(f"experience: {experience_prompt}")
    education = generate_description(f"education: {education_prompt}")
    skills = generate_description(f"skills: {skills_prompt}")

    resume = generate_resume(name, contact_info, experience, education, skills)
    return render_template('resume.html', resume=resume)

def generate_resume(name, contact_info, experience, education, skills):
    resume = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                padding: 20px;
                border: 1px solid #ddd;
                border-radius: 10px;
                max-width: 800px;
                margin: auto;
            }}
            h1 {{
                text-align: center;
                color: #333;
            }}
            h2 {{
                color: #666;
            }}
            p {{
                line-height: 1.6;
            }}
        </style>
    </head>
    <body>
        <h1>Resume</h1>
        <h2>{name}</h2>
        <p><strong>Contact Info:</strong> {contact_info}</p>
        <h2>Experience</h2>
        <p>{experience}</p>
        <h2>Education</h2>
        <p>{education}</p>
        <h2>Skills</h2>
        <p>{skills}</p>
    </body>
    </html>
    """
    return resume

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
