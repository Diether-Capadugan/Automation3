
import os
from flask import Flask, render_template, request
from netmiko import ConnectHandler


# Get the directory where api.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Locate the templates folder
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

# If templates is outside Automation3, check its parent directory
if not os.path.isfile(os.path.join(TEMPLATE_DIR, "index.html")):
    TEMPLATE_DIR = os.path.join(BASE_DIR, "..", "templates")
    TEMPLATE_DIR = os.path.abspath(TEMPLATE_DIR)


# Check if index.html exists
print("Project directory:", BASE_DIR)
print("Templates directory:", TEMPLATE_DIR)
print("Templates folder exists:", os.path.isdir(TEMPLATE_DIR))
print(
    "index.html exists:",
    os.path.isfile(os.path.join(TEMPLATE_DIR, "index.html"))
)


# Initialize Flask
app = Flask(__name__, template_folder=TEMPLATE_DIR)


@app.route("/", methods=["GET", "POST"])
def index():

    results = {}
    error = None
    success = False

    # Router configuration
    router_device = {
        'device_type': 'cisco_ios_telnet',
        'ip': '192.168.10.11',
        'port': 32770,
        'username': 'admin',
        'password': 'eve123',
        'secret': 'eve123',
    }

    # Commands to execute
    commands_to_run = [
        "show version",
        "show ip interface brief",
        "show running-config"
    ]

    # Execute commands when the button is clicked
    if request.method == "POST":

        net_connect = None

        try:
            print("\nConnecting to router...")

            net_connect = ConnectHandler(**router_device)

            # Enter privileged EXEC mode
            net_connect.enable()

            print("Connected successfully!")

            # Execute each command
            for cmd in commands_to_run:

                print(f"\nExecuting: {cmd}")

                output = net_connect.send_command(cmd)

                results[cmd] = output

            success = True

            print("\nAll commands executed successfully.")

        except Exception as e:

            error = f"Connection failed: {e}"

            print(error)

        finally:

            if net_connect:
                net_connect.disconnect()
                print("Disconnected from router.")

    # Display the webpage for both GET and POST requests
    return render_template(
        "index.html",
        results=results,
        error=error,
        success=success
    )


if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
