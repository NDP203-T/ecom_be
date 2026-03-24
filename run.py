from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Render cung cấp PORT qua environment variable
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
