# test_flask.py
print("Testing Flask installation...")

try:
    from flask import Flask
    print("✅ Flask imported successfully!")
    
    app = Flask(__name__)
    
    @app.route('/')
    def hello():
        return {"message": "Hello from Flask!"}
    
    print("✅ Flask app created!")
    print("\n🎉 Everything works! Now try your main app.")
    
except Exception as e:
    print(f"❌ Error: {e}")