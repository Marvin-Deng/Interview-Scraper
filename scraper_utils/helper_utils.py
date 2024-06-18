def parse_css_selector(css_selector: str) -> str:
    if " " in css_selector:
        css_selector = "." + ".".join(css_selector.split())
    return css_selector
