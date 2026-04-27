# Rendering Quarto Markdown with Python (Jupyter)

When rendering Quarto `.qmd` documents that use the Python (Jupyter) engine, there is no direct, native Quarto YAML option (like `fig-path` in Knitr) to cleanly specify a custom image output folder (e.g., `examples/images/madison`). 

By default, Pandoc will always extract embedded Jupyter media into a relative directory structured as `[filename]_files/figure-[format]/` during the rendering process.

If you need to place your generated `.png` files in a custom, clean directory structure, you can use one of the two approaches below:

## Approach 1: Save Figures Manually in Python (Recommended)

The cleanest and most robust approach is to use Python to explicitly save the plots to your desired directory. This gives you full control over the filenames and locations directly within the code.

**For Matplotlib / GeoPandas plots:**
```python
import os
import matplotlib.pyplot as plt

# Ensure the custom directory exists
os.makedirs("images/madison", exist_ok=True)

# Generate your plot
plot_gdf_state(redlining_gdf)

# Save the plot explicitly
plt.savefig("images/madison/redlining_state.png")
```

**For HoloViews plots:**
```python
import os
import holoviews as hv

os.makedirs("images/madison", exist_ok=True)

madison_hv = (ndvi_hv + pred_hv + grade_hv)
hv.save(madison_hv, 'images/madison/madison_hv.png')
```

## Approach 2: Use a Quarto Post-Render Hook

If you prefer not to add `savefig` to every single Python cell in your notebook, you can write a `post-render` script that automatically moves the images and updates the markdown links in the generated `.md` file after Quarto finishes rendering.

In your `.qmd` YAML header, add a post-render script hook:
```yaml
---
title: "Madison"
jupyter: python3
post-render:
  - python3 scripts/move_images.py madison
---
```

Then create a Python script (`scripts/move_images.py`) that handles the file operations and markdown link updates:

```python
import os
import sys
import shutil
import re

if len(sys.argv) < 2:
    print("Please provide the document basename.")
    sys.exit(1)

filename = sys.argv[1] # e.g., 'madison'
source_dir = f"{filename}_files/figure-markdown"
target_dir = f"images/{filename}"
md_file = f"{filename}.md"

if os.path.exists(source_dir):
    os.makedirs(target_dir, exist_ok=True)
    
    # 1. Move the image files
    for img in os.listdir(source_dir):
        shutil.move(os.path.join(source_dir, img), os.path.join(target_dir, img))
        
    # 2. Clean up the old empty directory
    shutil.rmtree(f"{filename}_files")
    
    # 3. Update the markdown links in the .md file
    if os.path.exists(md_file):
        with open(md_file, "r") as f:
            content = f.read()
            
        content = re.sub(rf"{filename}_files/figure-markdown/", f"{target_dir}/", content)
        
        with open(md_file, "w") as f:
            f.write(content)
```

This acts behind the scenes so your `.qmd` files stay clean, while automatically routing the `.png` files directly to your custom path.
