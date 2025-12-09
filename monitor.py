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

def get_top_processes():
    """
    Get the top 3 processes with highest CPU and memory usage.
    
    Returns:
        str: HTML table rows with process information
    """
    try:
        # Get all processes and their resource usage
        process_list = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                process_list.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'cpu': proc.info['cpu_percent'] or 0,
                    'memory': proc.info['memory_percent'] or 0
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        # Sort by total resource usage (CPU + Memory)
        process_list.sort(key=lambda x: (x['cpu'] + x['memory']), reverse=True)
        
        # Get top 3 processes
        top_3 = process_list[:3]
        
        # Generate HTML table rows
        html_rows = ""
        for proc in top_3:
            html_rows += f"""                        <tr>
                            <td>{proc['name']}</td>
                            <td>{proc['pid']}</td>
                            <td>{proc['cpu']:.1f}%</td>
                            <td>{proc['memory']:.1f}%</td>
                        </tr>
"""
        
        return html_rows if html_rows else "<tr><td colspan='4'>No processes found</td></tr>"
    
    except Exception as e:
        print(f"Error collecting process information: {e}")
        return "<tr><td colspan='4'>Error collecting process data</td></tr>"

