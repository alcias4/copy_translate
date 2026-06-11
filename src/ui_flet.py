import asyncio
import subprocess
from pathlib import Path

import flet as ft

from modules.clip_paste import paste_clip

# from modules.translate import tranlate_text
from service.deekseep_service import translate_api
from service.get_audio import audio_generate


@ft.component
def Panel():
    textOrigin, set_textOrigin = ft.use_state("")
    spanishTeXT, set_TextSpanish = ft.use_state("")
    active_change, set_change = ft.use_state(False)

    async def uptade_text():

        text = textOrigin
        if not active_change:
            text = paste_clip()
            set_textOrigin(text)

        set_TextSpanish("Loading...")
        response = await asyncio.to_thread(translate_api, text=text)

        set_TextSpanish(response)

    async def handle_audio():

        text = textOrigin.strip()

        if not text:
            return
        url = await asyncio.to_thread(
            audio_generate,
            text,
        )

        if not url:
            return

        subprocess.run(
            [
                "ffplay",
                "-nodisp",
                "-autoexit",
                url,
            ]
        )
        audio = Path(url)
        audio.unlink(missing_ok=True)

    def change_text(e):
        set_textOrigin(e.control.value)

    def handle_active():
        set_change(not active_change)

    return ft.Column(
        controls=[
            ft.TextField(
                label="text to translate",
                value=f"{textOrigin}",
                multiline=True,
                min_lines=8,
                max_lines=8,
                expand=True,
                read_only=True if not active_change else False,
                on_change=change_text,
            ),
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=(ft.Icons.VOLUME_UP),
                        tooltip="Listen pronunciation",
                        on_click=handle_audio,
                    ),
                ]
            ),
            ft.TextField(
                label="translate text",
                value=f"{spanishTeXT}",
                multiline=True,
                min_lines=8,
                max_lines=8,
                read_only=True,
                expand=True,
            ),
            ft.Row(
                controls=[
                    ft.Button(
                        "change active",
                        on_click=handle_active,
                        width=200,
                        bgcolor=ft.Colors.GREEN if active_change else ft.Colors.RED,
                        color=ft.Colors.WHITE,
                    ),
                    ft.Button("Translate", on_click=uptade_text, width=200),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                margin=5,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


async def home(page: ft.Page):
    page.fonts = {"Google": "fonts/google/static/GoogleSans-Regular.ttf"}
    page.theme = ft.Theme(font_family="Google")
    page.title = "Tranlate"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    page.window.height = 580
    page.window.width = 500

    page.render(lambda: Panel())
