import subprocess
import sys
import os

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_and_install_requirements():
    print("🔍 Checking required packages...")
    
    required_packages = [
        "streamlit>=1.28.0",
        "numpy>=1.21.0", 
        "pandas>=1.3.0",
        "scikit-learn>=1.0.0",
        "beautifulsoup4>=4.10.0",
        "requests>=2.25.0",
        "lxml>=4.6.0"
    ]
    
    for package in required_packages:
        try:
            package_name = package.split(">=")[0].split("==")[0]
            if package_name == "scikit-learn":
                package_name = "sklearn"
            elif package_name == "beautifulsoup4":
                package_name = "bs4"
            
            __import__(package_name)
            print(f"✅ {package.split('>=')[0]} is already installed")
        except ImportError:
            print(f"📦 Installing {package}...")
            install_package(package)
            print(f"✅ {package.split('>=')[0]} installed successfully")

def setup_files():
    print("\n📂 Setting up data files...")
    
    import shutil
    
    source_dir = "AJAX-Movie-Recommendation-System-with-Sentiment-Analysis-master/AJAX-Movie-Recommendation-System-with-Sentiment-Analysis-master"
    
    files_to_copy = [
        "main_data.csv",
        "nlp_model.pkl", 
        "tranform.pkl"
    ]
    
    for file in files_to_copy:
        source_path = os.path.join(source_dir, file)
        dest_path = file
        
        if os.path.exists(source_path):
            shutil.copy2(source_path, dest_path)
            print(f"✅ Copied {file}")
        else:
            print(f"❌ Warning: {file} not found in source directory")
    
    print("📂 File setup complete!")

def run_streamlit():
    print("\n🚀 Starting Streamlit application...")
    print("📝 Note: You'll need a TMDb API key to use the app")
    print("🌐 Get your free API key from: https://www.themoviedb.org/settings/api")
    print("\n" + "="*50)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running Streamlit: {e}")

def main():
    print("🎬 Movie Recommendation System - Automated Setup")
    print("=" * 50)
    
    try:
        check_and_install_requirements()
        setup_files()
        
        print("\n✅ Setup complete!")
        choice = input("\n🚀 Do you want to run the Streamlit app now? (y/n): ").lower().strip()
        
        if choice in ['y', 'yes', '']:
            run_streamlit()
        else:
            print("\n📝 To run the app later, use: streamlit run streamlit_app.py")
            print("📚 Don't forget to get your TMDb API key!")
            
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        print("💡 Try running the individual steps manually:")
        print("   1. pip install -r requirements_streamlit.txt")
        print("   2. python setup_files.py")
        print("   3. streamlit run streamlit_app.py")

if __name__ == "__main__":
    main() 