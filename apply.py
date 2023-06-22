import os
import time
import subprocess

def apply_kubernetes_file(file_path):
    subprocess.Popen(f'kubectl apply -f "{file_path}"', shell=True)
    print(f"Applied Kubernetes file: {file_path}")

def apply_kubernetes_files_in_order():

    def loop_through_files(file_names):
        for file_name in file_names:
            file_path = os.path.join(current_directory, "kubernetes", file_name)
            apply_kubernetes_file(file_path)
        
    current_directory = os.getcwd()
    
    # Define the file names in the desired order
    file_names = [
        "mongodb-deployment.yml",
        "mongodb-service.yml"]
    
    loop_through_files(file_names)
    
    time.sleep(10)  # Wait for 10 seconds between applying each file

    file_names = [
        "server-deployment.yml",
        "server-hpa.yml",
        "server-service.yml",
        "scraper-job.yml",
        "scraper-service.yml",
        "scraper-hpa.yml",
        "client-deployment.yml",
        "client-service.yml",
        "client-hpa.yml",
    ]

    loop_through_files(file_names)

# Run the function to apply the Kubernetes files in order
apply_kubernetes_files_in_order()
