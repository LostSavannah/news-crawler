from typing import Dict, Tuple
from threadsnake.turbo import *
from threadsnake.http.core.common import get_port
from threadsnake.http.router import Router

app:Application = Application(get_port(8084))

def style(selector:str, styles:Dict[str, str]) -> Tuple[str, Dict[str, str]]:
    return (selector, styles)

def style_str(style:Tuple[str, Dict[str, str]]) -> str:
    result:str = style[0] + '{\n'
    for st in style[1]:
        result += f'\t{st}: {style[1][st]};\n'
    result += '}\n'
    return result


@app.get('/')
def get(app:Application, req:HttpRequest, res:HttpResponse):
    children = [(method, route) for method in app.routes for route in app.routes[method]]
    children = [
        f'<li><span class="{method} method">{method}</span>{route}</li>'
        for (method, route)
        in children
    ]
    html:str = '<ul>' + ''.join(children) + '</ul>'
    head:str = f'<head><style>{get_style()}</style></head><body>{html}</body>'
    res.html(f'<html>{head}</html>')


methodcolors:Dict[str, str] = {
    ".method":{
        "padding": "0.2em",
        "margin": "0.2em",
        "border-radius": "5px"
    },
    ".GET": {
        "background-color": "#7a7",
        "color": "white"
    }
}

def get_style():
    styles = []
    for method in methodcolors:
        st = style(f'{method}', methodcolors[method])
        styles.append(st)
    result = ''
    for st in styles:
        result += style_str(st)
    return result



try:
    app.start()
except:
    pass