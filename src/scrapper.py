from bs4 import BeautifulSoup

def extract_tooltip(dt):
    dt_soup = BeautifulSoup(dt, "html.parser")
    infos = dt_soup.find_all("td")
    resa = {}
    while infos:
        if infos[0].text.endswith(":"):
            key = infos[0].text.strip(":")
            resa[key] = []
        else:
            if (infos[0].text != ""):
                resa[key].append(infos[0].text.strip())
        infos = infos[1:]
    for key in resa:
        if (resa[key].__len__() == 1):
            resa[key] = resa[key][0]
    return resa

def extract_instructor_resas(html):
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find_all("td", {"class": "referenceContentTD"})
    tooltips = []
    for row in rows:
        resa = row.find("div", {"class": "reservation"})
        if (resa):
            dt = resa["data-tooltip"]
            tooltip = extract_tooltip(dt)
            tooltips.append(tooltip)
    return tooltips