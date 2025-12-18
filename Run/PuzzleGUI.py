import inspect
import os
import sys
import threading
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext

from Domain.Board.Grid import Grid
from Run.GameComponentFactory import GameComponentFactory

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)


class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, text):
        try:
            self.widget.configure(state="normal")
            self.widget.insert("end", text, (self.tag,))
            self.widget.see("end")
            self.widget.configure(state="disabled")
        except RuntimeError:
            # If called from thread and Tcl raises error
            pass

    def flush(self):
        pass


class PuzzleGUI:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("Puzzle Solver Launcher")
        self.root.geometry("900x700")

        # Set Environment Variable for Playwright Provider to avoid forcing headless
        os.environ["PUZZLE_SOLVER_GUI_MODE"] = "1"

        # URL Input
        input_frame = tk.Frame(root_window)
        input_frame.pack(pady=10, fill="x", padx=10)

        tk.Label(input_frame, text="Game URL:").pack(side="left")
        self.url_entry = tk.Entry(input_frame)
        self.url_entry.pack(side="left", fill="x", expand=True, padx=5)

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Queens", command=lambda: self.set_url("queens")).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Zip", command=lambda: self.set_url("zip")).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Tango", command=lambda: self.set_url("tango")).pack(side="left", padx=5)

        # Options Frame
        options_frame = tk.Frame(root)
        options_frame.pack(pady=5)

        self.record_video_var = tk.BooleanVar(value=False)
        tk.Checkbutton(options_frame, text="Enregistrer vidéo", variable=self.record_video_var).pack(
            side="left", padx=10
        )

        # Action Buttons
        action_frame = tk.Frame(root)
        action_frame.pack(pady=10)

        self.run_btn = tk.Button(
            action_frame,
            text="Start Solver",
            command=self.start_solver,
            bg="green",
            fg="white",
            font=("Arial", 12, "bold"),
        )
        self.run_btn.pack(side="left", padx=10)

        tk.Button(action_frame, text="Clear Log", command=self.clear_log).pack(side="left", padx=10)

        # Log Area
        self.log_area = scrolledtext.ScrolledText(root, state="disabled", font=("Consolas", 10))
        self.log_area.pack(expand=True, fill="both", padx=10, pady=10)

        # Redirect stdout/stderr
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        sys.stdout = TextRedirector(self.log_area)
        sys.stderr = TextRedirector(self.log_area)

    def set_url(self, name):
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, name)

    def clear_log(self):
        self.log_area.configure(state="normal")
        self.log_area.delete(1.0, tk.END)
        self.log_area.configure(state="disabled")

    def start_solver(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showwarning("Input Error", "Please enter a URL")
            return

        self.run_btn.config(state="disabled", text="Running...")
        thread = threading.Thread(target=self.run_logic, args=(url,))
        thread.daemon = True
        thread.start()

    def run_logic(self, url):
        try:
            os.environ["PLAYWRIGHT_RECORD_VIDEO"] = "True" if self.record_video_var.get() else "False"

            print(f"Starting solver for: {url}")

            if url == "queens":
                url = "https://www.linkedin.com/games/queens"
            elif url == "zip":
                url = "https://www.linkedin.com/games/zip"
            elif url == "tango":
                url = "https://www.linkedin.com/games/tango"

            import asyncio

            async def async_main():
                factory = GameComponentFactory()
                game_solver_class, data_game, game_player, playwright = await factory.create_components_from_url(url)

                print("Components created. Solving...")
                solver_instance = factory.create_solver(game_solver_class, data_game)

                start_time = time.time()
                solution = solver_instance.get_solution()
                end_time = time.time()

                if solution != Grid.empty():
                    print(f"Solution found in {end_time - start_time:.2f} seconds")
                    print(solution)
                    if game_player:
                        print("Playing solution in browser...")
                        if inspect.iscoroutinefunction(game_player.play):
                            await game_player.play(solution)
                        else:
                            await game_player.play(solution)
                        print("Execution complete.")
                        if hasattr(game_player, 'browser') and game_player.browser:
                            await game_player.browser.close()
                        if playwright:
                            await playwright.stop()
                else:
                    print("No solution found.")
                    # Close the browser context and playwright even if no solution
                    if playwright:
                        await playwright.stop()

            # Run the async code directly in this thread
            asyncio.run(async_main())

        except Exception as e:
            print(f"Error: {e}")
            import traceback

            traceback.print_exc()
        finally:
            # Schedule button reset on main thread
            self.root.after(0, lambda: self.run_btn.config(state="normal", text="Start Solver"))


if __name__ == "__main__":
    # Fix for frozen executable looking for browsers in internal dir
    if getattr(sys, "frozen", False):
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            playwright_path = os.path.join(local_app_data, "ms-playwright")
            if os.path.exists(playwright_path):
                os.environ["PLAYWRIGHT_BROWSERS_PATH"] = playwright_path
                print(f"Playwright browsers path forced to: {playwright_path}")

    root = tk.Tk()
    app = PuzzleGUI(root)

    try:
        import pyi_splash

        pyi_splash.close()
    except ImportError:
        pass

    root.mainloop()
