#!/usr/bin/env python3
"""
Challenge Triple A - System Monitoring Dashboard
Main monitoring script that collects system metrics and generates an HTML dashboard.

This script gathers CPU, memory, system, process, and file statistics,
then renders them into an HTML file using a template.
"""

import psutil
import os
import platform
import socket
from datetime import datetime
from pathlib import Path

def get_cpu_information():
    """
    Collect CPU-related information.
    
    Returns:
        dict: Dictionary containing CPU metrics
            - cpu_cores: Physical CPU core count
            - cpu_frequency: CPU frequency in MHz
            - cpu_percent: CPU utilization percentage
            - cpu_status: Status level (green/orange/red) based on utilization
    """
    try:
        # Get number of physical CPU cores
        cpu_cores = psutil.cpu_count(logical=False)
        
        # Get CPU frequency in MHz
        cpu_freq = psutil.cpu_freq()
        if cpu_freq:
            cpu_frequency = f"{cpu_freq.current:.0f} MHz"
        else:
            cpu_frequency = "N/A"
        
        # Get CPU usage percentage
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Determine status color based on utilization
        if cpu_percent <= 50:
            cpu_status = "green"
        elif cpu_percent <= 80:
            cpu_status = "orange"
        else:
            cpu_status = "red"
        
        return {
            "cpu_cores": cpu_cores,
            "cpu_frequency": cpu_frequency,
            "cpu_percent": f"{cpu_percent:.1f}",
            "cpu_status": cpu_status
        }
    
    except Exception as e:
        print(f"Error collecting CPU information: {e}")
        return {
            "cpu_cores": "N/A",
            "cpu_frequency": "N/A",
            "cpu_percent": "0",
            "cpu_status": "green"
        }

def get_memory_information():
    """
    Collect memory-related information.
    
    Returns:
        dict: Dictionary containing memory metrics
            - ram_total: Total RAM in GB
            - ram_used: Used RAM in GB
            - memory_percent: Memory utilization percentage
            - memory_status: Status level (green/orange/red) based on utilization
    """
    try:
        # Get memory information
        memory = psutil.virtual_memory()
        
        # Convert bytes to GB (1 GB = 1024^3 bytes)
        ram_total = memory.total / (1024**3)
        ram_used = memory.used / (1024**3)
        memory_percent = memory.percent
        
        # Determine status color based on utilization
        if memory_percent <= 50:
            memory_status = "green"
        elif memory_percent <= 80:
            memory_status = "orange"
        else:
            memory_status = "red"
        
        return {
            "ram_total": f"{ram_total:.2f} GB",
            "ram_used": f"{ram_used:.2f} GB",
            "memory_percent": f"{memory_percent:.1f}",
            "memory_status": memory_status
        }
    
    except Exception as e:
        print(f"Error collecting memory information: {e}")
        return {
            "ram_total": "N/A",
            "ram_used": "N/A",
            "memory_percent": "0",
            "memory_status": "green"
        }

def get_system_information():
    """
    Collect general system information.
    
    Returns:
        dict: Dictionary containing system metrics
            - hostname: Machine hostname
            - operating_system: OS distribution and version
            - uptime: System uptime in human-readable format
            - user_count: Number of connected users
            - primary_ip: Primary IP address
            - load_average_1: Load average (1 minute)
            - load_average_5: Load average (5 minutes)
            - load_average_15: Load average (15 minutes)
            - timestamp: Current timestamp
            - generation_date: Current date and time
    """
    try:
        # Get hostname
        hostname = socket.gethostname()
        
        # Get OS information
        os_name = platform.system()
        os_version = platform.release()
        operating_system = f"{os_name} {os_version}"
        
        # Calculate uptime
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime_delta = datetime.now() - boot_time
        
        # Format uptime as days, hours, minutes
        uptime_days = uptime_delta.days
        uptime_hours = uptime_delta.seconds // 3600
        uptime_minutes = (uptime_delta.seconds % 3600) // 60
        uptime = f"{uptime_days}d {uptime_hours}h {uptime_minutes}m"
        
        # Get number of connected users
        user_count = len(psutil.users())
        
        # Get primary IP address
        try:
            # Connect to a public DNS server to determine primary IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            primary_ip = s.getsockname()[0]
            s.close()
        except Exception:
            primary_ip = "127.0.0.1"
        
        # Get load average
        load_avg = os.getloadavg()
        
        # Get current timestamp and generation date
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        generation_date = timestamp
        
        return {
            "hostname": hostname,
            "operating_system": operating_system,
            "uptime": uptime,
            "user_count": user_count,
            "primary_ip": primary_ip,
            "load_average_1": f"{load_avg[0]:.2f}",
            "load_average_5": f"{load_avg[1]:.2f}",
            "load_average_15": f"{load_avg[2]:.2f}",
            "timestamp": timestamp,
            "generation_date": generation_date
        }
    
    except Exception as e:
        print(f"Error collecting system information: {e}")
        return {
            "hostname": "N/A",
            "operating_system": "N/A",
            "uptime": "N/A",
            "user_count": "N/A",
            "primary_ip": "N/A",
            "load_average_1": "N/A",
            "load_average_5": "N/A",
            "load_average_15": "N/A",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
