from textual.widgets import DataTable
from textual.containers import Vertical
from textual.app import ComposeResult
import psutil

class ProcessWidget(Vertical):
    """Widget to display Process list."""
    
    def compose(self) -> ComposeResult:
        yield DataTable(id="process-table")

    def on_mount(self) -> None:
        self.table = self.query_one("#process-table", DataTable)
        self.table.add_columns("PID", "User", "CPU %", "Mem %", "Name")
        self.table.cursor_type = "row"
        self.update_processes()
        self.set_interval(2.0, self.update_processes)

    def update_processes(self) -> None:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
            try:
                pinfo = proc.info
                processes.append(pinfo)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
                
        # Sort by CPU percent descending
        processes.sort(key=lambda x: x.get('cpu_percent') or 0, reverse=True)
        
        self.table.clear()
        for p in processes[:100]:  # limit to top 100 for performance
            cpu = f"{p['cpu_percent']:.1f}" if p['cpu_percent'] is not None else "0.0"
            mem = f"{p['memory_percent']:.1f}" if p['memory_percent'] is not None else "0.0"
            self.table.add_row(
                str(p['pid']),
                str(p['username'])[:10] if p['username'] else "N/A",
                cpu,
                mem,
                str(p['name'])
            )
