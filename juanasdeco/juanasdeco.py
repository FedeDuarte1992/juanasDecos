import reflex as rx

class State(rx.State):
    """Estado base de la aplicación"""
    pass

def navbar() -> rx.Component:
    """Barra de navegación"""
    return rx.box(
        rx.hstack(
            rx.image(src="/logo.jpg", width="2.5em"),
            rx.heading("Mi App", size="4"),  # Tamaño numérico
            justify="between",  # Formato correcto
            padding="1em",
            border_bottom="1px solid #eee",
        ),
        width="100%",
    )

def sidebar() -> rx.Component:
    """Barra lateral"""
    return rx.box(
        rx.vstack(
            rx.text("Menú"),
            rx.link("Inicio", href="/"),
            rx.link("Configuración", href="/settings"),
            spacing="4",  # Valor numérico
            padding="1em",
        ),
        width="20%",
        border_right="1px solid #eee",
    )

def main_content() -> rx.Component:
    """Contenido principal"""
    return rx.center(
        rx.vstack(
            rx.heading("¡Bienvenido!", size="4"),
            rx.text("Esta es la página principal"),
            rx.button(
                "Acción",
                color_scheme="blue",
                size="3",  # Tamaño numérico (1-4)
                margin_top="2em",
            ),
            align="center",
            spacing="4",
        ),
        width="80%",
        padding="2em",
    )

def footer() -> rx.Component:
    """Pie de página"""
    return rx.box(
        rx.text("© 2023 Mi App - Todos los derechos reservados"),
        padding="1em",
        border_top="1px solid #eee",
        text_align="center",
        width="100%",
    )

def index() -> rx.Component:
    """Página principal"""
    return rx.flex(
        navbar(),
        rx.flex(
            sidebar(),
            main_content(),
            height="85vh",
        ),
        footer(),
        direction="column",
        height="100vh",
    )

app = rx.App()
app.add_page(index, route="/")