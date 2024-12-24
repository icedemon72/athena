import flet as ft, asyncio
from flet_navigator import PageData
from controllers.register_controller import handle_register
from components.loader import Loader
from components.responsive_container import ResponsiveContainer

def register_screen(page_data: PageData):
	page = page_data.page
	
	async def on_submit():
		loader = Loader(page)
		asyncio.create_task(loader.create_loader())		
		register = handle_register(email_tf.value, name_tf.value, password_tf.value, faculty.value)
		loader.delete_loader()

		if register['success']:
			success_snack = ft.SnackBar(ft.Text('Uspešna registracija, sada je potrebno prijaviti se!'), open=True)
			page.overlay.append(success_snack)
			page_data.navigate_homepage()

		else: 
			email_tf.border_color = None
			name_tf.border_color = None
			password_tf.border_color = None
			faculty.border_color = None

			field_controls = {
        'email': email_tf,
        'name': name_tf,
        'password': password_tf,
        'faculty': faculty
    	}

			errors = ft.Column(
				controls = [
					ft.Text('Greška prilikom registracije', weight=ft.FontWeight.BOLD),
				]
			)
			
			for error in register['errors']:
				if error['field'] in field_controls:
					field_controls[error['field']].border_color = ft.Colors.RED_300

				errors.controls.append(ft.Text(f"• {error['message']}"))
				
			
			error_snack = ft.SnackBar(errors, open=True)
			page.overlay.append(error_snack)
	
		page.update()

	email_tf = ft.TextField(
		prefix_icon=ft.Icons.EMAIL,
		label='E-adresa',
		autofill_hints=ft.AutofillHint.EMAIL,
		keyboard_type=ft.KeyboardType.EMAIL
	)

	name_tf = ft.TextField(
		prefix_icon=ft.Icons.PERSON,
		label='Ime i prezime'
	)

	password_tf = ft.TextField(
		prefix_icon=ft.Icons.LOCK,
		label='Lozinka',
		password=True,
		can_reveal_password=True,
		autofill_hints=ft.AutofillHint.NEW_PASSWORD
	)
	
	faculty = ft.Dropdown(
		prefix_icon=ft.Icons.SCHOOL,
		label='Fakultet',
		hint_text='Izaberi tvoj fakultet',
		options=[
				ft.dropdown.Option('Ekonomski fakultet'),
				ft.dropdown.Option('Medicinski fakultet'),
				ft.dropdown.Option('Poljoprivredni fakultet'),
				ft.dropdown.Option('Pravni fakultet'),
				ft.dropdown.Option('Prirodno-matematički fakultet'),
				ft.dropdown.Option('Učiteljski fakultet'),
				ft.dropdown.Option('Fakultet za sport i fizičko vaspitanje'),
				ft.dropdown.Option('Fakultet tehničkih nauka'),
				ft.dropdown.Option('Filozofski fakultet'),
		],
	)

	container = ft.SafeArea(
		ft.Container(
			ft.Column(
				[
					ft.Row(
						[ft.Text('Registracija', theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)],
						alignment=ft.MainAxisAlignment.CENTER,
					),
					ft.Column(
						[ email_tf, password_tf, name_tf, faculty ]
					),
					ResponsiveContainer(
						[ 
							ft.ElevatedButton(
								'Registruj se', 
								on_click = lambda _: asyncio.run(on_submit()),
								height=50,
								expand=True
							) 
						],
					),
					ft.Row(
						[ ft.TextButton('Imaš nalog? Prijavi se', on_click=lambda _: page_data.navigate('/')) ]
					)
				]
			)
		)
	)
	return container