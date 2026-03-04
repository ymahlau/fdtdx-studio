import sys
import time
import socket
from playwright.sync_api import sync_playwright
import subprocess

def wait_for_server(port=8080, timeout=15.0):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection(("localhost", port), timeout=1.0):
                return True
        except OSError:
            time.sleep(0.1)
    return False

def test_logs():
    # Start the application as a background process
    print("Starting server...")
    proc = subprocess.Popen(["uv", "run", "python", "test_view_helper.py"], stdout=None, stderr=None)
    
    if not wait_for_server():
        print("Server did not start in time. Exiting.")
        proc.terminate()
        return

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()

            # Capture console messages
            def log_console(msg):
                print(f"BROWSER CONSOLE [{msg.type}]: {msg.text}")
            
            # Listen to page errors
            def log_error(err):
                print(f"BROWSER ERROR: {err}")

            page.on("console", log_console)
            page.on("pageerror", log_error)

            print("Navigating to http://localhost:8080...")
            page.goto("http://localhost:8080")
            
            # Wait for any potential scripts to run
            page.wait_for_selector('[id^="c"]', timeout=10000)
            
            # Retrieve available global variables
            eval_result = page.evaluate("() => Object.keys(window).filter(k => k.includes('getElement') || k.includes('vue') || k.includes('gui'))")
            print("Available globals related to Vue or GUI:", eval_result)
            
            # Test how to get the camera
            # Find the scene canvas
            scene_lookup = page.evaluate('''() => {
                const el = document.querySelector('[id^="c"]');
                if(!el) return "No element found";
                return el.id;
            }''')
            print("Scene element ID:", scene_lookup)

            camera_lookup = page.evaluate(f'''() => {{
                try {{
                    const el = document.getElementById("{scene_lookup}");
                    // How to find the VUE object? 
                    // Let's check vue properties
                    const props = Object.keys(el).filter(k => k.startsWith('__vue'));
                    return props.join(', ');
                }} catch(e) {{
                    return e.toString();
                }}
            }}''')
            print("Vue properties on DOM element:", camera_lookup)
            
            # Try to see if getElement is defined
            has_getElement = page.evaluate("() => typeof getElement")
            print("typeof getElement:", has_getElement)

            browser.close()
    finally:
        proc.terminate()

if __name__ == "__main__":
    test_logs()
