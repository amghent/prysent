import os.path
import uuid

import nbformat
from django.conf import settings
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor


class Notebook:
    def __init__(self, path):
        assert os.path.exists(path) and os.path.isfile(path)

        self.path = path

    def convert(self):
        with open(self.path, "r", encoding="utf-8") as notebook_file:
            notebook_json = notebook_file.read()

        notebook = nbformat.reads(notebook_json, as_version=4)

        executor = ExecutePreprocessor(timeout=600, kernel_name="python3")

        executor.preprocess(notebook, {"metadata": {"path": f"{os.path.dirname(self.path)}"}})

        html_exporter = HTMLExporter()

        html_exporter.template_name = "lab"
        html_exporter.exclude_input = True
        html_exporter.exclude_anchor_links = True
        html_exporter.exclude_input_prompt = True
        html_exporter.exclude_output_prompt = True
        html_exporter.embed_images = True

        html, resources = html_exporter.from_notebook_node(notebook)
        file_name, _ = os.path.splitext(os.path.basename(self.path))
        export = os.path.join(settings.HTML_DIR, f"{uuid.uuid4()}.html")

        with open(export, "w", encoding="utf-8") as html_file:
            html_file.write(html)

        return export