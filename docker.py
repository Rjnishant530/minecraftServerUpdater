import subprocess
import os

def stop_docker_compose():
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    try:
        print("Stopping Docker Compose services...")
        
        # Change to the script directory
        os.chdir(script_dir)
        
        # Run docker-compose down
       
        result = subprocess.run(
            ['docker', 'compose', 'down', '--remove-orphans'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        if result.returncode == 0:
            print("Successfully stopped all services")
            return True
        else:
            print(f"Error stopping services: {result.stderr}")
            return False
            
   
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def check_container_status():
    try:
       
        result = subprocess.run(
            ['docker', 'ps', '--format', '{{.Names}}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        running_containers = result.stdout.strip().split('\n')
        if running_containers and running_containers[0]:
            print("\nWarning: Some containers are still running:")
            for container in running_containers:
                print(f"- {container}")
        else:
            print("All containers are stopped")
            
   
    except Exception as e:
        print(f"Error checking container status: {str(e)}")

def start_docker_compose():
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    try:
        print("Starting Docker Compose services...")
        
        # Change to the script directory
        os.chdir(script_dir)
        
        # Run docker-compose up -d (detached mode)
       
        result = subprocess.run(
            ['docker', 'compose', 'up', '-d'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        if result.returncode == 0:
            print("Successfully started all services")
            return True
        else:
            print(f"Error starting services: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    if stop_docker_compose():
        check_container_status()
