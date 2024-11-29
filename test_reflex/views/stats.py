import reflex as rx
from ..backend.backend import State
from ..components.stats_selector import stats_selector


class StatsState(rx.State):
    stats_view: str = "age_value"
    radar_toggle: bool = False
    area_toggle: bool = False

    def toggle_radarchart(self):
        self.radar_toggle = not self.radar_toggle

    def toggle_areachart(self):
        self.area_toggle = not self.area_toggle


def _age_value_chart() -> rx.Component:
    return rx.cond(
        StatsState.area_toggle,
        rx.recharts.area_chart(
            rx.recharts.legend(),
            rx.recharts.graphing_tooltip(cursor=False),
            rx.recharts.cartesian_grid(),
            rx.recharts.area(
                type_="monotone",
                data_key="average value",
                stroke="#30A46C",
                fill="#5bb98bb3",
            ),
            rx.recharts.x_axis(data_key="age"),
            rx.recharts.y_axis(type_="number", scale="auto", hide=True),
            data=State.get_age_value_chart_data,
            min_height=325,
        ),
        rx.recharts.bar_chart(
            rx.recharts.legend(),
            rx.recharts.graphing_tooltip(),
            rx.recharts.cartesian_grid(),
            rx.recharts.bar(
                data_key="average value", stroke="#30A46C", fill="#5bb98bb3"
            ),
            rx.recharts.x_axis(data_key="age"),
            rx.recharts.y_axis(type_="number", scale="auto", hide=True),
            data=State.get_age_value_chart_data,
            min_height=325,
        ),
    )




def _age_rating_chart() -> rx.Component:
    return rx.cond(
        StatsState.area_toggle,
        rx.recharts.area_chart(
            rx.recharts.legend(),
            rx.recharts.graphing_tooltip(cursor=False),
            rx.recharts.cartesian_grid(),
            rx.recharts.area(
                type_="monotone",
                data_key="average rating",
                stroke="#30A46C",
                fill="#5bb98bb3",
            ),
            rx.recharts.x_axis(data_key="age"),
            rx.recharts.y_axis(type_="number", scale="auto", hide=True),
            data=State.get_age_rating_chart_data,
            min_height=325,
        ),
        rx.recharts.bar_chart(
            rx.recharts.legend(),
            rx.recharts.graphing_tooltip(),
            rx.recharts.cartesian_grid(),
            rx.recharts.bar(
                data_key="average rating", stroke="#30A46C", fill="#5bb98bb3"
            ),
            rx.recharts.x_axis(data_key="age"),
            rx.recharts.y_axis(type_="number", scale="auto", hide=True),
            data=State.get_age_rating_chart_data,
            min_height=325,
        ),
    )




def _team_value_chart() -> rx.Component:
    return rx.cond(
        StatsState.area_toggle,
        rx.recharts.area_chart(
            rx.recharts.legend(),
            rx.recharts.graphing_tooltip(cursor=False),
            rx.recharts.cartesian_grid(),
            rx.recharts.area(
                type_="monotone",
                data_key="total value",
                stroke="#8E4EC6",
                fill="#8e4ec6a9",
            ),
            rx.recharts.brush(data_key="name", height=30, stroke="#8E4EC6"),
            rx.recharts.x_axis(data_key="team"),
            rx.recharts.y_axis(type_="number", scale="auto", hide=True),
            data=State.get_team_value_chart_data,
            min_height=325,
        ),
        rx.recharts.bar_chart(
            rx.recharts.legend(),
            rx.recharts.graphing_tooltip(cursor=False),
            rx.recharts.cartesian_grid(),
            rx.recharts.bar(
                data_key="total value",
                stroke="#8E4EC6",
                fill="#8e4ec6a9",
            ),
            rx.recharts.brush(data_key="name", height=30, stroke="#8E4EC6"),
            rx.recharts.x_axis(data_key="team"),
            rx.recharts.y_axis(type_="number", scale="auto", hide=True),
            data=State.get_team_value_chart_data,
            min_height=325,
        ),
    )


def _age_team_chart() -> rx.Component:
    return rx.cond(
        StatsState.area_toggle,
        rx.recharts.area_chart(
            rx.recharts.legend(),
            rx.recharts.graphing_tooltip(cursor=False),
            rx.recharts.cartesian_grid(),
            rx.recharts.area(
                data_key="average age",
                type_="monotone",
                stroke="#FFA500",
                fill="#ffa6009e",
            ),
            rx.recharts.brush(data_key="team", height=30, stroke="#FFA500"),
            rx.recharts.x_axis(data_key="team"),
            rx.recharts.y_axis(type_="number", scale="auto", hide=True),
            data=State.get_team_age_average_data,
            min_height=325,
        ),
        rx.recharts.bar_chart(
            rx.recharts.legend(),
            rx.recharts.graphing_tooltip(),
            rx.recharts.cartesian_grid(),
            rx.recharts.bar(data_key="average age", stroke="#FFA500", fill="#ffa6009e"),
            rx.recharts.brush(data_key="team", height=30, stroke="#FFA500"),
            rx.recharts.x_axis(data_key="team"),
            rx.recharts.y_axis(type_="number", scale="auto", hide=True),
            data=State.get_team_age_average_data,
            min_height=325,
        ),
    )



def _radar_toggle() -> rx.Component:
    return rx.cond(
        StatsState.radar_toggle,
        rx.icon_button(
            rx.icon("pentagon", size=24),
            size="3",
            cursor="pointer",
            variant="soft",
            on_click=StatsState.toggle_radarchart,
        ),
        rx.icon_button(
            rx.icon("bar-chart-3", size=24),
            size="3",
            cursor="pointer",
            variant="soft",
            on_click=StatsState.toggle_radarchart,
        ),
    )


def _area_toggle() -> rx.Component:
    return rx.cond(
        StatsState.area_toggle,
        rx.icon_button(
            rx.icon("area-chart", size=24),
            size="3",
            cursor="pointer",
            variant="soft",
            on_click=StatsState.toggle_areachart,
        ),
        rx.icon_button(
            rx.icon("bar-chart-3", size=24),
            size="3",
            cursor="pointer",
            variant="soft",
            on_click=StatsState.toggle_areachart,
        ),
    )


def stats_ui() -> rx.Component:
    return rx.flex(
        rx.scroll_area(
            stats_selector(),
            scrollbars="vertical",
            width=["100%", "100%", "100%", "45%"],
            height=["100%", "100%", "100%", "calc(100vh - 300px)"],
            type="always",
        ),
        rx.vstack(
            rx.flex(
                rx.select(
                    value=StatsState.stats_view,
                    items=[
                        "age_value",
                        "age_team",
                        "age_rating",
                        "team_value",
                    ],
                    on_change=StatsState.set_stats_view,
                    size="3",
                    variant="soft",
                    justify_content="end",
                ),
                rx.match(
                    StatsState.stats_view,
                    ("age_value", "age_rating", _radar_toggle()),
                    (_area_toggle()),
                ),
                margin_bottom=["2em", "2em", "4em"],
                spacing="4",
                width="110%",
            ),
            rx.match(
                StatsState.stats_view,
                ("age_value", _age_value_chart()),
                ("age_team", _age_team_chart()),
                ("age_rating", _age_rating_chart()),
                ("team_value", _team_value_chart()),
            ),
            width="90%",
            justify="center",
            padding_x=["0em", "0em", "0em", "0em", "6em"],
        ),
        flex_direction=["column-reverse", "column-reverse", "column-reverse", "row"],
        spacing="9",
        width="100%",
    )
