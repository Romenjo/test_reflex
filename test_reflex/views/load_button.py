import reflex as rx
from ..backend.backend import State

def load_data() -> rx.Component:
    rx.flex(
        rx.button(
            "Fill OLTP",
            color_scheme="orange",
            on_click=State.fill_oltp,
        ),
    )