import json
import textwrap

import nbformat
import nbformat.v4 as nbf


def notebook(uuid, payload, visualisations):
    nb = nbf.new_notebook()
    nb.cells.append(nbf.new_markdown_cell(textwrap.dedent('''
        ![Health report](https://repohealth.info/static/img/heart.png)

        <h1>Health report for {slug}</h1>

        <h3>About this notebook</h3>

        This notebook was originally generated by
        [repohealth.info](https://repohealth.info/).

        You can see the latest version of this report at
        https://repohealth.info/report/{slug}.

        **Please note:** This notebook requires python 3 and plotly.
        '''.format(slug=uuid))))

    nb.cells.append(nbf.new_code_cell(
        '\n'.join(['# The following data can be retrieved from '
                   'https://repohealth.info/api/data/{}'.format(uuid),
                   'import json',
                   'payload = json.loads(r"""',
                   json.dumps(payload),
                   '""".strip())',
                    ''])))
    nb.cells.append(nbf.new_markdown_cell(
        "Now, let's initialise plotly, and recreate the visualisations on "
        "[repohealth.info](https://repohealth.info)."))
    nb.cells.append(nbf.new_code_cell(
        ['from plotly.offline import iplot, init_notebook_mode\n',
         'init_notebook_mode()']))
    for visualisation in visualisations.values():
        nb.cells.append(nbf.new_markdown_cell(visualisation['title']))
        nb.cells.append(nbf.new_code_cell(visualisation['code']))

    content = nbformat.writes(nb, version=4)
    return content
