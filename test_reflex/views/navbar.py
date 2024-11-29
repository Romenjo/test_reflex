import reflex as rx


def navbar():
    return rx.flex(
        rx.hstack(
            rx.image(src="/ball.png", height="38px"),
            rx.heading("FOOTBALL DATA", size="7"),
            rx.badge(
                "2021-2024 seasons",
                radius="full",
                align="center",
                color_scheme="orange",
                variant="surface",
            ),
            align="center",
        ),
        rx.spacer(),
        rx.hstack(
            rx.logo(),
            rx.color_mode.button(),
            align="center",
            spacing="3",
        ),
        spacing="2",
        flex_direction=["column", "column", "row"],
        align="center",
        width="100%",
        top="0px",
    )
