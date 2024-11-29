import reflex as rx
from ..backend.backend import State


def form_field(
    label: str, placeholder: str, type: str, name: str, default_value: str = ""
) -> rx.Component:
    return rx.form.field(
        rx.flex(
            rx.form.label(label),
            rx.form.control(
                rx.input(
                    placeholder=placeholder, type=type, default_value=default_value
                ),
                as_child=True,
            ),
            direction="column",
        ),
        name=name,
    )


def add_details_button() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button("Add Game", size='4'),
        ),
        rx.dialog.content(
            rx.vstack(
                rx.dialog.title(
                    "Add Game Details",
                ),
                rx.dialog.description(
                    "Fill the form with the game details",
                ),
            ),
            rx.flex(
                rx.form.root(
                    rx.vstack(
                        rx.flex(
                            rx.vstack(
                                rx.hstack(
                                        form_field(
                                            "Home club",
                                            "Home Club",
                                            "text",
                                            "home_club",
                                            "Brighton and Hove Albion Football Club"
                                        ),
                                   form_field(
                                       "Home club goals",
                                       "0",
                                       "number",
                                       "home_goals",
                                       "0"
                                   )
                                ),

                                rx.hstack(
                                        form_field(
                                            "Away club",
                                            "Away Club",
                                            "text",
                                            "away_club",
                                            "Everton Football Club"
                                        ),
                                   form_field(
                                       "Away club goals",
                                       "0",
                                       "number",
                                       "away_goals",
                                       "0"
                                   )
                                ),
                                rx.hstack(
                                    form_field(
                                        "Game date",
                                        "",
                                        "date",
                                        "date",
                                        "12.12.2024"
                                    ),
                                    form_field(
                                        "Competition name",
                                        "Competition",
                                        "text",
                                        "competition_name",
                                        "fa-cup"
                                    ),
                                    form_field(
                                        "Competition Round",
                                        "Round",
                                        "text",
                                        "round_name",
                                        "Second Round"
                                    )
                                    
                                
                                ),
                                
                            ),
                        
                            direction="column",
                        ),
                        rx.flex(
                            rx.hstack(
                                rx.dialog.close(
                                    rx.button(
                                        "Cancel",
                                    ),
                                ),
                                rx.form.submit(
                                    rx.dialog.close(
                                        rx.button(
                                            "Submit Game",
                                            type='submit'
                                        ),
                                    ),
                                    as_child=True,
                                ),
                            ),    
                        ),
                    ),
                    on_submit=State.handle_submit_game_data,
                    reset_on_submit=False,
                ),
            ),
        ),
    )



def add_perfomance_button() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button("Add Player Performance", size='4'),
        ),
        rx.dialog.content(
            rx.vstack(
                rx.dialog.title(
                    "Add Player Performance",
                ),
                rx.dialog.description(
                    "Fill the form with the player performance details",
                ),
            ),
            rx.flex(
                rx.form.root(
                    rx.vstack(
                        rx.flex(
                            rx.vstack(
                                # Game date, home club, away club, player performance fields
                                rx.hstack(
                                    form_field(
                                        "Game date",
                                        "Date of the game",
                                        "date",
                                        "date",
                                        "2024-12-12"
                                    ),
                                ),
                                rx.hstack(
                                    form_field(
                                        "Home club",
                                        "Home Club",
                                        "text",
                                        "home_club",
                                        "Brighton and Hove Albion Football Club"
                                    ),
                                    form_field(
                                        "Away club",
                                        "Away Club",
                                        "text",
                                        "away_club",
                                        "Everton Football Club"
                                    )
                                ),
                                rx.hstack(
                                    form_field(
                                        "Player name",
                                        "Player Name",
                                        "text",
                                        "player_name",
                                        "James Milner"
                                    ),
                                    form_field(
                                        "Goals",
                                        "Goals scored",
                                        "number",
                                        "player_goals",
                                        "0"
                                    ),
                                    form_field(
                                        "Assists",
                                        "Assists made",
                                        "number",
                                        "player_assists",
                                        "0"
                                    ),
                                    form_field(
                                        "Rating",
                                        "Player rating",
                                        "number",
                                        "player_rating",
                                        "6.0"
                                    ),
                                ),
                            ),
                            direction="column",
                        ),
                        rx.flex(
                            rx.hstack(
                                rx.dialog.close(
                                    rx.button(
                                        "Cancel",
                                    ),
                                ),
                                rx.form.submit(
                                    rx.dialog.close(
                                        rx.button(
                                            "Submit Performance",
                                            type='submit'
                                        ),
                                    ),
                                    as_child=True,
                                ),
                            ),
                        ),
                    ),
                    on_submit=State.handle_submit_player_performance,
                    reset_on_submit=False,
                ),
            ),
        ),
    )

@rx.event
def add_transfer_button() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button("Update Player Club", size='4'),
        ),
        rx.dialog.content(
            rx.vstack(
                rx.dialog.title(
                    "Make Player Transfer",
                ),
                rx.dialog.description(
                    "Fill the form with the player transfer details",
                ),
            ),
            rx.flex(
                rx.form.root(
                    rx.vstack(
                        rx.flex(
                            rx.vstack(
                                # Player name, club name, and transfer value fields
                                rx.hstack(
                                    form_field(
                                        "Player name",
                                        "Name of the player",
                                        "text",
                                        "player_name",
                                        "James Milner"
                                    ),
                                ),
                                rx.hstack(
                                    form_field(
                                        "Club name",
                                        "Name of the club the player is transferring to",
                                        "text",
                                        "club_name",
                                        "Liverpool Football Club"
                                    ),
                                    form_field(
                                        "Transfer value",
                                        "Transfer value in Euros",
                                        "number",
                                        "transfer_value",
                                        "25000000"
                                    ),
                                ),
                            ),
                            direction="column",
                        ),
                        rx.flex(
                            rx.hstack(
                                rx.dialog.close(
                                    rx.button(
                                        "Cancel",
                                    ),
                                ),
                                rx.form.submit(
                                    rx.dialog.close(
                                        rx.button(
                                            "Submit Transfer",
                                            type='submit'
                                        ),
                                    ),
                                    as_child=True,
                                ),
                            ),
                        ),
                    ),
                    on_submit=State.handle_update_player_transfer,  
                    reset_on_submit=False,
                ),
            ),
        ),
    )


def export_data_button() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button("Export Data", size='2'),
        ),
        rx.dialog.content(
            rx.vstack(
                rx.dialog.title(
                    "Export Data",
                ),
                rx.dialog.description(
                    "Select the year for the data export",
                ),
            ),
            rx.flex(
                rx.form.root(
                    rx.vstack(
                        rx.flex(
                            rx.vstack(
                                # Year field
                                rx.hstack(
                                    form_field(
                                        "Year",
                                        "Enter the year",
                                        "number",
                                        "year",
                                        "2024"
                                    ),
                                ),
                            ),
                            direction="column",
                        ),
                        rx.flex(
                            rx.hstack(
                                rx.dialog.close(
                                    rx.button(
                                        "Cancel",
                                    ),
                                ),
                                rx.form.submit(
                                    rx.dialog.close(
                                        rx.button(
                                            "Export",
                                            type='submit'
                                        ),
                                    ),
                                    as_child=True,
                                ),
                            ),
                        ),
                    ),
                    on_submit=State.generate_game_stats_json,  
                    reset_on_submit=False,
                ),
            ),
        ),
    )




def edit_ui() -> rx.Component:
    return rx.flex(
        rx.hstack(
        add_details_button(),
        add_perfomance_button(),
        add_transfer_button(),
        justify='center'
        )
    )