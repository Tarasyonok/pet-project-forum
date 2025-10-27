# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = 2
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2

# Logging
accesslog = "-"  # Log to stdout
errorlog = "-"  # Log to stderr
loglevel = "info"

# Process naming
proc_name = "night_coder"

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None
