import os
import time
import json
import signal
import threading
import subprocess
import glob
import multiprocessing
from IPython.display import display, HTML

class MissionControl:
    """
    A detached process management engine for Jupyter Notebooks.
    Handles background workers and a live-streaming external dashboard.
    """
    def __init__(self, monitor_script='monitor_engine.py'):
        self.monitor_script = monitor_script
        self.log_name = 'monitor_engine.log'
        self.dashboard_file = 'dashboard.txt'
        self.monitor_pid = None
        self.registry = {}  # Format: {pid: "file_path.py"}
        self.total_cores = multiprocessing.cpu_count()

    # --- GLOBAL CONTROL ---

    def stop_all(self):
        """Stops the monitor and all tasks. Displays status if empty."""
        if not self.registry and not self.monitor_pid:
            print("ℹ️ No active tasks or monitor to stop.")
            return

        print("🛑 [SHUTDOWN] Terminating all tracked processes...")
        self.stop_monitor()
        for pid in list(self.registry.keys()):
            self.stop_task(pid)
        print("✨ Shutdown complete.")

    def active_tasks(self):
        """Displays all running processes and core usage status."""
        active_list = []
        
        # Check if Monitor is running
        if self.monitor_pid:
            active_list.append({"pid": self.monitor_pid, "name": f"🖥️ {self.monitor_script} (Monitor)"})
        
        # Add tasks from registry
        for pid, name in self.registry.items():
            active_list.append({"pid": pid, "name": f"⚙️ {name}"})

        used_cores = len(active_list)
        pending_cores = max(0, self.total_cores - used_cores)

        print("\n🛰️ MISSION CONTROL - RESOURCE STATUS")
        print("=" * 55)
        if not active_list:
            print("ℹ️ No active tasks running.")
        else:
            for item in active_list:
                print(f"PID: {item['pid']:<7} | Process: {item['name']}")
        
        print("-" * 55)
        print(f"📊 CORES: [Used: {used_cores}] | [Pending: {pending_cores}] | [Total: {self.total_cores}]")
        print("=" * 55)

    # --- MONITOR CONTROL ---

    def stop_monitor(self):
        """Kills the monitor process and triggers the browser to close the UI window."""
        if self.monitor_pid:
            self._kill_pid(self.monitor_pid, "Monitor")
            self.monitor_pid = None
        else:
            self._kill_by_name(self.monitor_script, "Monitor")
        
        # Push message to browser to close window
        display(HTML("<script>window.postMessage({type: 'close_monitor'}, '*');</script>"), 
                display_id="broadcaster_id")

    def start_monitor(self, lines_count=3, wrap=False):
        """Launches the detached monitoring engine and the JS-based dashboard."""
        self.stop_monitor()
        
        # Write the detached monitor script
        with open(self.monitor_script, 'w') as f:
            f.write(f"""import time, os, glob
while True:
    files = sorted(glob.glob("log_*.txt"))
    with open("{self.dashboard_file}", "w") as out:
        out.write(f"🛰️ MISSION CONTROL | {{time.strftime('%H:%M:%S')}}\\n")
        out.write("=============================================\\n")
        for f_name in files:
            if f_name == '{self.dashboard_file}' or not f_name.endswith('.txt'): continue
            out.write(f"📄 {{f_name}}\\n")
            try:
                with open(f_name, 'r') as f:
                    lines = f.readlines()[-{lines_count}:]
                    for line in lines:
                        out.write(f"  | {{line.strip()}}\\n")
            except: pass
            out.write("-" * 45 + "\\n")
    time.sleep(2)""")

        log_file = open(self.log_name, "w")
        process = subprocess.Popen(['python3', '-u', self.monitor_script], 
                                    stdout=log_file, stderr=log_file, preexec_fn=os.setsid)
        
        self.monitor_pid = process.pid
        print(f"✅ Monitor started (PID: {self.monitor_pid})")
        
        # Display the control UI
        white_space_style = "pre-wrap" if wrap else "pre"
        display(HTML(self._get_ui_html(white_space_style)))
        self._start_broadcaster()

    # --- TASK CONTROL ---

    def start_task(self, file_path):
        """Launches a script. If already running, restarts it automatically."""
        if not os.path.exists(file_path):
            print(f"❌ Error: File '{file_path}' not found.")
            return None

        # Auto-Restart: Kill existing PID for this file
        existing_pids = [p for p, name in self.registry.items() if name == file_path]
        for old_pid in existing_pids:
            print(f"♻️ Restarting: {file_path}...")
            self.stop_task(old_pid)

        # Start process
        task_log = open(f"{file_path}.log", "w")
        process = subprocess.Popen(['python3', '-u', file_path], 
                                    stdout=task_log, stderr=task_log, preexec_fn=os.setsid)
        
        pid = process.pid
        self.registry[pid] = file_path
        print(f"🚀 Task started: {file_path} (PID: {pid})")
        return pid

    def stop_task(self, pid):
        """Stops a task by PID. Prints warning if not active."""
        if pid in self.registry:
            name = self.registry[pid]
            self._kill_pid(pid, f"Task {name}")
            del self.registry[pid]
        else:
            print(f"⚠️ Task not at active: PID {pid} is not currently running.")

    # --- INTERNAL HELPERS ---

    def _kill_pid(self, pid, label):
        try:
            os.kill(pid, signal.SIGTERM)
            print(f"🛑 {label} stopped (PID: {pid})")
        except ProcessLookupError: pass

    def _kill_by_name(self, name, label):
        try:
            p_check = subprocess.check_output(["pgrep", "-f", name]).decode().split()
            for pid in p_check:
                os.kill(int(pid), signal.SIGTERM)
            if p_check: print(f"🛑 {label} stopped via pgrep")
        except: pass

    def _get_ui_html(self, white_space_style):
        """Generates the HTML/JS for the monitor button and window control."""
        return f'''
            <div style="padding: 15px; background: #111; border: 2px solid #ff4b4b; border-radius: 10px; width: 350px; display: flex; justify-content: center;">
                <button onclick="launchIndependentWindow()" 
                        style="background: #ff4b4b; color: white; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; 
                               display: flex; align-items: center; justify-content: center; gap: 10px; width: 100%; min-height: 45px; line-height: 1;">
                    🚀 OPEN EXTERNAL MONITOR
                </button>
            </div>
            <script>
            // Persistent window reference
            function launchIndependentWindow() {{
                window.monitorWin = window.open("", "ExternalMonitor", "width=600,height=700");
                window.monitorWin.document.write(`<html><head><style>body {{ background: #0e1117; color: #00ff00; font-family: monospace; padding: 20px; white-space: {white_space_style}; overflow-x: auto; }}</style></head><body><div id="content">Connecting...</div></body></html>`);
            }}
            
            // Singleton listener logic
            if (window.missionHandler) {{
                window.removeEventListener("message", window.missionHandler);
            }}
            
            window.missionHandler = function(e) {{
                if (e.data.type === "push_data" && window.monitorWin && !window.monitorWin.closed) {{
                    window.monitorWin.document.getElementById('content').innerText = e.data.content;
                }}
                if (e.data.type === "close_monitor" && window.monitorWin && !window.monitorWin.closed) {{
                    window.monitorWin.close();
                }}
            }};
            
            window.addEventListener("message", window.missionHandler);
            </script>
        '''

    def _start_broadcaster(self):
        """Background thread to push log data from Python to Browser JS."""
        def loop():
            while True:
                if os.path.exists(self.dashboard_file):
                    try:
                        with open(self.dashboard_file, "r") as f:
                            data = f.read()
                        display(HTML(f"<script>window.postMessage({{type: 'push_data', content: {json.dumps(data)}}}, '*');</script>"), 
                                display_id="broadcaster_id")
                    except: pass
                time.sleep(3)
        if not any(t.name == "BroadcasterThread" for t in threading.enumerate()):
            threading.Thread(target=loop, daemon=True, name="BroadcasterThread").start()
