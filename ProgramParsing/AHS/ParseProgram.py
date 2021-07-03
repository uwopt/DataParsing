from ProgramParsing.AHS.MajorParser import AHSMajorParser
from ProgramParsing.ProgramParser.ParseProgram import main, filterFiles
import os

if __name__ == "__main__":
    dir = os.path.dirname(__file__)
    path = os.path.join(dir, 'Specs')
    files = set(["/Specs/" + f for f in os.listdir(path) if f.endswith(".html")])

    filesToIgnore = []
    files = filterFiles(files, filesToIgnore)

    parsers = {
        'MajorParser': AHSMajorParser,
    }

    main(parsers, files, "Applied Health Science")
