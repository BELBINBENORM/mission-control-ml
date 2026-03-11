# 🛰️ Mission Control ML
**A Detached Process Management & Real-Time Monitoring Engine for Jupyter**

Developed by **BELBIN BENO RM** [![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-IPython-orange)](https://ipython.org/)

Mission Control is a lightweight framework designed for Machine Learning Engineers and Data Scientists to launch long-running scripts (model training, ETL pipelines, Optuna tuning) as detached background processes. It features a live-streaming external dashboard that tracks logs and system resources without blocking your Jupyter Notebook execution.

---

## ✨ Key Features

* **🚀 Detached Execution:** Launch scripts as independent processes that bypass Python's Global Interpreter Lock (GIL).
* **🖥️ Live External Monitor:** Real-time log streaming to a perfectly centered, independent browser window.
* **🛡️ Smart Task Registry:** Prevents "orphan" processes by automatically managing PIDs and handling task restarts.
* **📊 Resource Tracking:** Integrated monitoring of CPU core allocation (Used vs. Pending cores).
* **🛑 Auto-Closing UI:** The external monitor window closes automatically when the engine is stopped from Python.

---

## 🚀 Quick Start

### Installation
Clone the repository and install in editable mode:
```bash
git clone [https://github.com/BELBINBENORM/mission-control-ml.git](https://github.com/BELBINBENORM/mission-control-ml.git)
cd mission-control-ml
pip install -e .
```
### 🚀 Notebook Installation (Kaggle / Colab / Jupyter)
Run this command in a code cell to install the library directly from GitHub:

```python
!pip install -q git+https://github.com/BELBINBENORM/mission-control-ml.git
```
---

## 🚀 Basic Usage

```python
from mission_control import MissionControl

# 1. Initialize and Start the External Monitor
mc = MissionControl()
mc.start_monitor(lines_count=5)

# 2. Launch ML tasks in the background
# These will stream logs to the external window automatically
mc.start_task("train_expert.py")
mc.start_task("data_processor.py")

# 3. Check Resource Status (Core Usage)
mc.active_tasks()

# 4. Graceful Shutdown (Kills all processes and closes UI window)
mc.stop_all()
```
---

## 📊 Resource Status Output
When calling `mc.active_tasks()`, you get a clear snapshot of your background engine:

```text
🛰️ MISSION CONTROL - RESOURCE STATUS
=======================================================
PID: 1024    | Process: 🖥️ monitor_engine.py (Monitor)
PID: 1025    | Process: ⚙️ train_expert.py
PID: 1026    | Process: ⚙️ data_processor.py
-------------------------------------------------------
📊 CORES: [Used: 3] | [Pending: 5] | [Total: 8]
=======================================================
```
---

## 📁 Repository Structure

* `mission_control.py`: The core module containing the `MissionControl` engine.
* `setup.py`: Package configuration for easy installation.
* `.gitignore`: Prevents temporary log files and caches from cluttering your repo.
---

## 📬 Contact & Support

**Author:** BELBIN BENO RM  
**Role:** Associate AI / ML Engineer  
**Email:** [belbin.datascientist@gmail.com](mailto:belbin.datascientist@gmail.com)  
**GitHub:** [BELBINBENORM](https://github.com/BELBINBENORM)
