import yaml
import argparse
import time
import os
import collections.abc
import copy
def merge_config(config1, config2):
    if isinstance(config1, dict) and isinstance(config2, dict):
        result = {}
        all_keys = set(config1.keys())
        all_keys = all_keys | set(config2.keys())
        for k in all_keys:
            if k in config1:
                if k in config2:
                    result[k] = merge_config(config1[k], config2[k])
                    pass
                else:#not in config2
                    result[k] = config1[k]
                    pass
                pass
            else: #k not in config1, must in config 2
                assert k in config2
                result[k] = config2[k]
                pass
            pass
        return result
    elif isinstance(config1, list) and isinstance(config2, list) and len(config1) == len(config2):
        result = []
        for i in range(len(config1)):
            result.append(merge_config(config1[i], config2[i]))
            pass
        return result
    else:
        return config2
        pass
    pass
def resolve_config_inheritance(config, config_file):
    if isinstance(config, dict):
        result = {}
        for k,v in config.items():
            result[k] = resolve_config_inheritance(v, config_file)
            pass
        
        if "__inherits_from__" in result:
            inherits_from = result["__inherits_from__"]
            del result["__inherits_from__"]
            
            config_base = load_config_with_inheritance(os.path.join(os.path.dirname(config_file), inherits_from))
            result = merge_config(config_base, result)
            
            pass
        
        return result
    elif isinstance(config, list):
        result = []
        for v in config:
            result.append(resolve_config_inheritance(v, config_file))
            pass
        return result
    else:
        return config
    pass

def load_config_with_inheritance(config_file):
    with open(config_file) as f:
        config = yaml.safe_load(f)
        pass
    
    return resolve_config_inheritance(config, config_file)
  

def load_config_files(config_files):
    config_all = load_config_with_inheritance(config_files[0])
    for config in config_files[1:]:
        new_config = load_config_with_inheritance(config)
        config_all = merge_config(config_all, new_config)
        pass
    return config_all
