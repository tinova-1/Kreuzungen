from collections import defaultdict
import csv

FILE_EXTENSIONS_DOC = {"pdf", "doc", "docx"}
FILE_EXTENSIONS_PHOTO = {"png", "jpg", "jpeg"}
ICON_DOC = "📃"
ICON_PHOTO = "📷"
ICON_MAP = "🗺️"
ICON_LINK = "\u2197\ufe0f"
ICON_ARCHIVE = "🗄️"
ICON_DWG = "✏️"

IMPORT_CSV_SEP = ","
EXPORT_CSV_SEP = ","
IMPORT_CSV_QUOTECHAR = '"'
COMMENT = "#"
IMPORT_FILENAME = "Kreuzungen.txt"
EXPORT_FILENAME = "Kreuzungen.html"
DEFAULT_IMG_FOLDER = ""

INPUT_COL_HEADLINES = ["COUNTRY", "PLACE", "N", "E", "USE", "TECHNOLOGY", "RATING", "IMG_LINK"]
LEN_INPUT_COL_HEADLINES = len(INPUT_COL_HEADLINES)
OUTPUT_COL_HEADLINES = ["COUNTRY", "PLACE", "MAP_LINK", "IMG_LINK", "USE", "TECHNOLOGY", "RATING"]

class EmptyLineException(Exception): pass

class Eintrag:
    def __init__(self, cells, is_headline=False):
        self.cells = cells
        self.is_headline = is_headline

    def __map_entry(self):
        url = "https://www.google.com/maps/search/?api=1&map_action=map&query={}+{}".format(self.cells["N"],
                                                                                            self.cells["E"])
        entry = '<a target="_blank" rel="noopener noreferrer" href="{}">{}</a>'.format(url, ICON_MAP)
        return entry

    def __img_link(self):
        if self.cells["IMG_LINK"] == [""]:
            return ""
        entry = ""
        for img_link in self.cells["IMG_LINK"]:
            icon = ICON_LINK
            for ext in FILE_EXTENSIONS_PHOTO:
                if img_link.lower().endswith(ext):
                    icon = ICON_PHOTO
                    break
                    
            for ext in FILE_EXTENSIONS_DOC:
                if img_link.lower().endswith(ext):
                    icon = ICON_DOC
                    break

            if img_link.lower().startswith("dwg"):
                icon = ICON_DWG
            if "web.archive.org" in img_link.lower():
                icon = ICON_ARCHIVE

            entry += '<a target="_blank" rel="noopener noreferrer" href="{}">{}</a>'.format(
                DEFAULT_IMG_FOLDER + img_link, icon)
        return entry

    def to_html(self):
        table_entries = self.cells.copy()
        if self.is_headline:
            table_entries.update({"MAP_LINK": "Karte"})
            table_entries.update({"IMG_LINK": "Foto(s)"})
        else:
            table_entries.update({"MAP_LINK": self.__map_entry()})
            table_entries.update({"IMG_LINK": self.__img_link()})
        yield "<tr>"
        for headline in OUTPUT_COL_HEADLINES:
            if not self.is_headline:
                yield "\t<td>{}</td>".format(table_entries[headline])
            else:
                yield "\t<th>{}</th>".format(table_entries[headline])
        yield "</tr>"


def parse_line(line, csv_sep=IMPORT_CSV_SEP, comment=COMMENT):
    """
    Parses a line (=a list of strings). If the line starts with the comment string or is None, ignores the line.
    Splits the line into cells defined by csv_sep. If the cell content is within quotes, ignores csv_seps. Removes quotes afterwards
    Returns a list of strings (cells)
    """

    if len(line) == 0 or line[0].startswith(comment):
        raise EmptyLineException

    cells = line
    # d is a dict so that dict has as keys the headlines as defined in INPUT_COL_HEADLINES
    d = defaultdict(str)

    for i in range(len(cells)):
        cells[i] = cells[i].strip()

        headline = INPUT_COL_HEADLINES[i]
        d[headline] = cells[i]

    img_link = d["IMG_LINK"]
    img_link = img_link.split(",")
    for i in range(len(img_link)):
        img_link[i] = img_link[i].strip()
    d["IMG_LINK"] = img_link

    return d


def read_file(filename=IMPORT_FILENAME):
    content = []  # a list of entries
    with open(filename, encoding="utf-8-sig") as csvfh:
        csv_reader = csv.reader(csvfh, delimiter=IMPORT_CSV_SEP, quotechar=IMPORT_CSV_QUOTECHAR)
        for lino, line in enumerate(csv_reader, start=1):

            try:
                cells = parse_line(line)
            except EmptyLineException:
                continue

            is_headline = lino == 1

            new_entry = Eintrag(cells, is_headline=is_headline)

            content.append(new_entry)
    return content


def write_file(content, filename=EXPORT_FILENAME):
    entry = content[0]
    theadrows = []
    for line in entry.to_html():
        theadrows.append("\t\t\t\t\t\t{}".format(line))
    trows = []
    for entry in content[1:]:
        for line in entry.to_html():
            trows.append("\t\t\t\t\t\t{}".format(line))

    thead = """					<thead>
{}
					</thead>""".format("\n".join(theadrows))

    tbody = """					<tbody>
{}
					</body>""".format("\n".join(trows))

    table = """				<table id="example" class="display" style="width:100%">
{}
{}
				</table>""".format(thead, tbody)

    website = """<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="Content-type" content="text/html; charset=utf-8">
	<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
	<title>Kreuzungen</title>
	<link rel="shortcut icon" type="image/png" href="/media/images/favicon.png">
	<link rel="alternate" type="application/rss+xml" title="RSS 2.0" href="http://www.datatables.net/rss.xml">
	<link rel="stylesheet" type="text/css" href="/media/css/site-examples.css?_=0db1cd38700c0cfcdc140c39a2ebc306">
	<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.21/css/jquery.dataTables.min.css">

	<script type="text/javascript" language="javascript" src="https://code.jquery.com/jquery-3.5.1.js"></script>
	<script type="text/javascript" language="javascript" src="https://cdn.datatables.net/1.10.21/js/jquery.dataTables.min.js"></script>
	<script type="text/javascript" class="init">
	
$(document).ready(function() {{
	$('#example').DataTable( {{
		stateSave: true
	}} );
}} );

	</script>
</head>
<body class="wide comments example">
	<a name="top" id="top"></a>
		<div class="fw-body">
			<div class="content">
{}
			</div>
		</div>
	</div>
</body>
</html>""".format(table)

    with open(filename, "w", encoding="utf8") as fh:
        fh.write(website)


if __name__ == "__main__":
    content = read_file(IMPORT_FILENAME)
    write_file(content, EXPORT_FILENAME)
