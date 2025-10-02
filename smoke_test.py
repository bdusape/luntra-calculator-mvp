#!/usr/bin/env python3
"""
Smoke test script to verify Streamlit app launches successfully
"""
import subprocess
import time
import sys
import signal

def run_smoke_test():
    """Run smoke test for Streamlit app"""
    try:
        print("🔥 Starting Streamlit smoke test...")
        
        # Start Streamlit process
        proc = subprocess.Popen([
            'streamlit', 'run', 'app.py', 
            '--server.headless', 'true', 
            '--server.port', '8502'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait 5 seconds for app to start
        time.sleep(5)
        
        # Check if process is still running
        if proc.poll() is None:
            print("✅ SUCCESS: Streamlit app started successfully")
            print("✅ App is running in headless mode on port 8502")
            
            # Terminate the process
            proc.terminate()
            proc.wait(timeout=5)
            
            print("✅ App terminated cleanly")
            return True
        else:
            # Process exited, get error output
            stdout, stderr = proc.communicate()
            print(f"❌ FAILED: App exited early")
            print(f"stdout: {stdout.decode()}")
            print(f"stderr: {stderr.decode()}")
            return False
            
    except FileNotFoundError:
        print("❌ FAILED: streamlit command not found. Is Streamlit installed?")
        return False
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

if __name__ == "__main__":
    success = run_smoke_test()
    sys.exit(0 if success else 1)