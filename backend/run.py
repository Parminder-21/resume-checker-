# Backend runner script
import sys
import os

if __name__ == "__main__":
    # Ensure app can find modules
    sys.path.insert(0, os.path.dirname(__file__))
    
    try:
        import uvicorn
        print("Starting OptiResume AI Backend...")
        print("Listening on http://localhost:8000")
        print("API Docs: http://localhost:8000/docs")
        
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except ImportError as e:
        print(f"Error: Missing dependencies: {e}")
        print("\nRun SETUP.bat first to install requirements!")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
