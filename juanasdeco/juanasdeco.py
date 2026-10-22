from typing import TypedDict
from urllib.parse import quote

import reflex as rx


class Product(TypedDict):
    id: str
    name: str
    category: str
    description: str
    price: int
    price_label: str
    image: str
    tag: str


class CartItem(Product):
    quantity: int
    line_total: str


PRODUCTS = [
    {
        "id": "jarron-oliva",
        "name": "Jarrón Oliva",
        "category": "Decoración",
        "description": "Cerámica artesanal · 24 cm",
        "price": 18500,
        "price_label": "$ 18.500",
        "image": "https://images.unsplash.com/photo-1578500494198-246f612d3b3d?auto=format&fit=crop&w=900&q=85",
        "tag": "Más elegido",
    },
    {
        "id": "manta-lino",
        "name": "Manta Lino",
        "category": "Textiles",
        "description": "Algodón suave · 130 × 170 cm",
        "price": 32900,
        "price_label": "$ 32.900",
        "image": "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=900&q=85",
        "tag": "Hecho para vos",
    },
    {
        "id": "lampara-nido",
        "name": "Lámpara Nido",
        "category": "Iluminación",
        "description": "Fibra natural · Luz cálida",
        "price": 47500,
        "price_label": "$ 47.500",
        "image": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=900&q=85",
        "tag": "Nuevo",
    },
    {
        "id": "bandeja-arena",
        "name": "Bandeja Arena",
        "category": "Decoración",
        "description": "Madera maciza · Terminación natural",
        "price": 22900,
        "price_label": "$ 22.900",
        "image": "https://images.unsplash.com/photo-1603199506016-b9a594b593c0?auto=format&fit=crop&w=900&q=85",
        "tag": "",
    },
    {
        "id": "almohadon-sur",
        "name": "Almohadón Sur",
        "category": "Textiles",
        "description": "Lino lavado · Funda desmontable",
        "price": 24900,
        "price_label": "$ 24.900",
        "image": "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?auto=format&fit=crop&w=900&q=85",
        "tag": "",
    },
    {
        "id": "espejo-sol",
        "name": "Espejo Sol",
        "category": "Decoración",
        "description": "Madera de kiri · 45 cm",
        "price": 38900,
        "price_label": "$ 38.900",
        "image": "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=900&q=85",
        "tag": "Últimas unidades",
    },
    {
        "id": "vela-calma",
        "name": "Vela Calma",
        "category": "Aromas",
        "description": "Cera vegetal · Cedro y vainilla",
        "price": 12900,
        "price_label": "$ 12.900",
        "image": "https://images.unsplash.com/photo-1603006905003-be475563bc59?auto=format&fit=crop&w=900&q=85",
        "tag": "",
    },
    {
        "id": "canasto-raiz",
        "name": "Canasto Raíz",
        "category": "Decoración",
        "description": "Fibras naturales · Tejido a mano",
        "price": 27900,
        "price_label": "$ 27.900",
        "image": "https://images.unsplash.com/photo-1594620302200-9a762244a156?auto=format&fit=crop&w=900&q=85",
        "tag": "",
    },
]

CATEGORIES = ["Todos", "Decoración", "Textiles", "Iluminación", "Aromas"]
WHATSAPP_CHECKOUT = "https://wa.me/?text="

COLORS = {
    "ink": "#3f3742",
    "muted": "#827985",
    "green": "#7b8f7b",
    "cream": "#fffaf6",
    "line": "#eee5e7",
    "white": "#ffffff",
    "rose": "#f8e9ec",
    "lilac": "#f0ebf7",
    "sage": "#edf2eb",
    "butter": "#fbf2dd",
    "plum": "#514553",
}


class StoreState(rx.State):
    search_query: str = ""
    selected_category: str = "Todos"
    cart: dict[str, int] = {}
    cart_open: bool = False

    @rx.var
    def filtered_products(self) -> list[Product]:
        query = self.search_query.strip().lower()
        return [
            product
            for product in PRODUCTS
            if (self.selected_category == "Todos" or product["category"] == self.selected_category)
            and (
                not query
                or query in product["name"].lower()
                or query in product["category"].lower()
                or query in product["description"].lower()
            )
        ]

    @rx.var
    def cart_count(self) -> int:
        return sum(self.cart.values())

    @rx.var
    def cart_items(self) -> list[CartItem]:
        items = []
        for product in PRODUCTS:
            quantity = self.cart.get(product["id"], 0)
            if quantity:
                items.append(
                    {
                        **product,
                        "quantity": quantity,
                        "line_total": f"$ {product['price'] * quantity:,}".replace(",", "."),
                    }
                )
        return items

    @rx.var
    def subtotal_label(self) -> str:
        subtotal = sum(
            product["price"] * self.cart.get(product["id"], 0) for product in PRODUCTS
        )
        return f"$ {subtotal:,}".replace(",", ".")

    @rx.var
    def checkout_url(self) -> str:
        lines = ["Hola, quiero hacer este pedido:"]
        for product in PRODUCTS:
            quantity = self.cart.get(product["id"], 0)
            if quantity:
                lines.append(f"• {product['name']} x{quantity} — ${product['price'] * quantity:,}".replace(",", "."))
        lines.append(f"Total: {self.subtotal_label}")
        return WHATSAPP_CHECKOUT + quote("\n".join(lines))

    def set_category(self, category: str):
        self.selected_category = category

    def add_to_cart(self, product_id: str):
        if any(product["id"] == product_id for product in PRODUCTS):
            self.cart = {**self.cart, product_id: self.cart.get(product_id, 0) + 1}
            self.cart_open = True

    def decrease_quantity(self, product_id: str):
        quantity = self.cart.get(product_id, 0)
        if quantity <= 1:
            self.cart = {key: value for key, value in self.cart.items() if key != product_id}
        else:
            self.cart = {**self.cart, product_id: quantity - 1}

    def toggle_cart(self):
        self.cart_open = not self.cart_open

    def close_cart(self):
        self.cart_open = False


def category_button(category: str) -> rx.Component:
    active = StoreState.selected_category == category
    return rx.button(
        category,
        on_click=StoreState.set_category(category),
        background=rx.cond(active, COLORS["plum"], COLORS["white"]),
        color=rx.cond(active, "white", COLORS["muted"]),
        border=rx.cond(active, "1px solid " + COLORS["plum"], "1px solid " + COLORS["line"]),
        border_radius="999px",
        padding="0.75em 1.35em",
        font_weight="600",
        cursor="pointer",
        transition="all 180ms ease",
        _hover={"border_color": COLORS["plum"], "color": COLORS["plum"]},
    )


def product_card(product: rx.Var) -> rx.Component:
    return rx.box(
        rx.box(
            rx.image(
                src=product["image"],
                alt=product["name"],
                width="100%",
                height={"initial": "300px", "md": "340px"},
                object_fit="cover",
                transition="transform 500ms ease",
                _group_hover={"transform": "scale(1.04)"},
            ),
            rx.cond(
                product["tag"] != "",
                rx.badge(
                    product["tag"],
                    position="absolute",
                    top="14px",
                    left="14px",
                    background=COLORS["butter"],
                    color=COLORS["plum"],
                    border_radius="999px",
                    padding="0.55em 0.9em",
                    font_weight="600",
                ),
                rx.fragment(),
            ),
            position="relative",
            overflow="hidden",
            border_radius="18px",
            background=COLORS["lilac"],
            box_shadow="0 12px 30px rgba(63, 55, 66, 0.07)",
        ),
        rx.vstack(
            rx.hstack(
                rx.text(product["category"], color=COLORS["green"], font_size="0.78rem", font_weight="600"),
                rx.text(product["price_label"], color=COLORS["ink"], font_weight="700"),
                justify="between",
                width="100%",
            ),
            rx.heading(product["name"], size="5", color=COLORS["ink"], letter_spacing="-0.025em"),
            rx.text(product["description"], color=COLORS["muted"], font_size="0.9rem"),
            rx.button(
                "Sumar a mi bolsa  ↗",
                on_click=StoreState.add_to_cart(product["id"]),
                width="100%",
                margin_top="0.65em",
                background=COLORS["rose"],
                color=COLORS["plum"],
                border="1px solid " + COLORS["rose"],
                border_radius="999px",
                padding="0.9em",
                font_weight="600",
                cursor="pointer",
                transition="all 180ms ease",
                _hover={"background": COLORS["plum"], "color": "white"},
            ),
            align="start",
            spacing="2",
            padding="1.15em 0.25em 0.2em",
            width="100%",
        ),
        role="group",
        min_width="0",
        padding="0.75em",
        border_radius="24px",
        background=COLORS["white"],
        border="1px solid " + COLORS["line"],
        box_shadow="0 12px 32px rgba(63, 55, 66, 0.04)",
        transition="transform 220ms ease, box-shadow 220ms ease",
        _hover={"transform": "translateY(-4px)", "box_shadow": "0 18px 40px rgba(63, 55, 66, 0.11)"},
    )


def cart_item(item: rx.Var) -> rx.Component:
    return rx.hstack(
        rx.image(
            src=item["image"],
            alt=item["name"],
            width="72px",
            height="78px",
            object_fit="cover",
            border_radius="5px",
        ),
        rx.vstack(
            rx.text(item["name"], font_weight="600", color=COLORS["ink"]),
            rx.text(item["line_total"], color=COLORS["muted"], font_size="0.9rem"),
            rx.hstack(
                rx.button(
                    "−",
                    on_click=StoreState.decrease_quantity(item["id"]),
                    aria_label="Quitar una unidad",
                    background=COLORS["lilac"],
                    color=COLORS["plum"],
                    border_radius="50%",
                    width="30px",
                    height="30px",
                    cursor="pointer",
                ),
                rx.text(item["quantity"], min_width="24px", text_align="center"),
                rx.button(
                    "+",
                    on_click=StoreState.add_to_cart(item["id"]),
                    aria_label="Agregar una unidad",
                    background=COLORS["cream"],
                    border_radius="50%",
                    width="30px",
                    height="30px",
                    cursor="pointer",
                ),
                align="center",
                spacing="2",
            ),
            align="start",
            spacing="1",
            flex="1",
        ),
        align="center",
        spacing="3",
        width="100%",
        padding="0.8em 0",
        border_bottom="1px solid " + COLORS["line"],
    )


def cart_drawer() -> rx.Component:
    return rx.box(
        rx.box(
            on_click=StoreState.close_cart,
            position="fixed",
            inset="0",
            background="rgba(63, 55, 66, 0.42)",
            z_index="10",
            aria_label="Cerrar carrito",
            role="button",
            tab_index=0,
        ),
        rx.vstack(
            rx.hstack(
                rx.heading("Tu carrito", size="6", color=COLORS["ink"]),
                rx.button(
                    "×",
                    on_click=StoreState.close_cart,
                    aria_label="Cerrar carrito",
                    background="transparent",
                    font_size="1.8rem",
                    cursor="pointer",
                    color=COLORS["muted"],
                ),
                justify="between",
                width="100%",
                padding_bottom="1em",
                border_bottom="1px solid " + COLORS["line"],
            ),
            rx.cond(
                StoreState.cart_count > 0,
                rx.vstack(
                    rx.foreach(StoreState.cart_items, cart_item),
                    rx.vstack(
                        rx.hstack(
                            rx.text("Subtotal", color=COLORS["muted"]),
                            rx.text(StoreState.subtotal_label, font_weight="700", color=COLORS["ink"]),
                            justify="between",
                            width="100%",
                        ),
                        rx.text(
                            "Envío a coordinar al confirmar tu pedido.",
                            color=COLORS["muted"],
                            font_size="0.82rem",
                        ),
                        rx.link(
                            rx.button(
                                "Enviar pedido por WhatsApp",
                                width="100%",
                                background=COLORS["plum"],
                                color="white",
                                border_radius="999px",
                                padding="1em",
                                font_weight="600",
                                cursor="pointer",
                                _hover={"background": COLORS["green"]},
                            ),
                            href=StoreState.checkout_url,
                            is_external=True,
                            width="100%",
                        ),
                        spacing="3",
                        width="100%",
                        padding_top="1em",
                    ),
                    width="100%",
                    flex="1",
                    overflow_y="auto",
                ),
                rx.vstack(
                    rx.text("Todavía no agregaste productos.", color=COLORS["muted"]),
                    rx.button(
                        "Explorar colección",
                        on_click=StoreState.close_cart,
                        background=COLORS["plum"],
                        color="white",
                        border_radius="999px",
                        padding="0.8em 1em",
                        cursor="pointer",
                    ),
                    align="center",
                    justify="center",
                    flex="1",
                    width="100%",
                ),
            ),
            position="fixed",
            top="0",
            right="0",
            height="100dvh",
            width={"initial": "100%", "sm": "420px"},
            max_width="100%",
            background=COLORS["white"],
            z_index="11",
            padding="1.5em",
            align="stretch",
            spacing="3",
            box_shadow="-12px 0 40px rgba(63, 55, 66, 0.14)",
        ),
        position="fixed",
        inset="0",
        z_index="10",
    )


def header() -> rx.Component:
    return rx.vstack(
        rx.box(
            rx.text(
                "UNA CASA LINDA SE ARMA DE A POCO  ✿  ENVÍOS A TODO EL PAÍS",
                color=COLORS["plum"],
                font_size="0.68rem",
                font_weight="600",
                letter_spacing="0.12em",
                text_align="center",
            ),
            width="100%",
            padding="0.65em 1em",
            background=COLORS["butter"],
        ),
        rx.hstack(
            rx.link(
                rx.hstack(
                    rx.text("✿", color=COLORS["green"], font_size="1.4rem"),
                    rx.heading("juanas", size="7", color=COLORS["ink"], letter_spacing="-0.07em"),
                    spacing="2",
                    align="center",
                ),
                href="/",
                text_decoration="none",
            ),
            rx.hstack(
                rx.link("Tienda", href="#coleccion", color=COLORS["ink"], font_weight="500"),
                rx.link("Nuestra esencia", href="#historia", color=COLORS["ink"], font_weight="500"),
                rx.button(
                    rx.hstack(
                        rx.text("Mi bolsa"),
                        rx.badge(
                            StoreState.cart_count,
                            background=COLORS["rose"],
                            color=COLORS["plum"],
                            font_weight="700",
                            font_size="0.75rem",
                            border="1px solid " + COLORS["white"],
                            border_radius="999px",
                            min_width="22px",
                            justify_content="center",
                        ),
                        spacing="2",
                    ),
                    on_click=StoreState.toggle_cart,
                    background=COLORS["lilac"],
                    color=COLORS["ink"],
                    cursor="pointer",
                    padding="0.65em 1em",
                    border_radius="999px",
                    font_weight="600",
                    _hover={"background": COLORS["rose"]},
                ),
                spacing={"initial": "2", "sm": "6"},
                align="center",
            ),
            justify="between",
            align="center",
            width="100%",
            max_width="1280px",
            margin="0 auto",
            padding={"initial": "0.9em 1.1em", "md": "1.1em 1.5em"},
        ),
        width="100%",
        background=COLORS["cream"],
        border_bottom="1px solid " + COLORS["line"],
        position="sticky",
        top="0",
        z_index="5",
        spacing="0",
        box_shadow="0 5px 22px rgba(63, 55, 66, 0.04)",
    )


def hero() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(
                "OBJETOS CON HISTORIA  ✿",
                color=COLORS["plum"],
                background=COLORS["butter"],
                border_radius="999px",
                padding="0.65em 1em",
                font_size="0.72rem",
                letter_spacing="0.12em",
                font_weight="600",
            ),
            rx.heading(
                "Un hogar que se siente muy tuyo.",
                size={"initial": "8", "md": "9"},
                color=COLORS["ink"],
                max_width="620px",
                line_height="1.02",
                letter_spacing="-0.055em",
            ),
            rx.text(
                "Piezas lindas, texturas nobles y pequeños detalles para hacer de cada rincón tu lugar favorito.",
                color=COLORS["muted"],
                font_size={"initial": "1rem", "md": "1.15rem"},
                max_width="460px",
                line_height="1.75",
            ),
            rx.link(
                rx.button(
                    "Encontrá tus favoritos  →",
                    background=COLORS["plum"],
                    color="white",
                    padding="1.05em 1.6em",
                    border_radius="999px",
                    font_weight="600",
                    cursor="pointer",
                    box_shadow="0 10px 24px rgba(81, 69, 83, 0.16)",
                    _hover={"background": COLORS["green"], "transform": "translateY(-2px)"},
                ),
                href="#coleccion",
                margin_top="0.5em",
            ),
            align="start",
            spacing="4",
            max_width="1280px",
            width="100%",
            margin="0 auto",
            padding={"initial": "5em 1.3em", "md": "8em 3em"},
        ),
        background_image="linear-gradient(90deg, rgba(255,250,246,0.98) 0%, rgba(255,250,246,0.9) 38%, rgba(255,250,246,0.12) 100%), url('https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=2000&q=90')",
        background_size="cover",
        background_position={"initial": "62% center", "md": "center 52%"},
        min_height={"initial": "520px", "md": "650px"},
        display="flex",
        align_items="center",
        background_color=COLORS["rose"],
    )


def benefits() -> rx.Component:
    benefit_items = [
        ("✳", "Hecho con intención", "Piezas elegidas una por una", COLORS["rose"]),
        ("⌂", "Envíos a todo el país", "Coordinamos cada entrega", COLORS["sage"]),
        ("♡", "Atención cercana", "Te ayudamos a elegir", COLORS["lilac"]),
    ]
    return rx.grid(
        *[
            rx.hstack(
                rx.box(
                    rx.text(icon, color=COLORS["plum"], font_size="1.45rem"),
                    width="48px",
                    height="48px",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    border_radius="50%",
                    background=COLORS["white"],
                ),
                rx.vstack(
                    rx.text(title, font_weight="700", color=COLORS["ink"]),
                    rx.text(description, color=COLORS["muted"], font_size="0.82rem"),
                    align="start",
                    spacing="1",
                ),
                justify={"initial": "start", "md": "center"},
                align="center",
                padding="1.15em",
                border_radius="18px",
                background=background,
            )
            for icon, title, description, background in benefit_items
        ],
        columns={"initial": "1", "sm": "3"},
        spacing="4",
        max_width="1280px",
        margin="0 auto",
        width="100%",
        padding={"initial": "1.2em 1.2em", "md": "1.7em 1.5em"},
    )


def collection() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.vstack(
                rx.text(
                    "UNA COLECCIÓN PARA DISFRUTAR",
                    color=COLORS["green"],
                    font_size="0.75rem",
                    letter_spacing="0.14em",
                    font_weight="600",
                ),
                rx.heading(
                    "Detalles que hacen hogar.",
                    size={"initial": "7", "md": "8"},
                    color=COLORS["ink"],
                    letter_spacing="-0.045em",
                ),
                rx.text(
                    "Elegí con calma. Enamorate de una textura. Encontrá esa pieza que te estaba esperando.",
                    color=COLORS["muted"],
                    max_width="560px",
                    line_height="1.7",
                ),
                align="center",
                spacing="2",
                text_align="center",
                padding_bottom="0.5em",
            ),
            rx.input(
                placeholder="¿Qué estás buscando?  ✿",
                value=StoreState.search_query,
                on_change=StoreState.set_search_query,
                aria_label="Buscar productos",
                width={"initial": "100%", "sm": "420px"},
                padding="1em 1.2em",
                border="1px solid " + COLORS["line"],
                border_radius="999px",
                background=COLORS["white"],
                color=COLORS["ink"],
                box_shadow="0 8px 20px rgba(63, 55, 66, 0.04)",
                _focus={"outline": "2px solid " + COLORS["rose"], "border_color": COLORS["green"]},
            ),
            rx.hstack(
                rx.foreach(CATEGORIES, category_button),
                spacing="2",
                flex_wrap="wrap",
                justify="center",
                padding="0.7em 0 1.25em",
                width="100%",
            ),
            rx.cond(
                StoreState.filtered_products.length() > 0,
                rx.grid(
                    rx.foreach(StoreState.filtered_products, product_card),
                    columns={"initial": "1", "sm": "2", "lg": "4"},
                    spacing={"initial": "4", "md": "5"},
                    width="100%",
                ),
                rx.vstack(
                    rx.heading("No encontramos productos", size="5", color=COLORS["ink"]),
                    rx.text("Probá con otra búsqueda o categoría.", color=COLORS["muted"]),
                    align="center",
                    width="100%",
                    padding="5em 1em",
                    background=COLORS["white"],
                    border_radius="24px",
                ),
            ),
            align="center",
            spacing="5",
            max_width="1280px",
            margin="0 auto",
            padding={"initial": "4.5em 1.2em", "md": "6em 1.5em"},
        ),
        id="coleccion",
        background="linear-gradient(180deg, " + COLORS["cream"] + " 0%, " + COLORS["lilac"] + " 100%)",
    )


def story() -> rx.Component:
    return rx.grid(
        rx.image(
            src="https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=1100&q=85",
            alt="Ambiente cálido con objetos naturales y luz suave",
            width="100%",
            height={"initial": "320px", "md": "480px"},
            object_fit="cover",
            border_radius="24px",
            box_shadow="0 20px 50px rgba(63, 55, 66, 0.12)",
        ),
        rx.vstack(
            rx.text(
                "HECHO PARA TU DÍA A DÍA",
                color=COLORS["green"],
                font_size="0.75rem",
                letter_spacing="0.14em",
                font_weight="600",
            ),
            rx.heading(
                "Lo lindo también puede ser simple.",
                size={"initial": "7", "md": "8"},
                color=COLORS["ink"],
                letter_spacing="-0.045em",
                line_height="1.08",
            ),
            rx.text(
                "En Juanas creemos que los espacios se construyen de a poco. Por eso buscamos piezas nobles, versátiles y con personalidad: para acompañar tus momentos y contar tu historia.",
                color=COLORS["muted"],
                line_height="1.8",
            ),
            rx.link(
                "Explorá la colección  →",
                href="#coleccion",
                color=COLORS["plum"],
                font_weight="600",
                margin_top="0.5em",
                padding="0.9em 1.2em",
                border_radius="999px",
                background=COLORS["white"],
            ),
            align="start",
            justify="center",
            spacing="4",
            padding={"initial": "2em 1.4em", "md": "3.5em"},
            background=COLORS["sage"],
            border_radius="24px",
        ),
        columns={"initial": "1", "md": "2"},
        spacing="8",
        max_width="1280px",
        margin="0 auto",
        padding={"initial": "3.5em 1.2em", "md": "6em 1.5em"},
        align="center",
        id="historia",
        background=COLORS["cream"],
    )


def footer() -> rx.Component:
    return rx.box(
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.text("✿", color="#d8c4dc", font_size="1.35rem"),
                    rx.heading("juanas", size="6", color="white", letter_spacing="-0.07em"),
                    align="center",
                    spacing="2",
                ),
                rx.text("Objetos lindos para sentirte en casa.", color="#e0d9e2"),
                align="start",
                spacing="2",
            ),
            rx.vstack(
                rx.text("Un rincón más tuyo empieza acá.", color="white", font_weight="600"),
                rx.link("Descubrí la colección  ↗", href="#coleccion", color="#e0d9e2"),
                align="start",
                spacing="2",
            ),
            display="flex",
            justify_content="space-between",
            align_items={"initial": "flex-start", "md": "center"},
            flex_direction={"initial": "column", "md": "row"},
            max_width="1280px",
            margin="0 auto",
            padding={"initial": "2.5em 1.2em", "md": "3.2em 1.5em"},
            width="100%",
        ),
        rx.text(
            "© 2026 Juanas Deco · Hecho con cariño",
           color="#cfc5d1",
            font_size="0.8rem",
            text_align="center",
            padding="1em",
           border_top="1px solid rgba(255,255,255,0.12)",
        ),
        background=COLORS["plum"],
    )


def index() -> rx.Component:
    return rx.box(
        header(),
        hero(),
        benefits(),
        collection(),
        story(),
        footer(),
        rx.cond(StoreState.cart_open, cart_drawer(), rx.fragment()),
        background=COLORS["cream"],
        min_height="100vh",
        color=COLORS["ink"],
        font_family="Arial, sans-serif",
    )


app = rx.App()
app.add_page(index, route="/", title="Juanas Deco | Decoración para tu hogar")
