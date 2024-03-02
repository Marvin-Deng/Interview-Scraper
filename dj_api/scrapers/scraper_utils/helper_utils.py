def parse_css_selector(css_selector: str):
    if ' ' in css_selector:
        css_selector = '.' + '.'.join(css_selector.split())
    return css_selector
