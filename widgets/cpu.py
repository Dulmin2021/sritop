from textual.widgets import Static
from textual.reactive import reactive
import psutil

class CPUWidget(Static):
    """Widget to display CPU usage."""
    
    cpu_percent = reactive(0.0)

    def on_mount(self) -> None:
        self.update_timer = self.set_interval(1.0, self.update_cpu)

    def update_cpu(self) -> None:
        self.cpu_percent = psutil.cpu_percent()
        
    def render(self) -> str:
        bars = int(self.cpu_percent / 5)
        bar_str = "|" * bars + "-" * (20 - bars)
        
        try:
            load_avg = psutil.getloadavg()
            load_str = f"{load_avg[0]:.2f}, {load_avg[1]:.2f}, {load_avg[2]:.2f}"
        except Exception:
            load_str = "N/A"
            
        freq = psutil.cpu_freq()
        freq_str = f"{freq.current:.0f} MHz" if freq else "N/A"
            
        return (
            f"[b]CPU Usage[/b]\n\n"
            f"[{bar_str}] {self.cpu_percent}%\n"
            f"Freq: {freq_str}\n"
            f"Load Avg: {load_str}\n"
            f"Cores: {psutil.cpu_count(logical=False)} Physical / {psutil.cpu_count(logical=True)} Logical"
        )
