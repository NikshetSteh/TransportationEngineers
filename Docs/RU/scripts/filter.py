"""
Pandoc filter using panflute for plantUML and mermaid
"""

import hashlib
import sys
import os
import subprocess
import shutil


import panflute as pf

dirname_of_included_mdfile = ""

MERMAID_BIN = shutil.which("mmdc.cmd")
if MERMAID_BIN is None:
    pf.debug("Mermaid executable not found. Please check your installation.")
else:
    MERMAID_BIN = MERMAID_BIN.replace("\\", "/")
    pf.debug(f"Mermaid executable found at: {MERMAID_BIN}")



def process_mermaid(elem, doc):
    """Change Text in codeblock from mermaid
    to an Image reference

    The image is rendered during execution

    Arguments:
    elem -- The element that should be processed
    doc  -- The document
    """
    if isinstance(elem, pf.CodeBlock) and 'mermaid' in elem.classes:
        # Extract the caption from element attributes
        if 'caption' in elem.attributes:
            caption = [pf.Str(elem.attributes['caption'])]
            typef = 'fig:'
        else:
            caption = []
            typef = ''

        filename = get_filename4code("mermaid", elem.text)
        filetype = get_extension(doc.format, "png", html="svg", latex="png")

        src = filename + '.mmd'
        dest = filename + '.' + filetype

        if not os.path.isfile(dest):
            txt = elem.text.encode(sys.getfilesystemencoding())
            with open(src, "wb") as f:
                f.write(txt)

        # Default command to execute
        cmd = [MERMAID_BIN, "-i", src, "-o", dest]

        # stdout PIPE required to avoid 'BlockingIOError: [Errno 11] write could not complete without blocking'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        _ = p.communicate()

        sys.stderr.write('Created image ' + dest + '\n')

        return pf.Para(pf.Image(*caption, identifier=elem.identifier,
                                attributes=elem.attributes, url=dest, title=typef))


def process_codeblockinclude(elem, _):
    """Change Text in codeblock from an included
    file that is placed in the codeblock

    Arguments:
    elem -- The element that should be processed
    doc  -- The document
    """

    if isinstance(elem, pf.CodeBlock) and 'codeblock-include' in elem.classes:
        concatinated_file_content = ''

        # Within the codeblock the files are listed. We extract them
        file_names = elem.text.splitlines()
        for c, file_name in enumerate(file_names):
            if not file_name.startswith('#'):
                try:
                    file_content = open(file_name, "r", encoding="utf-8")
                    concatinated_file_content = concatinated_file_content + file_content.read()
                except:
                    pf.debug('Error in reading ' + str(file_name) + '\n')

        elem.text = concatinated_file_content
    pass


def get_filename4code(module, content, ext=None):
    """Generate filename based on content
    The function ensures that the (temporary) directory exists, so that the
    file can be written.
    Example:
        filename = get_filename4code("myfilter", code)
    """
    imagedir = module + "-images"
    fn = hashlib.sha1(content.encode(sys.getfilesystemencoding())).hexdigest()
    try:
        os.mkdir(imagedir)
        sys.stderr.write('Created directory ' + imagedir + '\n')
    except OSError:
        pass
    if ext:
        fn += "." + ext
    return os.path.join(imagedir, fn)


def get_extension(ext_format, default, **alternates):
    """get the extension for the result, needs a default and some specialisations
    Example:
      filetype = get_extension(format, "png", html="svg", latex="eps")
    """
    try:
        return alternates[ext_format]
    except KeyError:
        return default


def process_mdinclude(elem, doc):
    """Recursive mdinclude based on mdinclude CodeBlock

    Arguments:
    elem -- The element that should be processed
    doc  -- The document
    """

    if isinstance(elem, pf.CodeBlock) and 'mdinclude' in elem.classes:
        # We take the received element and turn it into a list of elements
        # that are derived from the included markdown file
        list_of_converted_elements = convert_code_element_to_list_of_elements(
            elem, doc)

        # Enumerate over the new elements and see if there are
        # further mdinclude codeblocks to include
        # Since enumerate is also working over a list that is changed
        # during enumeration this works in a recursive manner
        for n, element in enumerate(list_of_converted_elements):

            # There seems to be one
            if isinstance(element, pf.CodeBlock) and 'mdinclude' in element.classes:
                # Convert it
                next_converted_list = convert_code_element_to_list_of_elements(
                    element, doc)
                # Remove the codeblock
                del list_of_converted_elements[n]
                # Insert the new elements at the place
                # Where the codeblock was
                list_of_converted_elements[n:n] = next_converted_list

        pf.debug(list_of_converted_elements)
        return list_of_converted_elements


def convert_code_element_to_list_of_elements(elem, _):
    """Conversion of a codeblock element to a list of elements
    that have been extracted from the included markdown

    Ignores lines with # as comments
    Honors the following control keywords:
        Increase_headers=True -- If set headers in the included files are
                                 increased by one level

    Arguments:
    elem -- The element that should be processed
    doc  -- The document

    Returns a list with the converted elements
    """

    # Safety first. In case we use this function for a recursive call.
    # If Not, we can remove it anyway
    if isinstance(elem, pf.CodeBlock) and 'mdinclude' in elem.classes:
        # All files in one codeblock will be combined as if they
        # where one file. We need a string to concatenate the file_content
        # of all files
        increase_headers = False

        included_elements = []

        # Within the codeblock the files are listed. We extract them
        file_names = elem.text.splitlines()
        for c, file_name in enumerate(file_names):
            if 'Increase_headers=True' in file_name:
                increase_headers = True
                continue

            if 'Increase_headers=False' in file_name:
                continue

            if not file_name.startswith('#') and file_name.strip():
                try:
                    # extracting the directory name for later use
                    # in case we need to change the image URI
                    global dirname_of_included_mdfile
                    dirname_of_included_mdfile = os.path.dirname(
                        file_name) + '/'

                    if dirname_of_included_mdfile == "/" or dirname_of_included_mdfile == "":
                        dirname_of_included_mdfile = "./"

                    # Read the file and store as string
                    content_as_string = open(
                        file_name, "r", encoding="utf-8").read()

                    # Convert all to pandoc elements and add them
                    # to the list of elements
                    content_as_elements = pf.convert_text(content_as_string)

                    # Test recursion
                    for n, element in enumerate(content_as_elements):
                        element.walk(change_uri, doc=None)

                    included_elements.extend(content_as_elements)
                except:
                    pf.debug('Error in reading ' + str(file_name) + '\n')

        # User want to increase the header levels
        if increase_headers:
            for n, element in enumerate(included_elements):
                if isinstance(element, pf.Header):
                    element.level += 1
                    included_elements[n] = element

        return included_elements

    # Just in case it is no Codeblock we pass through
    pass


def change_uri(elem, _):
    """Private Helper that is called in mdinclude parser to change
    relative URIs

    Arguments:
    elem -- The element that should be processed
    doc  -- The document
    """

    if isinstance(elem, pf.Image):
        # In case we found an Image we need to change the URI
        # based on the location the file that is including the
        # image. We do this by prepending the global variable
        new_url = dirname_of_included_mdfile + elem.url
        elem.url = new_url
    if isinstance(elem, pf.CodeBlock) and 'mdinclude' in elem.classes:
        # More or less the same thing for other mdincludes. But in
        # this case we change the element text after all URIs have been
        # rewritten.
        file_names = elem.text.splitlines()
        for c, file_name in enumerate(file_names):
            if 'Increase_headers' in file_name:
                continue
            if not file_name.startswith('#') and file_name.strip():
                new_file_name = dirname_of_included_mdfile + file_name
                file_names[c] = new_file_name
        new_text = '\n'.join(file_names)
        elem.text = new_text


def main(doc=None):
    #    return pf.run_filters([process_mdinclude, process_codeblockinclude, process_plantuml, process_mermaid],
    return pf.run_filters([process_mdinclude, process_codeblockinclude, process_mermaid],
                          # prepare=prepare,
                          # finalize=finalize,
                          doc=doc)


if __name__ == '__main__':
    main()
