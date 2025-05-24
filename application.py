import os

from dotenv import load_dotenv

from src.main import app

if __name__ == "__main__":
    load_dotenv()
    PORT: int = int(os.getenv('PORT', default='5002'))
    app.run(host="0.0.0.0", port=PORT, debug=True)
