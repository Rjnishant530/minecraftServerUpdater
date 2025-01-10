import os
import shutil
from dotenv import load_dotenv

load_dotenv()

minecraft_folder = os.getenv('MINECRAFT_FOLDER')
temp_folder = os.getenv('TEMP_FOLDER')

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

def copy_world_folder():
    try:

        if not minecraft_folder or not temp_folder:
            print("Error: MINECRAFT_FOLDER or TEMP_FOLDER environment variable not set")
            return False

        # Source world folder
        world_path = os.path.join(minecraft_folder, 'world')
        
        # Destination path
        dest_path = os.path.join(temp_folder, 'world')

        # Check if world folder exists
        if not os.path.exists(world_path):
            print(f"Error: World folder not found at {world_path}")
            return False
        
        if os.path.exists(dest_path):
            print(f"Removing existing world folder in temp directory")
            shutil.rmtree(dest_path)
            
        print(f"Copying world folder to {dest_path}")
        
        # Copy the world folder (overwrite if exists)
        shutil.copytree(world_path, dest_path)
        
        print("World folder copied successfully")
        return True

    except Exception as e:
        print(f"Error copying world folder: {str(e)}")
        quit()


def replace_folder():
    print("Starting folder replacement process...")
    verify_folders()
    if replace_minecraft_folder():
        print("\nFolder replacement completed successfully!")
        verify_folders()
    else:
        print("\nFolder replacement failed!")
        quit()
