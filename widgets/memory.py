from textual.widgets import Static
import psutil

class MemoryWidget(Static):
    """Widget to display Memory usage."""
    
    def on_mount(self) -> None:
        self.set_interval(1.0, self.refresh)

    def render(self) -> str:
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        mem_percent = mem.percent
        swap_percent = swap.percent
        
        def make_bar(percent):
            bars = int(percent / 5)
            return "|" * bars + "-" * (20 - bars)
            
        return (
            f"[b]Memory[/b]\n\n"
            f"RAM:  [{make_bar(mem_percent)}] {mem_percent}%\n"
            f"Used: {mem.used / (1024**3):.2f} GB / {mem.total / (1024**3):.2f} GB\n\n"
            f"[b]Swap[/b]\n"
            f"SWAP: [{make_bar(swap_percent)}] {swap_percent}%\n"
            f"Used: {swap.used / (1024**3):.2f} GB / {swap.total / (1024**3):.2f} GB"
        )
