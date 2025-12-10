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
    Collect CPU-related information including per-core utilization.
    
    Returns:
        dict: Dictionary containing CPU metrics
            - cpu_cores: Physical CPU core count
            - cpu_frequency: CPU frequency in MHz
            - cpu_percent: CPU utilization percentage
            - cpu_status: Status level (green/orange/red) based on utilization
            - cpu_per_core: HTML table with per-core utilization
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
        
        # Get CPU usage percentage (overall)
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Determine status color based on utilization
        if cpu_percent <= 50:
            cpu_status = "green"
        elif cpu_percent <= 80:
            cpu_status = "orange"
        else:
            cpu_status = "red"
        
        # Get per-core/thread CPU utilization
        per_cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        
        # Generate HTML table for per-core utilization
        cpu_per_core_html = ""
        for core_index, core_percent in enumerate(per_cpu_percent, 1):
            # Determine color for each core
            if core_percent <= 50:
                core_status = "green"
            elif core_percent <= 80:
                core_status = "orange"
            else:
                core_status = "red"
            
            cpu_per_core_html += f"""                        <tr>
                            <td>Core {core_index}</td>
                            <td class="status-{core_status}">{core_percent:.1f}%</td>
                            <td><div class="progress-bar"><div class="progress-fill status-{core_status}" style="width: {core_percent}%"></div></div></td>
                        </tr>
"""
        
        return {
            "cpu_cores": cpu_cores,
            "cpu_frequency": cpu_frequency,
            "cpu_percent": f"{cpu_percent:.1f}",
            "cpu_status": cpu_status,
            "cpu_per_core": cpu_per_core_html
        }
    
    except Exception as e:
        print(f"Error collecting CPU information: {e}")
        return {
            "cpu_cores": "N/A",
            "cpu_frequency": "N/A",
            "cpu_percent": "0",
            "cpu_status": "green",
            "cpu_per_core": "<tr><td colspan='3'>CPU per-core data unavailable</td></tr>"
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
        
        # Get number of connected users (platform-specific)
        try:
            user_count = len(psutil.users())
        except (AttributeError, OSError):
            # Windows may not support psutil.users() in all configurations
            user_count = "N/A"
        
        # Get primary IP address
        try:
            # Connect to a public DNS server to determine primary IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            primary_ip = s.getsockname()[0]
            s.close()
        except Exception:
            primary_ip = "127.0.0.1"
        
        # Get load average (not available on Windows)
        try:
            load_avg = os.getloadavg()
            load_average_1 = f"{load_avg[0]:.2f}"
            load_average_5 = f"{load_avg[1]:.2f}"
            load_average_15 = f"{load_avg[2]:.2f}"
        except AttributeError:
            # Windows doesn't support os.getloadavg()
            # Use CPU percent as alternative metric
            cpu_percent = psutil.cpu_percent(interval=0.1)
            load_average_1 = f"{cpu_percent:.2f}"
            load_average_5 = "N/A (Windows)"
            load_average_15 = "N/A (Windows)"
        
        # Get current timestamp and generation date
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        generation_date = timestamp
        
        return {
            "hostname": hostname,
            "operating_system": operating_system,
            "uptime": uptime,
            "user_count": user_count,
            "primary_ip": primary_ip,
            "load_average_1": load_average_1,
            "load_average_5": load_average_5,
            "load_average_15": load_average_15,
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


def get_advanced_file_statistics(directory_path=None):
    """
    Advanced file analysis with 10 extensions, recursive exploration, and disk size calculation.
    
    Args:
        directory_path: Path to analyze. Defaults to sample_data directory.
    
    Returns:
        dict: Dictionary containing advanced file statistics
            - total_files: Total number of files analyzed
            - analysis_directory: Path analyzed
            - file_stats: HTML with file type distribution
            - total_size_mb: Total size of analyzed files in MB
            - file_sizes: HTML with size per file type
    """
    try:
        # Default to sample_data directory if not specified
        if directory_path is None:
            directory_path = "sample_data"
        
        # Check if directory exists
        if not os.path.exists(directory_path):
            print(f"Warning: Directory '{directory_path}' not found. Creating it...")
            os.makedirs(directory_path, exist_ok=True)
        
        # 10 file extensions to track with descriptions
        extensions = {
            '.txt': 'Text Documents',
            '.py': 'Python Scripts',
            '.pdf': 'PDF Documents',
            '.jpg': 'JPEG Images',
            '.png': 'PNG Images',
            '.md': 'Markdown Files',
            '.css': 'Stylesheets',
            '.exe': 'Executables',
            '.json': 'JSON Files',
            '.html': 'HTML Pages'
        }
        
        file_counts = {ext: 0 for ext in extensions}
        file_sizes = {ext: 0 for ext in extensions}  # Size in bytes
        total_files = 0
        total_size_bytes = 0
        
        # Recursively walk through all subdirectories
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                total_files += 1
                file_path = os.path.join(root, file)
                file_ext = Path(file).suffix.lower()
                
                # Get file size in bytes
                try:
                    file_size = os.path.getsize(file_path)
                    total_size_bytes += file_size
                except OSError:
                    file_size = 0
                
                # Count and accumulate size for each extension
                if file_ext in file_counts:
                    file_counts[file_ext] += 1
                    file_sizes[file_ext] += file_size
        
        # Avoid division by zero
        if total_files == 0:
            total_files = 1
        
        # Convert total size to MB
        total_size_mb = total_size_bytes / (1024 * 1024)
        
        # Generate HTML for file statistics with sizes
        file_stats_html = ""
        file_sizes_html = ""
        
        for ext, count in file_counts.items():
            percentage = (count / total_files) * 100
            size_bytes = file_sizes[ext]
            size_mb = size_bytes / (1024 * 1024)
            
            # File type distribution
            file_stats_html += f"""                <div class="file-stat-item">
                    <div class="extension">{ext}</div>
                    <div class="count">{count}</div>
                    <div class="percentage">{percentage:.1f}%</div>
                </div>
"""
            
            # File size per type
            file_sizes_html += f"""                <div class="file-stat-item">
                    <div class="extension">{ext}</div>
                    <div class="count">{size_mb:.2f} MB</div>
                    <div class="percentage">{(size_mb/total_size_mb*100):.1f}% of total</div>
                </div>
"""
        
        return {
            "total_files": total_files,
            "analysis_directory": directory_path,
            "file_stats": file_stats_html,
            "total_size_mb": f"{total_size_mb:.2f}",
            "file_sizes": file_sizes_html
        }
    
    except Exception as e:
        print(f"Error analyzing files: {e}")
        return {
            "total_files": "0",
            "analysis_directory": "N/A",
            "file_stats": "<div class='file-stat-item'>Error analyzing files</div>",
            "total_size_mb": "0.00",
            "file_sizes": "<div class='file-stat-item'>Error calculating sizes</div>"
        }


def get_largest_files(directory_path=None, limit=10):
    """
    Identify the largest files in the specified directory.
    
    Args:
        directory_path: Path to analyze. Defaults to sample_data directory.
        limit: Number of largest files to return (default 10)
    
    Returns:
        dict: Dictionary containing largest files information
            - largest_files_html: HTML table with top largest files
    """
    try:
        if directory_path is None:
            directory_path = "sample_data"
        
        if not os.path.exists(directory_path):
            return {
                "largest_files_html": "<tr><td colspan='3'>Directory not found</td></tr>"
            }
        
        # Collect all files with their sizes
        file_list = []
        
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    file_size = os.path.getsize(file_path)
                    file_list.append({
                        'name': file,
                        'path': file_path,
                        'size': file_size,
                        'size_mb': file_size / (1024 * 1024)
                    })
                except OSError:
                    continue
        
        # Sort by size descending and get top limit
        file_list.sort(key=lambda x: x['size'], reverse=True)
        top_files = file_list[:limit]
        
        # Generate HTML table
        largest_files_html = ""
        for rank, file_info in enumerate(top_files, 1):
            largest_files_html += f"""                        <tr>
                            <td>{rank}</td>
                            <td>{file_info['name']}</td>
                            <td>{file_info['size_mb']:.2f} MB</td>
                        </tr>
"""
        
        return {
            "largest_files_html": largest_files_html if largest_files_html else "<tr><td colspan='3'>No files found</td></tr>"
        }
    
    except Exception as e:
        print(f"Error analyzing largest files: {e}")
        return {
            "largest_files_html": f"<tr><td colspan='3'>Error: {str(e)}</td></tr>"
        }


def load_template(template_path="template.html"):
    """
    Load the HTML template file.
    
    Args:
        template_path: Path to the template file
    
    Returns:
        str: Content of the template file, or empty string if not found
    """
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Template file '{template_path}' not found")
        return ""
    except Exception as e:
        print(f"Error loading template: {e}")
        return ""

def substitute_variables(template_content, variables_dict):
    """
    Replace template variables with actual values.
    
    Template variables use the format: {{ variable_name }}
    
    Args:
        template_content: Content of the template with {{ }} placeholders
        variables_dict: Dictionary with variable names and their values
    
    Returns:
        str: Rendered HTML with variables substituted
    """
    try:
        html_content = template_content
        
        # Iterate through all variables and substitute them
        for variable_name, variable_value in variables_dict.items():
            placeholder = "{{ " + variable_name + " }}"
            html_content = html_content.replace(placeholder, str(variable_value))
        
        return html_content
    
    except Exception as e:
        print(f"Error substituting variables: {e}")
        return template_content

def write_html_file(html_content, output_path="index.html"):
    """
    Write the rendered HTML content to a file.
    
    Args:
        html_content: The HTML content to write
        output_path: Path where the HTML file will be saved
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return True
    except Exception as e:
        print(f"Error writing HTML file: {e}")
        return False

def main():
    """
    Main function to orchestrate the monitoring script.
    Collects all system information and generates the HTML dashboard.
    """
    
    print("=" * 60)
    print("Challenge Triple A - System Monitoring Dashboard")
    print("=" * 60)
    print()
    
    # Collect CPU information
    print("[*] Collecting CPU information...")
    cpu_data = get_cpu_information()
    
    print(f"    CPU Cores: {cpu_data['cpu_cores']}")
    print(f"    CPU Frequency: {cpu_data['cpu_frequency']}")
    print(f"    CPU Usage: {cpu_data['cpu_percent']}%")
    print()
    
    # Collect memory information
    print("[*] Collecting memory information...")
    memory_data = get_memory_information()
    
    print(f"    RAM Total: {memory_data['ram_total']}")
    print(f"    RAM Used: {memory_data['ram_used']}")
    print(f"    Memory Usage: {memory_data['memory_percent']}%")
    print()
    
    # Collect system information
    print("[*] Collecting system information...")
    system_data = get_system_information()
    
    print(f"    Hostname: {system_data['hostname']}")
    print(f"    Operating System: {system_data['operating_system']}")
    print(f"    Uptime: {system_data['uptime']}")
    print(f"    Connected Users: {system_data['user_count']}")
    print(f"    Primary IP: {system_data['primary_ip']}")
    print(f"    Load Average: {system_data['load_average_1']}, {system_data['load_average_5']}, {system_data['load_average_15']}")
    print()
    
    # Collect process information
    print("[*] Collecting process information...")
    top_processes = get_top_processes()
    print(f"    Top processes retrieved successfully")
    print()
    
    # Collect advanced file statistics
    print("[*] Analyzing files (10 extensions, recursive, with sizes)...")
    file_data = get_advanced_file_statistics()
    
    # Get largest files
    print("[*] Identifying largest files...")
    largest_files_data = get_largest_files()
    print(f"    Total files analyzed: {file_data['total_files']}")
    print(f"    Directory: {file_data['analysis_directory']}")
    print()
    
    # Load template
    print("[*] Loading template...")
    template = load_template()
    
    if not template:
        print("Error: Could not load template. Exiting.")
        return
    
    print("    Template loaded successfully")
    print()
    
    # Combine all data into a single dictionary
    print("[*] Preparing variables for substitution...")
    all_variables = {
        **cpu_data,
        **memory_data,
        **system_data,
        "top_processes": top_processes,
        **file_data,
        **largest_files_data
    }
    
    print(f"    Total variables to substitute: {len(all_variables)}")
    print()
    
    # Substitute variables
    print("[*] Substituting variables in template...")
    html_output = substitute_variables(template, all_variables)
    
    print("    Variables substituted successfully")
    print()
    
    # Write output HTML file
    print("[*] Writing HTML file...")
    success = write_html_file(html_output)
    
    if success:
        print("    HTML file generated successfully: index.html")
        print()
        print("=" * 60)
        print("Dashboard ready! Open index.html in your browser.")
        print("=" * 60)
    else:
        print("Error: Failed to write HTML file")


if __name__ == "__main__":
    main()