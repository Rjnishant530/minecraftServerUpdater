import os
import zipfile
from datetime import datetime
from dotenv import load_dotenv
import glob

# amazonq-ignore-next-line
def create_backup():
    # Load environment variables
    load_dotenv()
    minecraft_folder = os.getenv('MINECRAFT_FOLDER')
    backup_folder = '../backups'  # Local backup folder

    if not minecraft_folder:
        print("Error: MINECRAFT_FOLDER not set in environment variables")
        return False

    # Create backup folder if it doesn't exist
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
        print(f"Created backup folder: {backup_folder}")

    # Generate backup filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f'minecraft_world_backup_{timestamp}.zip'
    backup_path = os.path.join(backup_folder, backup_filename)
    world_path = os.path.join(minecraft_folder, 'world')

    # Check if world folder exists
    if not os.path.exists(world_path):
        print(f"Error: World folder not found at {world_path}")
        return False

    try:
        # Create new backup
        print(f"Creating backup of world...")
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(world_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, minecraft_folder)
                   
                    print(f"Adding {arcname}")
                    zipf.write(file_path, arcname)

        print(f"Backup created successfully: {backup_filename}")

        # Get list of existing backups
        existing_backups = glob.glob(os.path.join(backup_folder, 'minecraft_world_backup_*.zip'))
        existing_backups.sort(key=os.path.getctime)  # Sort by creation time

        # Remove oldest backups if we have more than 3
        while len(existing_backups) > 3:
            oldest_backup = existing_backups.pop(0)  # Remove and get oldest backup
            try:
                os.remove(oldest_backup)
                print(f"Removed old backup: {os.path.basename(oldest_backup)}")
            except Exception as e:
                print(f"Error removing old backup {oldest_backup}: {str(e)}")

        return True

   
    except Exception as e:
       
        print(f"Error creating backup: {str(e)}")
        if os.path.exists(backup_path):
            os.remove(backup_path)
        return False

def list_backups():
    """List all existing backups with their creation times."""
   
    backup_folder = 'backups'
    if not os.path.exists(backup_folder):
        print("No backups folder found.")
        return

    backups = glob.glob(os.path.join(backup_folder, 'minecraft_world_backup_*.zip'))
    if not backups:
        print("No backups found.")
        return

    print("\nExisting backups:")
    print("-" * 60)
    print(f"{'Backup Name':<40} {'Creation Date':<20}")
    print("-" * 60)
    
    for backup in sorted(backups, key=os.path.getctime):
        creation_time = datetime.fromtimestamp(os.path.getctime(backup))
        backup_name = os.path.basename(backup)
        print(f"{backup_name:<40} {creation_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)

if __name__ == "__main__":
    if create_backup():
        print("\nBackup completed successfully!")
        list_backups()
    else:
        print("\nBackup failed!")
