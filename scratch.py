import re
import os
import importlib

qmd_files = [f for f in os.listdir('examples') if f.endswith('.qmd')]
missing = []
for file in qmd_files:
    with open(os.path.join('examples', file), 'r') as f:
        content = f.read()
    imports = re.findall(r'^from landmapy\.(\w+) import (.*)$', content, re.MULTILINE)
    for mod_name, funcs_str in imports:
        # remove comments
        funcs_str = funcs_str.split('#')[0]
        funcs = [f.strip() for f in funcs_str.split(',')]
        
        try:
            mod = importlib.import_module(f'landmapy.{mod_name}')
        except ImportError:
            missing.append(f"{file}: module landmapy.{mod_name} not found")
            continue
        
        for func in funcs:
            if not func:
                continue
            if not hasattr(mod, func):
                missing.append(f"{file}: landmapy.{mod_name}.{func} not found")
for m in sorted(list(set(missing))):
    print(m)
print("Done")
