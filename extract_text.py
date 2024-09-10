import fulltext
from fulltext import BaseBackend

register_backend(
    'text/plain',
    'extract_text', # path to this module
    extensions=['.txt', '.text'])



class Backend(BaseBackend):

    def handle_fobj(self, f):

        return f.read()



def extract(filename):
    """
    A function that extracts text given a filepath
    """

    with open(filename, 'rb') as f:
        result = chardet.detect(f.read())
        charenc = result['encoding']
        with open(filename, 'r', encoding=charenc) as f:
            content = fulltext.get(f, None, name=filename)
            # content = f.read()

    return content

