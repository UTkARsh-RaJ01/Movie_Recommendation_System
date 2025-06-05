import os
import shutil

def copy_files():
    files_to_copy = [
        ("static/model/nlp_model.pkl", "nlp_model.pkl"),
        ("static/model/tranform.pkl", "tranform.pkl"),
        ("static/model/main_data.csv", "main_data.csv")
    ]
    
    for source, dest in files_to_copy:
        if os.path.exists(source):
            shutil.copy2(source, dest)
            print(f"✅ Copied {source} to {dest}")
        else:
            print(f"❌ File not found: {source}")
    
    print("\n🎬 Setup complete! You can now run: streamlit run streamlit_app.py")

if __name__ == "__main__":
    copy_files() 