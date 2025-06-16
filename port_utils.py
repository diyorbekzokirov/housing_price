import socket

def find_available_port(start_port=8050, max_attempts=1000):
    """Find an available port starting from start_port"""
    port = start_port
    for _ in range(max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            port += 1
    
    # If no port found in range, try a random available port
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('127.0.0.1', 0))  # Let OS choose
            return s.getsockname()[1]
    except OSError:
        return 8050  # Fallback to default
