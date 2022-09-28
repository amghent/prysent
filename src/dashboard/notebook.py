import logging
import os.path
import uuid

import nbformat
from bs4 import BeautifulSoup
from django.conf import settings
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor

from cacher.models import Cache
from scheduler.models import Schedule


class Notebook:
    logger = logging.getLogger(__name__)

    def __init__(self, path: str, export_path: str = None):
        if not path.startswith(settings.MEDIA_DIR):
            path = os.path.join(settings.MEDIA_DIR, path)

        assert os.path.exists(path) and os.path.isfile(path)

        if export_path is None:
            export_path = f"{uuid.uuid4()}.html"

        self.path = path
        self.export_path = export_path

    def convert(self):
        self.logger.info(f"Converting notebook: {self.path[len(settings.MEDIA_DIR)+1:]}")

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

        soup = BeautifulSoup(html, features="lxml")

        # Remove code cells that produce not output at all
        divs = soup.findAll("div", {"class": "jp-Cell jp-CodeCell jp-Notebook-cell jp-mod-noOutputs jp-mod-noInput"})

        for div in divs:
            if len(div.get_text(strip=True)) == 0:
                div.extract()

        html = soup.prettify(encoding="utf-8").decode("utf-8")

        file_name, _ = os.path.splitext(os.path.basename(self.path))

        with open(os.path.join(settings.HTML_DIR, self.export_path), "w", encoding="utf-8") as html_file:
            html_file.write(html)

        self.logger.info(f"Finished converting notebook: {self.path[len(settings.MEDIA_DIR)+1:]}")

        try:
            cache = Cache.objects.get(cached_html=self.export_path)
            cache.generated = True
            cache.save()

        except Cache.DoesNotExist:
            pass

        try:
            schedule = Schedule.objects.get(html_file=self.export_path)
            schedule.generated = True
            schedule.save()

        except Schedule.DoesNotExist:
            pass
