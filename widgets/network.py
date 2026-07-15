from textual.widgets import Static
import psutil
import time

class NetworkWidget(Static):
    """Widget to display Network usage."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_net = None
        self.last_time = time.time()
        self.up_speed = 0.0
        self.down_speed = 0.0

    def on_mount(self) -> None:
        self.last_net = psutil.net_io_counters()
        self.set_interval(1.0, self.update_net)

    def update_net(self) -> None:
        current_net = psutil.net_io_counters()
        current_time = time.time()
        
        elapsed = current_time - self.last_time
        if elapsed > 0 and self.last_net:
            self.down_speed = (current_net.bytes_recv - self.last_net.bytes_recv) / elapsed
            self.up_speed = (current_net.bytes_sent - self.last_net.bytes_sent) / elapsed
            
        self.last_net = current_net
        self.last_time = current_time
        self.refresh()

    def format_bytes(self, bytes_per_sec):
        if bytes_per_sec < 1024:
            return f"{bytes_per_sec:.1f} B/s"
        elif bytes_per_sec < 1024**2:
            return f"{bytes_per_sec / 1024:.1f} KB/s"
        elif bytes_per_sec < 1024**3:
            return f"{bytes_per_sec / (1024**2):.1f} MB/s"
        else:
            return f"{bytes_per_sec / (1024**3):.1f} GB/s"

    def render(self) -> str:
        return (
            f"[b]Network Interfaces[/b]\n\n"
            f"▼ Download: {self.format_bytes(self.down_speed)}\n"
            f"▲ Upload:   {self.format_bytes(self.up_speed)}\n\n"
            f"Total DL: {self.last_net.bytes_recv / (1024**3):.2f} GB\n"
            f"Total UL: {self.last_net.bytes_sent / (1024**3):.2f} GB"
        )
