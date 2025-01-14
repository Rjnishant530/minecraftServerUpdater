from dotenv import load_dotenv
from updateServer import updateServer
from docker import stop_docker_compose,check_container_status,start_docker_compose


load_dotenv('mmc4.env')

if stop_docker_compose():
        check_container_status()
else:
    print("Failed to stop Docker Compose.")
    quit()
    
updateServer()

load_dotenv('bmc4.env', override=True)

updateServer()

if start_docker_compose():
    check_container_status()
else:
    print("Failed to stop Docker Compose.")
    quit()