from flask import Flask, jsonify, render_template
import openai
import logging

openai.api_key = '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'

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generateimages/<prompt>')
def generate(prompt):
    try:
        app.logger.info("Received prompt: %s", prompt)
        response = openai.Image.create(prompt=prompt, n=5, size="256x256")

        # Check for errors in the OpenAI API response
        if 'error' in response:
            error_message = response['error']['message']
            app.logger.error("OpenAI API error: %s", error_message)
            return jsonify({"error": f"OpenAI API Error: {error_message}"}), 500

        app.logger.info("OpenAI API response: %s", response)
        return jsonify(response), 200
    except Exception as e:
        app.logger.error("Error generating images: %s", str(e))
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5087)
