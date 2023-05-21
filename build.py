import os
import toml
import argparse
import shutil
import glob
from jinja2 import Environment, FileSystemLoader

# get parameters
parser = argparse.ArgumentParser()
parser.add_argument("--config", "-c", type=str, default="config.toml", help="path of configure file")
args = parser.parse_args()

# load config
try:
  config = toml.load(args.config)
except:
  raise Exception("The configure file is not a toml file, or there is a syntax error.")

# check output folder
if not os.path.exists(config["render"]["build_folder"]):
   os.makedirs(config["render"]["build_folder"])

# render
env = Environment(loader=FileSystemLoader(config["render"]["template_folder"]))
template = env.get_template(config["render"]["file"])
output_from_parsed_template = template.render(links=config["link"], **config["parameter"])

# clean the build fodler
for f in glob.glob(os.path.join(config["render"]["build_folder"], "*")):
  if os.path.isfile(f):
    os.remove(f)

# save the results
with open(os.path.join(config["render"]["build_folder"], config["render"]["file"]), "w") as f:
  f.write(output_from_parsed_template)

# copy the static files
for f in glob.glob(os.path.join(config["render"]["static_folder"], "*")):
  shutil.copy(f, config["render"]["build_folder"])

print("Finish")