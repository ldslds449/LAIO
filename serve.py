import argparse
import toml
import http.server
import socketserver

# get parameters
parser = argparse.ArgumentParser()
parser.add_argument("--config", "-c", type=str, default="config.toml", help="path of configure file")
parser.add_argument("--port", "-p", type=int, default=8086, help="http server's port")
args = parser.parse_args()

# load config
try:
  config = toml.load(args.config)
except:
  raise Exception("The configure file is not a toml file, or there is a syntax error.")

PORT = args.port
DIRECTORY = config["render"]["build_folder"]

class Handler(http.server.SimpleHTTPRequestHandler):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, directory=DIRECTORY, **kwargs)

# start http server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
  sa = httpd.socket.getsockname()
  print("Serving HTTP on", sa[0], "port", sa[1], "...")
  httpd.serve_forever()
