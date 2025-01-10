import os
import shutil
from dotenv import load_dotenv

load_dotenv()

minecraft_folder = os.getenv('MINECRAFT_FOLDER', 'bmc5')
temp_folder = os.getenv('TEMP_FOLDER', 'temp')

def replace_minecraft_folder():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    minecraft_path = os.path.join(script_dir, minecraft_folder)
    temp_path = os.path.join(script_dir, temp_folder)
    
   
    print(f"Using Minecraft folder: {minecraft_folder}")
    print(f"Using temp folder: {temp_folder}")
    
    try:
        # Check if temp folder exists
        if not os.path.exists(temp_path):
            print(f"Error: Temp folder not found at {temp_path}")
            return False
            
        # Check if minecraft folder exists
        if os.path.exists(minecraft_path):
            print(f"Removing current Minecraft folder: {minecraft_path}")
            try:
                shutil.rmtree(minecraft_path)
                print("Successfully removed current Minecraft folder")
            except PermissionError as e:
                print(f"Permission error: {str(e)}")
                print("Please ensure all files are closed and you have proper permissions")
                return False
            except Exception as e:
                print(f"Error removing Minecraft folder: {str(e)}")
                return False
        
        # Rename temp folder to minecraft folder
        try:
            print(f"Renaming temp folder to: {minecraft_path}")
            shutil.move(temp_path, minecraft_path)
            print("Successfully renamed temp folder to Minecraft folder")
            return True
        except Exception as e:
            print(f"Error renaming temp folder: {str(e)}")
            return False
            
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return False

def verify_folders():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    minecraft_path = os.path.join(script_dir, minecraft_folder)
    temp_path = os.path.join(script_dir, temp_folder)
    print("\nVerifying folders:")
    print(f"Temp folder exists: {os.path.exists(temp_path)}")
    print(f"Minecraft folder exists: {os.path.exists(minecraft_path)}")


def replace_folder():
    print("Starting folder replacement process...")
    verify_folders()
    if replace_minecraft_folder():
        print("\nFolder replacement completed successfully!")
        verify_folders()
    else:
        print("\nFolder replacement failed!")
        quit()
