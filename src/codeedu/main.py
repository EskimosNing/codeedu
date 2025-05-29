'''
 # @ Author: Jianing ZHAO
 # @ Create Time: 2025-05-29 22:17:27
 # @ Modified by: Jianing ZHAO
 # @ Modified time: 2025-05-29 22:18:03
 # @ Description:
 '''
from flask import Flask
from flask_cors import CORS


from routes.chat import chat_bp
from routes.upload import upload_bp
from routes.conversation import convo_bp
from config.paths import OUTPUT_PATH, STORAGE_PATH
import os

app = Flask(__name__)
CORS(app)


os.makedirs(OUTPUT_PATH, exist_ok=True)
os.makedirs(STORAGE_PATH, exist_ok=True)

app.register_blueprint(chat_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(convo_bp)
app.register_blueprint(chat_bp)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)