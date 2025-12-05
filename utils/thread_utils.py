"""
Thread utilities for non-blocking database operations
Prevents UI freezing during database queries
"""
import threading
from queue import Queue
import tkinter as tk

class BackgroundTask:
    """
    Execute database operations in background thread without blocking UI.
    Results are safely passed back to main thread via queue.
    """
    
    def __init__(self, root):
        """
        Initialize background task manager
        
        Args:
            root: Tkinter root window for scheduling UI updates
        """
        self.root = root
        self.result_queue = Queue()
        self.active_threads = []
    
    def run_async(self, task_func, callback=None, *args, **kwargs):
        """
        Run a function in background thread and optionally call callback with result.
        
        Args:
            task_func: Function to run in background (database query, etc.)
            callback: Function to call with result in main thread (UI update)
            *args, **kwargs: Arguments to pass to task_func
            
        Example:
            def query_db(mcu_id):
                return get_data_firmware(mcu_id)
            
            def update_ui(result):
                data, trans_time = result
                # Update UI with result
            
            task = BackgroundTask(root)
            task.run_async(query_db, update_ui, mcu_id="ABC123")
        """
        def worker():
            try:
                result = task_func(*args, **kwargs)
                if callback:
                    # Schedule callback in main thread
                    self.root.after(0, lambda: callback(result))
            except Exception as e:
                # Log error but don't crash
                print(f"Background task error: {e}")
                if callback:
                    self.root.after(0, lambda: callback(None))
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        self.active_threads.append(thread)
        
        # Clean up finished threads
        self.active_threads = [t for t in self.active_threads if t.is_alive()]
        
        return thread
    
    def run_sequence(self, tasks, on_complete=None):
        """
        Run a sequence of tasks in background, each waiting for previous to complete.
        
        Args:
            tasks: List of (task_func, args, kwargs) tuples
            on_complete: Callback when all tasks complete
            
        Example:
            tasks = [
                (get_data_firmware, (mcu_id,), {}),
                (get_data_pba, (mcu_id,), {}),
                (get_data_heater, (mcu_id,), {})
            ]
            task.run_sequence(tasks, on_complete=lambda: print("All done!"))
        """
        def worker():
            results = []
            for task_func, args, kwargs in tasks:
                try:
                    result = task_func(*args, **kwargs)
                    results.append(result)
                except Exception as e:
                    print(f"Task error: {e}")
                    results.append(None)
            
            if on_complete:
                self.root.after(0, lambda: on_complete(results))
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        return thread
    
    def wait_all(self, timeout=None):
        """
        Wait for all active threads to complete.
        
        Args:
            timeout: Maximum time to wait in seconds (None = wait forever)
        """
        for thread in self.active_threads:
            if thread.is_alive():
                thread.join(timeout=timeout)


class StageChecker:
    """
    Helper class for running stage checks with progress updates in background.
    Prevents UI freezing during sequential database queries.
    """
    
    def __init__(self, root, update_callback):
        """
        Args:
            root: Tkinter root window
            update_callback: Function called after each stage: callback(stage_key, result, trans_time)
        """
        self.root = root
        self.update_callback = update_callback
        self.background = BackgroundTask(root)
        self.is_cancelled = False
    
    def run_checks(self, mcu_id, stage_configs, on_complete=None):
        """
        Run all stage checks sequentially in background thread.
        
        Args:
            mcu_id: MCU ID to check
            stage_configs: List of (stage_key, query_func, log_name) tuples
            on_complete: Callback when all checks complete
            
        Example:
            configs = [
                ('FIRMWARE', get_data_firmware_P140, 'Firmware'),
                ('PBA', get_data_pba_function_P140, 'PBA Function'),
                # ...
            ]
            checker.run_checks(mcu_id, configs, on_complete=lambda: print("Done!"))
        """
        def worker():
            for stage_key, query_func, log_name in stage_configs:
                if self.is_cancelled:
                    break
                
                try:
                    # Run query in background
                    data, trans_time = query_func(mcu_id)
                    
                    # Update UI in main thread
                    self.root.after(0, lambda k=stage_key, d=data, t=trans_time: 
                                   self.update_callback(k, d, t))
                    
                    # Small delay between checks for UI responsiveness
                    import time
                    time.sleep(0.01)
                    
                except Exception as e:
                    print(f"Error checking {log_name}: {e}")
                    self.root.after(0, lambda k=stage_key: 
                                   self.update_callback(k, 'SKIP', None))
            
            if on_complete and not self.is_cancelled:
                self.root.after(0, on_complete)
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        return thread
    
    def cancel(self):
        """Cancel ongoing checks"""
        self.is_cancelled = True
