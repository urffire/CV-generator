from career_webpage import app
import os
import platform



if __name__ == '__main__':
    if platform.system() == 'Windows':
        # Windows file paths
        cert = os.path.join(app.root_path, 'cert\\server.crt')
        key = os.path.join(app.root_path, 'cert\\server.key')
    else:
        # MacOS (and Linux) file paths
        cert = os.path.join(app.root_path, 'cert/server.crt')
        key = os.path.join(app.root_path, 'cert/server.key')
    print(cert)
    app.run(debug=True, ssl_context=(cert, key))