import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from textual.app import App, ComposeResult
from textual.containers import Grid, Horizontal, Vertical
from textual.widgets import Header, Footer
import psutil

from sritop.widgets.cpu import CPUWidget
from sritop.widgets.memory import MemoryWidget
from sritop.widgets.disk import DiskWidget
from sritop.widgets.network import NetworkWidget
from sritop.widgets.process import ProcessWidget

class SritopApp(App):
    """A Textual app for Sritop Next system monitor."""

    CSS_PATH = "sritop.tcss"
    TITLE = "Sritop Next"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Grid(id="main-grid"):
            with Vertical(id="left-pane"):
                yield CPUWidget(id="cpu")
                yield MemoryWidget(id="memory")
                yield DiskWidget(id="disk")
                yield NetworkWidget(id="network")
            with Vertical(id="right-pane"):
                yield ProcessWidget(id="processes")
        yield Footer()

if __name__ == "__main__":
    app = SritopApp()
    app.run()

