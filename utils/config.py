def get_config(fname="config.yml"):
  from yaml import safe_load
  with open(fname, 'r') as fh:
    config = safe_load(fh)
  return config