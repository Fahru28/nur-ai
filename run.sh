#!/data/data/com.termux/files/usr/bin/bash

echo "🌙 Starting Nur AI..."
echo "📁 Directory: $(pwd)"
echo "🐍 Python version: $(python --version)"
echo ""

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ app.py not found in current directory!"
    echo "📁 Files in current directory:"
    ls -la
    exit 1
fi

if [ ! -f "response_engine.py" ]; then
    echo "❌ response_engine.py not found!"
    exit 1
fi

echo "✅ All files found!"
echo "🚀 Starting Flask server..."
echo "📱 Access at: http://localhost:5000"
echo "🛑 Press Ctrl+C to stop"
echo ""

python app.py
