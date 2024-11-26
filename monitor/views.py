import subprocess
import platform
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse

def get_processes():
    """Retrieve running processes with ID, Name, and CPU usage in JSON format."""
    if platform.system() == "Windows":
        # PowerShell command to get processes as JSON
        command = ["powershell", "-Command", "Get-Process | Select-Object Id, ProcessName, CPU | ConvertTo-Json"]
    else:
        # Linux command to get processes and format output as JSON
        command = ["ps", "-eo", "pid,comm,%cpu", "--no-headers"]

    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout.strip()
    
    if platform.system() == "Windows":
        # Parse JSON directly from PowerShell output
        return json.loads(output)
    else:
        # Parse Linux output into JSON
        processes = []
        for line in output.splitlines():
            parts = line.strip().split()
            if len(parts) >= 3:
                pid = parts[0]
                name = parts[1]
                # Asegurarse de que el CPU sea un número válido
                try:
                    cpu = float(parts[2])
                except ValueError:
                    cpu = 0.0
                processes.append({
                    "Id": int(pid),
                    "ProcessName": name,
                    "CPU": cpu
                })
        return processes
    
def list_processes(request):
    """View to list all processes in JSON format."""
    processes = get_processes()
    return render(request, 'monitor/process_list.html', {"processes": processes})

def stop_process(request, pid):
    """View to stop a specific process by its PID."""
    try:
        if platform.system() == "Windows":
            command = ["powershell", "-Command", f"Stop-Process -Id {pid} -Force"]
        else:
            command = ["kill", str(pid)]
        
        subprocess.run(command, check=True)
        return JsonResponse({"status": "success", "message": f"Process {pid} stopped."})
    except subprocess.CalledProcessError:
        return JsonResponse({"status": "error", "message": f"Could not stop process {pid}."})
