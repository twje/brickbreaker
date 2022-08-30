from dataclasses import dataclass
from pathlib import Path
from .texture import Texture
from .texture_region import TextureRegion

__all__ = ["TextureAtlas"]


@dataclass
class Page:
    texture_file: str = None
    width: int = 0
    height: int = 0


@dataclass
class Region:
    page: Page = None
    name: str = ""
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0


class TextureAtlasData:
    def __init__(self, filepath) -> None:
        with open(filepath, "r") as fp:
            self.page, self.regions = self.load(filepath, fp.readlines())

    def load(self, filepath, lines):
        # setup
        entry = [None] * 5
        page_fields = {
            "size": self.parse_page_size
        }
        region_fields = {
            "xy": self.parse_region_xy,
            "size": self.parse_region_size
        }

        page = None
        regions = []

        index = 0
        while (index < len(lines)):
            line, index = self.parse_line(lines, index)
            # parse page
            if self.read_entry(entry, line) == 0 and page is None:
                page = Page()
                page.texture_file = Path(filepath).with_name(line)
                while (True):
                    line, index = self.parse_line(lines, index)
                    if self.read_entry(entry, line) == 0:
                        break

                    parser_id = entry[0]
                    if parser_id in page_fields:
                        page_fields[parser_id](entry, page)

            # parse regions
            if self.read_entry(entry, line) == 0:
                region = Region()
                region.page = page
                region.name = line
                regions.append(region)
            else:
                parser_id = entry[0]
                if parser_id in region_fields:
                    region_fields[parser_id](entry, regions[-1])

        return page, regions

    def parse_line(self, lines: list[str], index: int) -> int:
        """Return current line and next index."""
        while (True):
            line = lines[index].strip()
            if line == "":
                index += 1
                continue
            break

        return line, index + 1

    def parse_page_size(self, entry: list, page: Page):
        page.width = int(entry[1])
        page.height = int(entry[1])

    def parse_region_xy(self, entry: list, region: Region):
        region.x = int(entry[1])
        region.y = int(entry[2])

    def parse_region_size(self, entry: list, region: Region):
        region.width = int(entry[1])
        region.height = int(entry[2])

    def read_entry(self, entry: list[str], line: str) -> int:
        if line is None:
            return 0
        line = line.strip()
        if len(line) == 0:
            return 0
        if ":" not in line:
            return 0

        elements = line.split(":")
        entry[0] = elements[0]

        for index, value in enumerate(elements[1].split(","), start=1):
            entry[index] = value.strip()

        return index + 1


class TextureAtlas:
    def __init__(self, filepath) -> None:
        self.texture_regions: list[TextureRegion] = self.load(filepath)

    def load(self, filepath) -> list[TextureRegion]:
        texture_regions = []
        data = TextureAtlasData(filepath)
        texture = Texture(data.page.texture_file)

        for region in data.regions:
            texture_regions.append(TextureRegion(
                texture,
                region.name,
                region.x,
                region.y,
                region.width,
                region.height
            ))

        return texture_regions

    def find_region(self, name: str) -> TextureRegion:
        for texture_region in self.texture_regions:
            if texture_region.name == name:
                return texture_region
