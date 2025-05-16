import subprocess


#This code will work if custom command not found
def execute_system_command(command: str):
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
            )
        
        if result.stdout:
            print(result.stdout)
            
    except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr}")