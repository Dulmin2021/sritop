#!/usr/bin/env python3
"""
Simple Terminal System Monitor - Like BTOP
A beautiful terminal-based system monitoring application
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static, DataTable
from textual.reactive import reactive
from rich.text import Text
import psutil
import time

class CPUWidget(Static):
    """Display CPU usage with a bar chart"""
    
    cpu_percent = reactive(0.0)
    
    def on_mount(self) -> None:
        self.update_cpu()
        self.set_interval(1, self.update_cpu)
    
    def update_cpu(self) -> None:
        self.cpu_percent = psutil.cpu_percent(interval=0.1)
    
    def render(self) -> str:
        bar_length = 40
        filled = int(bar_length * self.cpu_percent / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        # Color based on usage
        if self.cpu_percent < 50:
            color = "green"
        elif self.cpu_percent < 80:
            color = "yellow"
        else:
            color = "red"
        
        return f"[bold cyan]CPU Usage[/bold cyan]\n[{color}]{bar}[/{color}] {self.cpu_percent:.1f}%"


class MemoryWidget(Static):
    """Display memory usage"""
    
    mem_info = reactive(None)
    
    def on_mount(self) -> None:
        self.update_memory()
        self.set_interval(1, self.update_memory)
    
    def update_memory(self) -> None:
        self.mem_info = psutil.virtual_memory()
    
    def render(self) -> str:
        if not self.mem_info:
            return "Loading..."
        
        bar_length = 40
        filled = int(bar_length * self.mem_info.percent / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        # Color based on usage
        if self.mem_info.percent < 50:
            color = "green"
        elif self.mem_info.percent < 80:
            color = "yellow"
        else:
            color = "red"
        
        used_gb = self.mem_info.used / (1024**3)
        total_gb = self.mem_info.total / (1024**3)
        
        return f"[bold magenta]Memory Usage[/bold magenta]\n[{color}]{bar}[/{color}] {self.mem_info.percent:.1f}%\n{used_gb:.1f}GB / {total_gb:.1f}GB"


class DiskWidget(Static):
    """Display disk usage"""
    
    disk_info = reactive(None)
    
    def on_mount(self) -> None:
        self.update_disk()
        self.set_interval(2, self.update_disk)
    
    def update_disk(self) -> None:
        self.disk_info = psutil.disk_usage('/')
    
    def render(self) -> str:
        if not self.disk_info:
            return "Loading..."
        
        bar_length = 40
        filled = int(bar_length * self.disk_info.percent / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        # Color based on usage
        if self.disk_info.percent < 50:
            color = "green"
        elif self.disk_info.percent < 80:
            color = "yellow"
        else:
            color = "red"
        
        used_gb = self.disk_info.used / (1024**3)
        total_gb = self.disk_info.total / (1024**3)
        
        return f"[bold yellow]Disk Usage (/)[/bold yellow]\n[{color}]{bar}[/{color}] {self.disk_info.percent:.1f}%\n{used_gb:.1f}GB / {total_gb:.1f}GB"


class NetworkWidget(Static):
    """Display network statistics"""
    
    net_io = reactive(None)
    prev_net_io = None
    
    def on_mount(self) -> None:
        self.prev_net_io = psutil.net_io_counters()
        self.update_network()
        self.set_interval(1, self.update_network)
    
    def update_network(self) -> None:
        current = psutil.net_io_counters()
        
        if self.prev_net_io:
            bytes_sent = current.bytes_sent - self.prev_net_io.bytes_sent
            bytes_recv = current.bytes_recv - self.prev_net_io.bytes_recv
            
            self.net_io = {
                'sent': bytes_sent / 1024,  # KB/s
                'recv': bytes_recv / 1024   # KB/s
            }
        
        self.prev_net_io = current
    
    def render(self) -> str:
        if not self.net_io:
            return "[bold green]Network[/bold green]\nInitializing..."
        
        sent = self.net_io['sent']
        recv = self.net_io['recv']
        
        # Format with appropriate units
        if sent > 1024:
            sent_str = f"{sent/1024:.2f} MB/s"
        else:
            sent_str = f"{sent:.2f} KB/s"
        
        if recv > 1024:
            recv_str = f"{recv/1024:.2f} MB/s"
        else:
            recv_str = f"{recv:.2f} KB/s"
        
        return f"[bold green]Network[/bold green]\n↑ Upload: {sent_str}\n↓ Download: {recv_str}"


class ProcessTable(Static):
    """Display top processes"""
    
    def on_mount(self) -> None:
        self.update_processes()
        self.set_interval(2, self.update_processes)
    
    def update_processes(self) -> None:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort by CPU usage
        processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
        
        # Build table
        lines = ["[bold white]Top Processes (by CPU)[/bold white]"]
        lines.append("─" * 70)
        lines.append(f"{'PID':<8} {'Name':<25} {'CPU%':<10} {'MEM%':<10}")
        lines.append("─" * 70)
        
        for proc in processes[:10]:
            pid = proc['pid']
            name = (proc['name'] or 'N/A')[:24]
            cpu = proc['cpu_percent'] or 0
            mem = proc['memory_percent'] or 0
            
            # Color code CPU usage
            if cpu > 50:
                cpu_str = f"[red]{cpu:.1f}%[/red]"
            elif cpu > 20:
                cpu_str = f"[yellow]{cpu:.1f}%[/yellow]"
            else:
                cpu_str = f"[green]{cpu:.1f}%[/green]"
            
            lines.append(f"{pid:<8} {name:<25} {cpu_str:<19} {mem:.1f}%")
        
        self.update("\n".join(lines))


class sritop(App):
    """A Terminal System Monitor Application"""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    #top_panel {
        height: auto;
        background: $boost;
        padding: 1;
    }
    
    #stats_row {
        height: auto;
        margin: 1;
    }
    
    .stat_box {
        border: solid $primary;
        height: auto;
        padding: 1;
        margin: 0 1;
    }
    
    #process_panel {
        border: solid $primary;
        height: 1fr;
        margin: 1;
        padding: 1;
    }
    """
    
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
    ]
    
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        
        with Container(id="top_panel"):
            yield Static("[bold blue]System Monitor[/bold blue] - Press 'q' to quit, 'r' to refresh", id="title")
        
        with Horizontal(id="stats_row"):
            with Vertical(classes="stat_box"):
                yield CPUWidget()
            with Vertical(classes="stat_box"):
                yield MemoryWidget()
        
        with Horizontal(id="stats_row2"):
            with Vertical(classes="stat_box"):
                yield DiskWidget()
            with Vertical(classes="stat_box"):
                yield NetworkWidget()
        
        with Container(id="process_panel"):
            yield ProcessTable()
        
        yield Footer()
    
    def action_refresh(self) -> None:
        """Force refresh all widgets"""
        self.notify("Refreshing...")


if __name__ == "__main__":
    app = sritop()
    app.run()


