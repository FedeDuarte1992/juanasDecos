from urllib.parse import quote

import reflex as rx


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
    "ink": "#263329",
    "muted": "#777d72",
    "green": "#536b50",
    "cream": "#f7f5ef",
    "line": "#e9e6dc",
    "white": "#fffefa",
}


class StoreState(rx.State):
    search_query: str = ""
    selected_category: str = "Todos"
    cart: dict[str, int] = {}
    cart_open: bool = False

    @rx.var
    def filtered_products(self) -> list[dict[str, str | int]]:
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
    def cart_items(self) -> list[dict[str, str | int]]:
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
        background=rx.cond(active, COLORS["green"], "transparent"),
        color=rx.cond(active, "white", COLORS["muted"]),
        border=rx.cond(active, "1px solid " + COLORS["green"], "1px solid " + COLORS["line"]),
        border_radius="999px",
        padding="0.65em 1.25em",
        font_weight="500",
        cursor="pointer",
        _hover={"border_color": COLORS["green"], "color": COLORS["green"]},
    )


def product_card(product: rx.Var) -> rx.Component:
    return rx.box(
        rx.box(
            rx.image(
                src=product["image"],
                alt=product["name"],
                width="100%",
                height="310px",
                object_fit="cover",
                transition="transform 350ms ease",
                _group_hover={"transform": "scale(1.04)"},
            ),
            rx.cond(
                product["tag"] != "",
                rx.badge(
                    product["tag"],
                    position="absolute",
                    top="14px",
                    left="14px",
                    background=COLORS["white"],
                    color=COLORS["green"],
                    border_radius="999px",
                    padding="0.45em 0.8em",
                ),
                rx.fragment(),
            ),
            position="relative",
            overflow="hidden",
            border_radius="8px",
            background=COLORS["cream"],
        ),
        rx.vstack(
            rx.hstack(
                rx.text(product["category"], color=COLORS["muted"], font_size="0.78rem"),
                rx.text(product["price_label"], color=COLORS["ink"], font_weight="600"),
                justify="between",
                width="100%",
            ),
            rx.heading(product["name"], size="5", color=COLORS["ink"]),
            rx.text(product["description"], color=COLORS["muted"], font_size="0.9rem"),
            rx.button(
                "Agregar al carrito",
                on_click=StoreState.add_to_cart(product["id"]),
                width="100%",
                margin_top="0.4em",
                background="transparent",
                color=COLORS["green"],
                border="1px solid " + COLORS["green"],
                border_radius="5px",
                padding="0.8em",
                cursor="pointer",
                _hover={"background": COLORS["green"], "color": "white"},
            ),
            align="start",
            spacing="2",
            padding_top="1em",
            width="100%",
        ),
        role="group",
        min_width="0",
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
                    background=COLORS["cream"],
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
            background="rgba(28, 35, 29, 0.4)",
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
                                background=COLORS["green"],
                                color="white",
                                border_radius="5px",
                                padding="1em",
                                cursor="pointer",
                                _hover={"background": "#435940"},
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
                        background=COLORS["green"],
                        color="white",
                        border_radius="5px",
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
            box_shadow="-12px 0 40px rgba(20, 30, 22, 0.12)",
        ),
        position="fixed",
        inset="0",
        z_index="10",
    )


def header() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.link(
                rx.heading("juanas", size="7", color=COLORS["ink"], letter_spacing="-0.06em"),
                href="/",
                text_decoration="none",
            ),
            rx.hstack(
                rx.link("Colección", href="#coleccion", color=COLORS["ink"]),
                rx.link("Nuestra esencia", href="#historia", color=COLORS["ink"]),
                rx.button(
                    rx.hstack(
                        rx.text("Bolsa"),
                        rx.badge(
                            StoreState.cart_count,
                            background=COLORS["green"],
                            color="white",
                            border_radius="999px",
                            min_width="22px",
                            justify_content="center",
                        ),
                        spacing="2",
                    ),
                    on_click=StoreState.toggle_cart,
                    background="transparent",
                    color=COLORS["ink"],
                    cursor="pointer",
                    padding="0.6em",
                ),
                spacing="6",
                align="center",
            ),
            justify="between",
            align="center",
            width="100%",
            max_width="1200px",
            margin="0 auto",
            padding="1.2em 1.5em",
        ),
        background=COLORS["white"],
        border_bottom="1px solid " + COLORS["line"],
        position="sticky",
        top="0",
        z_index="5",
    )


def hero() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(
                "OBJETOS CON HISTORIA · HOGARES CON ALMA",
                color="white",
                font_size="0.75rem",
                letter_spacing="0.18em",
                font_weight="600",
            ),
            rx.heading(
                "Tu casa, más tuya.",
                size="9",
                color="white",
                max_width="700px",
                line_height="1.05",
            ),
            rx.text(
                "Detalles simples, materiales nobles y ese toque cálido que transforma cualquier espacio.",
                color="rgba(255,255,255,0.9)",
                font_size={"initial": "1rem", "md": "1.15rem"},
                max_width="520px",
                line_height="1.7",
            ),
            rx.link(
                rx.button(
                    "Descubrí la colección",
                    background=COLORS["white"],
                    color=COLORS["ink"],
                    padding="1em 1.4em",
                    border_radius="4px",
                    font_weight="600",
                    cursor="pointer",
                    _hover={"background": COLORS["cream"]},
                ),
                href="#coleccion",
                margin_top="0.7em",
            ),
            align="start",
            spacing="5",
            max_width="1200px",
            width="100%",
            margin="0 auto",
            padding={"initial": "5em 1.5em", "md": "8em 3em"},
        ),
        background_image="linear-gradient(90deg, rgba(28, 38, 30, 0.78), rgba(28, 38, 30, 0.12)), url('https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=2000&q=90')",
        background_size="cover",
        background_position="center 52%",
        min_height={"initial": "480px", "md": "570px"},
        display="flex",
        align_items="center",
    )


def benefits() -> rx.Component:
    benefit_items = [
        ("✳", "Hecho con intención", "Piezas elegidas una por una"),
        ("⌂", "Envíos a todo el país", "Coordinamos cada entrega"),
        ("♡", "Atención cercana", "Te ayudamos a elegir"),
    ]
    return rx.grid(
        *[
            rx.hstack(
                rx.text(icon, color=COLORS["green"], font_size="1.5rem"),
                rx.vstack(
                    rx.text(title, font_weight="600", color=COLORS["ink"]),
                    rx.text(description, color=COLORS["muted"], font_size="0.82rem"),
                    align="start",
                    spacing="1",
                ),
                justify="center",
                align="center",
                padding="1.5em 1em",
            )
            for icon, title, description in benefit_items
        ],
        columns={"initial": "1", "sm": "3"},
        max_width="1200px",
        margin="0 auto",
        width="100%",
        border_bottom="1px solid " + COLORS["line"],
    )


def collection() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.vstack(
                rx.text(
                    "ELEGIDOS PARA VOS",
                    color=COLORS["green"],
                    font_size="0.75rem",
                    letter_spacing="0.16em",
                    font_weight="600",
                ),
                rx.heading("Pequeños detalles, grandes cambios", size="7", color=COLORS["ink"]),
                rx.text(
                    "Encontrá ese objeto que hace que un rincón se sienta hogar.",
                    color=COLORS["muted"],
                ),
                align="center",
                spacing="3",
                text_align="center",
                padding_bottom="1em",
            ),
            rx.input(
                placeholder="Buscar productos...",
                value=StoreState.search_query,
                on_change=StoreState.set_search_query,
                aria_label="Buscar productos",
                width={"initial": "100%", "sm": "360px"},
                padding="0.85em 1em",
                border="1px solid " + COLORS["line"],
                border_radius="5px",
                background=COLORS["white"],
                color=COLORS["ink"],
            ),
            rx.hstack(
                rx.foreach(CATEGORIES, category_button),
                spacing="2",
                flex_wrap="wrap",
                justify="center",
                padding="0.7em 0",
                width="100%",
            ),
            rx.cond(
                StoreState.filtered_products.length() > 0,
                rx.grid(
                    rx.foreach(StoreState.filtered_products, product_card),
                    columns={"initial": "1", "sm": "2", "lg": "4"},
                    spacing="6",
                    width="100%",
                ),
                rx.vstack(
                    rx.heading("No encontramos productos", size="5", color=COLORS["ink"]),
                    rx.text("Probá con otra búsqueda o categoría.", color=COLORS["muted"]),
                    align="center",
                    width="100%",
                    padding="4em 1em",
                ),
            ),
            align="center",
            spacing="6",
            max_width="1200px",
            margin="0 auto",
            padding={"initial": "4em 1.2em", "md": "6em 1.5em"},
        ),
        id="coleccion",
        background=COLORS["white"],
    )


def story() -> rx.Component:
    return rx.grid(
        rx.image(
            src="https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=1100&q=85",
            alt="Ambiente cálido con objetos naturales y luz suave",
            width="100%",
            height={"initial": "300px", "md": "440px"},
            object_fit="cover",
            border_radius="6px",
        ),
        rx.vstack(
            rx.text(
                "UN HOGAR QUE TE REPRESENTA",
                color=COLORS["green"],
                font_size="0.75rem",
                letter_spacing="0.16em",
                font_weight="600",
            ),
            rx.heading("Lo lindo también puede ser simple.", size="7", color=COLORS["ink"]),
            rx.text(
                "En Juanas creemos que los espacios se construyen de a poco. Por eso buscamos piezas nobles, versátiles y con personalidad: para acompañar tus momentos y contar tu historia.",
                color=COLORS["muted"],
                line_height="1.8",
            ),
            rx.link(
                "Encontrá tu próximo favorito →",
                href="#coleccion",
                color=COLORS["green"],
                font_weight="600",
                margin_top="0.5em",
            ),
            align="start",
            justify="center",
            spacing="4",
            padding={"initial": "2em 0", "md": "3em"},
        ),
        columns={"initial": "1", "md": "2"},
        spacing="8",
        max_width="1200px",
        margin="0 auto",
        padding={"initial": "3em 1.2em", "md": "5em 1.5em"},
        align="center",
        id="historia",
    )


def footer() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.heading("juanas", size="6", color="white", letter_spacing="-0.06em"),
                rx.text("Objetos con historia, hogares con alma.", color="#d2d7cc"),
                align="start",
                spacing="2",
            ),
            rx.vstack(
                rx.text("¿Te ayudamos a elegir?", color="white", font_weight="600"),
                rx.text("Escribinos y armamos tu espacio juntas.", color="#d2d7cc"),
                align={"initial": "start", "md": "end"},
                spacing="2",
            ),
            justify="between",
            align={"initial": "start", "md": "center"},
            flex_direction={"initial": "column", "md": "row"},
            max_width="1200px",
            margin="0 auto",
            padding="2.5em 1.5em",
            width="100%",
        ),
        rx.text(
            "© 2026 Juanas Deco · Hecho con cariño",
            color="#b9c0b4",
            font_size="0.8rem",
            text_align="center",
            padding="1em",
            border_top="1px solid rgba(255,255,255,0.15)",
        ),
        background="#263329",
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
        background=COLORS["white"],
        min_height="100vh",
        color=COLORS["ink"],
    )


app = rx.App()
app.add_page(index, route="/", title="Juanas Deco | Decoración para tu hogar")
