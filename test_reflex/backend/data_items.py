from typing import Dict
from reflex.components.radix.themes.base import LiteralAccentColor

teams_dict: Dict[str, LiteralAccentColor] = {
    "Real Club Deportivo Mallorca S.A.D.": "blue",
    "Olympique Gymnaste Club Nice Côte d'Azur": "yellow",
    "Bologna Football Club 1909": "purple",
    "Tottenham Hotspur Football Club": "cyan",
    "Racing Club de Strasbourg Alsace": "magenta",
    "Kieler Sportvereinigung Holstein von 1900": "olive",
    "Crystal Palace Football Club": "crimson",
    "Clermont Foot 63": "azure",
    "Arsenal Football Club": "aqua",
    "Sevilla Fútbol Club S.A.D.": "lime",
    "Villarreal Club de Fútbol S.A.D.": "cyan",
    "Verein für Bewegungsspiele Stuttgart 1893": "gold",
    "Spezia Calcio": "silver",
    "Juventus Football Club": "black",
    "Eintracht Frankfurt Fußball AG": "white",
    "Genoa Cricket and Football Club": "navy",
    "Lille Olympique Sporting Club Lille Métropole": "teal",
    "Società Sportiva Lazio S.p.A.": "emerald",
    "Elche CF": "peach",
    "SV Darmstadt 98": "amber",
    "Southampton Football Club": "beige",
    "Cádiz CF": "sand",
    "Athletic Club Bilbao": "taupe",
    "Watford FC": "silver",
    "Real Sociedad de Fútbol S.A.D.": "violet",
    "Club Atlético Osasuna": "ruby",
    "Racing Club de Lens": "saffron",
    "Reial Club Deportiu Espanyol de Barcelona S.A.D.": "indigo",
    "Società Sportiva Calcio Napoli": "lime",
    "Paris Saint-Germain Football Club": "blue",
    "Real Madrid Club de Fútbol": "white",
    "West Ham United Football Club": "gold",
    "TSG 1899 Hoffenheim Fußball-Spielbetriebs GmbH": "crimson",
    "Olympique de Marseille": "scarlet",
    "RasenBallsport Leipzig": "blue",
    "Valencia Club de Fútbol S. A. D.": "charcoal",
    "Torino Calcio": "beige",
    "Rayo Vallecano de Madrid S.A.D.": "yellow",
    "Borussia Dortmund": "orange",
    "Manchester United Football Club": "scarlet",
    "FC Bayern München": "crimson",
    "1.FC Köln": "yellow",
    "Manchester City Football Club": "skyblue",
    "Association sportive de Monaco Football Club": "white",
    "Fulham Football Club": "white",
    "Chelsea Football Club": "blue",
    "US Sassuolo": "mint",
    "Arminia Bielefeld": "lime",
    "Leeds United": "white",
    "Nottingham Forest Football Club": "red",
    "Sportverein Werder Bremen von 1899": "green",
    "UD Almería": "crimson",
    "Bayer 04 Leverkusen Fußball": "maroon",
    "Newcastle United Football Club": "periwinkle",
    "Associazione Calcio Fiorentina": "purple",
    "Liverpool Football Club": "red",
    "Atalanta Bergamasca Calcio S.p.a.": "navy",
    "Empoli Football Club S.r.l.": "apricot",
    "Aston Villa Football Club": "burgundy",
    "Brighton and Hove Albion Football Club": "teal",
    "Everton Football Club": "blue",
    "Verein für Leibesübungen Wolfsburg": "lime",
    "Futbol Club Barcelona": "maroon",
    "Borussia Verein für Leibesübungen 1900 Mönchengladbach": "silver",
    "Granada CF": "cherry",
    "Real Betis Balompié S.A.D.": "ivory",
    "Sheffield United": "charcoal",
    "Burnley FC": "crimson",
    "West Ham United Football Club": "gold",
    "Real Valladolid Club de Fútbol S.A.D.": "pink",
    "Football Club Internazionale Milano S.p.A.": "black",
    "Deportivo Alavés S.A.D.": "emerald",
    "Feyenoord Rotterdam": "red",
    "Unione Sportiva Lecce": "crimson",
    "UC Sampdoria": "azure",
    "Verona Hellas Football Club": "pink",
    "Parma Calcio 1913": "purple",
    "Newcastle United Football Club": "gold",
}


teams_list = list(teams_dict.keys())


position_dict: Dict[str, LiteralAccentColor] = {
    "Attack": "red",
    "Defender": "blue",
    "Midfield": "green",
    "Goalkeeper": "yellow",
}

positions_list = list(position_dict.keys())


all_items = {
    "teams": teams_list,
    "positions": positions_list
}

