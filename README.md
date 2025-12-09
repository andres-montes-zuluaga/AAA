# Challenge Triple A – System Monitoring Dashboard

## Description

A lightweight, real-time system monitoring dashboard that combines Linux administration, Python algorithms, and web display technologies. This project collects and visualizes critical system metrics in an interactive HTML dashboard.

**Triple A Challenge:**
- **Admin**: Linux VM management and configuration
- **Algo**: Python data collection and processing
- **Affichage**: HTML5/CSS3 web interface

## Prerequisites

- Ubuntu 22.04 LTS (or newer)
- Python 3.8+
- pip (Python package manager)
- Git
- Modern web browser

## Installation

### Clone the repository
```bash
git clone https://github.com/nombre-apellido/AAA.git
cd AAA
```

### Install Python dependencies
```bash
pip install psutil
```

## Usage

### Run the monitoring script
```bash
python3 monitor.py
```

This generates an `index.html` file with the latest system metrics.

### View the dashboard
Open `index.html` in your web browser.

## Features

- **System Information**: Hostname, OS, uptime, connected users
- **CPU Metrics**: Core count, frequency, utilization percentage
- **Memory Analysis**: RAM total/used, percentage with progress bars
- **Network Info**: Primary IP address
- **Process Monitoring**: Top 3 resource-intensive processes
- **File Analysis**: File type distribution in a selected directory

## Advanced Features

- Load average monitoring (load1, load5, load15)
- Per-core CPU utilization
- Recursive file analysis with 10+ extensions
- Disk space calculation by file type
- Color-coded status indicators (green/orange/red)
- Gauge.js visualization for CPU and disk
- Auto-refresh meta tag (30 seconds)

## Screenshots

- `screenshots/terminal.png` - Console output example
- `screenshots/index.png` - Dashboard display

## Challenges Encountered

- [ ] To be documented during development

## Possible Improvements

- [ ] API integration for remote monitoring
- [ ] Database storage for historical data
- [ ] Mobile app version
- [ ] Multi-server monitoring

## Author

[Your Name]

---

*Challenge Triple A - Educational Project*
