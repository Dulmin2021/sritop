from textual.widgets import Static
import psutil

class DiskWidget(Static):
    """Widget to display Disk usage."""
    
    def on_mount(self) -> None:
        self.set_interval(2.0, self.refresh)

    def render(self) -> str:
        try:
            # We look at the partition holding the root/system
            # On windows this might be C:\\, but on linux it is '/'
            # Since this is a linux terminal monitor, we'll try '/' and fallback
            partitions = psutil.disk_partitions()
            path = '/'
            if any(p.mountpoint == 'C:\\' for p in partitions):
                path = 'C:\\'
                
            disk = psutil.disk_usage(path)
            percent = disk.percent
            bars = int(percent / 5)
            bar_str = "|" * bars + "-" * (20 - bars)
            return (
                f"[b]Disk Usage ({path})[/b]\n\n"
                f"[{bar_str}] {percent}%\n"
                f"Used: {disk.used / (1024**3):.2f} GB / {disk.total / (1024**3):.2f} GB\n"
                f"Free: {disk.free / (1024**3):.2f} GB"
            )
        except Exception as e:
            return f"Disk Info N/A: {e}"
