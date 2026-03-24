from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Fly.io yêu cầu port 8080, Render dùng $PORT
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
