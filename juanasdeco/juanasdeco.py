import reflex as rx  # o import pynecone as pc (dependiendo de la versión)

class State(rx.State):
    pass

def index() -> rx.Component:
    return rx.center(
        rx.text("¡Hola Mundo!", font_size="2em"),
        rx.image(src="https://reflex.dev/logo.jpg",alt="Reflex Logo",)
        rx.button(
            "Fancy Button",
            border_radius="1em",
            box_shadow="rgba(151, 65, 252, 0.8) 0 15px 30px -10px",
            background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)",
            box_sizing="border-box",
            color="white",
            opacity=1,
                )
    )

app = rx.App()  # o pc.App() si usas Pynecone
app.add_page(index, route="/")  # Página principal