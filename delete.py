import os
import subprocess

current_directory = os.getcwd()
kubernetes_path = os.path.join(current_directory, "kubernetes")

subprocess.Popen(f'kubectl delete -f "{kubernetes_path}"', shell=True)