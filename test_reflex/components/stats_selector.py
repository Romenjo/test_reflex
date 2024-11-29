import reflex as rx
from ..backend.backend import State
from ..backend.data_items import teams_dict, position_dict
from .item_badges import _selected_item_badge, _unselected_item_badge


def _add_all_button(on_click: callable) -> rx.Component:
    return rx.button(
        rx.icon("plus", size=16),
        "Add All",
        variant="soft",
        size="2",
        on_click=on_click,
        color_scheme="green",
        cursor="pointer",
    )


def _clear_button(on_click: callable) -> rx.Component:
    return rx.button(
        rx.icon("trash", size=16),
        "Clear",
        variant="soft",
        size="2",
        on_click=on_click,
        color_scheme="tomato",
        cursor="pointer",
    )


def _random_button(on_click: callable) -> rx.Component:
    return rx.button(
        rx.icon("shuffle", size=16),
        variant="soft",
        size="2",
        on_click=on_click,
        color_scheme="gray",
        cursor="pointer",
    )


def _items_selector(item: str, items_dict: dict) -> rx.Component:
    return rx.vstack(
        rx.flex(
            rx.hstack(
                _add_all_button(State.add_all_selected(item)),
                _clear_button(State.clear_selected(item)),
                _random_button(State.random_selected(item)),
                spacing="2",
                justify="end",
                width="100%",
            ),
            direction="row",
            align="center",
            width="100%",
        ),
        rx.flex(
            rx.foreach(
                State.selected_items[item],
                lambda team: _selected_item_badge(item, items_dict, team),
            ),
            wrap="wrap",
        ),
        rx.divider(),
        rx.flex(
            rx.foreach(
                items_dict, lambda team: _unselected_item_badge(item, items_dict, team)
            ),
            wrap="wrap",
        ),
        width="100%",
    )


def _accordion_header_stat(icon: str, text: str, item: str) -> rx.Component:
    return rx.hstack(
        rx.icon(icon, size=24),
        rx.heading(text + f" ({(State.selected_items[item].length())})", size="5"),
        spacing="2",
        align="center",
        width="100%",
    )


def _accordion_header(icon: str, text: str) -> rx.Component:
    return rx.hstack(
        rx.icon(icon, size=24),
        rx.heading(text, size="5"),
        spacing="2",
        align="center",
        width="100%",
    )


def _age_selector() -> rx.Component:
    return rx.vstack(
        rx.slider(
            default_value=[18, 44],
            min=18,
            variant="soft",
            max=44,
            on_change=State.set_age,
        ),
        rx.hstack(
            rx.badge("Min Age: ", State.age[0]),
            rx.spacer(),
            rx.badge("Max Age: ", State.age[1]),
            width="100%",
        ),
        width="100%",
    )


def _value_selector() -> rx.Component:
    return rx.vstack(
        rx.slider(
            default_value=[0, 200000000],
            min=0,
            variant="soft",
            max=200000000,
            on_value_commit=State.set_market_value,
        ),
        rx.hstack(
            rx.badge("Min Value: ", State.market_value[0]),
            rx.spacer(),
            rx.badge("Max Value: ", State.market_value[1]),
            width="100%",
        ),
        width="100%",
    )

def _rating_selector() -> rx.Component:
    return rx.vstack(
        rx.slider(
            default_value=[2.0, 10.0],
            min=2.0,
            variant="soft",
            max=10.0,
            on_change=State.set_rating,
        ),
        rx.hstack(
            rx.badge("Min Rating: ", State.rating[0]),
            rx.spacer(),
            rx.badge("Max Rating: ", State.rating[1]),
            width="100%",
        ),
        width="100%",
    )


def stats_selector() -> rx.Component:
    return rx.accordion.root(
        rx.accordion.item(
            header=_accordion_header_stat("shield-half", "Teams", "teams"),
            content=_items_selector("teams", teams_dict),
            value="teams",
        ),
        rx.accordion.item(
            header=_accordion_header_stat("person-standing", "Positions", "positions"),
            content=_items_selector("positions", position_dict),
            value="positions",
        ),
        rx.accordion.item(
            header=_accordion_header("user", "Age"),
            content=_age_selector(),
            value="age",
        ),
        rx.accordion.item(
            header=_accordion_header("star", "Rating"),
            content=_rating_selector(),
            value="rating",
        ),
        rx.accordion.item(
            header=_accordion_header("dollar-sign", "Value"),
            content=_value_selector(),
            value="value",
        ),
        collapsible=True,
        default_value="teams",
        type="single",
        variant="ghost",
        width="100%",
    )
