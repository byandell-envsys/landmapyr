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

## Approach 2: Use a Post-Render Script

If you prefer not to add `savefig` to every single Python cell in your notebook, you can write a script that automatically moves the images and updates the markdown links in the generated `.md` file after Quarto finishes rendering.

**Important Quarto Limitation:** Quarto's built-in `post-render` hooks **do not run** when rendering individual files (e.g., `quarto render madison.qmd`). They only run when rendering an entire project via `quarto render` with a `_quarto.yml` file.

Because you are likely rendering single files, the easiest way to use this approach is to chain the script directly in your terminal command:

```bash
quarto render madison.qmd -t markdown && python3 -m landmapyr.move_images madison
```

After having created the markdown version,
you can move the images with

```bash
python3 ../landmapyr/move_images.py madison
```

Alternatively, if you *are* rendering a full project (using `quarto render`), you can add the hook to your `_quarto.yml` project file:

```yaml
project:
  type: default
post-render:
  - python3 -c "from landmapyr.move_images import move_images; move_images('madison')"
```

This leverages the `landmapyr.move_images` module, which encapsulates the following logic to handle file operations and markdown link updates.

By keeping this script within the `landmapyr` package, you avoid duplicating utility scripts across different analysis folders.

This acts behind the scenes so your `.qmd` files stay clean, while automatically routing the `.png` files directly to your custom path.
