from manage import application, find_available_port

if __name__ == "__main__":
    from werkzeug.serving import run_simple
    port = find_available_port("0.0.0.0", 5000)
    run_simple("0.0.0.0", port, application,
               use_reloader=True, use_debugger=True)
