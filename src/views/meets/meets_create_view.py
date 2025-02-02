import flet as ft, re, datetime, asyncio
from flet_navigator import PageData
from controllers.meets_controller import handle_create_meet
from components.loader import Loader
from components.responsive_card import ResponsiveForm
from components.snack_bar import SnackBar

def meets_create_screen(page_data: PageData):
	global selected_date
	global selected_time

	page = page_data.page
	selected_date = datetime.datetime.now()
	selected_time = datetime.datetime.now().time()

	async def on_submit():
		loader = Loader(page)
		asyncio.create_task(loader.create_loader())
		new_meet = await handle_create_meet(title_tf.value, description_tf.value, field_tf.value, location_tf.value, selected_date.strftime('%Y-%m-%d'), time_tf.value, limit_tf.value)
		loader.delete_loader()
		
		if new_meet['success']: 
			page.overlay.append(SnackBar('Uspešno kreiran Simpozijum!', 'Premeštam te na njegovu stranicu...'))
			page_data.navigate('meets_show', parameters={'id': new_meet['id']})

		else: 
			title_tf.border_color = None
			description_tf.border_color = None
			field_tf.border_color = None
			location_tf.border_color = None
			time_tf.border_color = None
			limit_tf.border_color = None
			date_tf.border_color = None

			field_controls = {
				'title': title_tf,
				'description': description_tf,
				'field': field_tf,
				'location': location_tf,
				'time': time_tf,
				'limit': limit_tf,
				'date': date_tf
			}

			error_snackbar = SnackBar('Greška prilikom kreiranja Simpozijuma', snackbar_type='ERROR')
			for error in new_meet['errors']:
				if error['field'] in field_controls:
					field_controls[error['field']].border_color = ft.Colors.RED_300

				error_snackbar.append_error(error['message'])
			
			page.overlay.append(error_snackbar)


		page.update()

	def handle_date_change(e):
		global selected_date
		selected_date = e.control.value
		date_tf.value = e.control.value.strftime('%d.%m.%Y.')
		page.update()

	def handle_time_change(e):
		global selected_time
		selected_time = e.control.value
		time_tf.value = e.control.value.strftime("%H:%M")
		page.update()

	def handle_number_input(e):
		limit_tf.value = re.sub(r'\D', '', limit_tf.value)
		
		page.update()

	title_tf = ft.TextField(label='Naslov Simpozijuma')
	description_tf = ft.TextField(label='Opis Simpozijuma', multiline=True, min_lines=1, max_lines=5)
	field_tf = ft.TextField(label='Naučno polje')
	location_tf = ft.TextField(label='Lokacija održavanja')
	time_tf = ft.TimePicker(help_text='Izaberi vreme održavanja Simpozijuma')
	limit_tf = ft.TextField(label='Slobodna mesta', keyboard_type=ft.KeyboardType.NUMBER, on_change=handle_number_input, max_length=2)
	date_tf = ft.TextField(label='Datum održavanja', value=selected_date.strftime('%d.%m.%Y.'), disabled=True, expand=True)
	time_tf = ft.TextField(label='Vreme održavanja', value=selected_time.strftime("%H:%M"), disabled=True, expand=True)
	
	container = ResponsiveForm(
		[
			ft.Row(
				[ ft.Text('Kreiraj novi Simpozijum', theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM) ],
				alignment=ft.MainAxisAlignment.CENTER,
				spacing=10
			),
			title_tf,
			description_tf,
			field_tf,
			location_tf,
			ft.Row(
				[
					ft.ElevatedButton(
						'Izaberi datum',
						icon=ft.Icons.CALENDAR_MONTH,
						on_click=lambda e: page.open(
							ft.DatePicker(
								help_text = 'Datum održavanja',
								first_date=datetime.datetime.now(),
								last_date=datetime.datetime.now() + datetime.timedelta(days = 60),
								on_change=handle_date_change,
								value=selected_date
							)
						),
					),
					date_tf
				],
			),
			ft.Row(
				[
					ft.ElevatedButton(
						'Izaberi vreme',
						icon=ft.Icons.CALENDAR_MONTH,
						on_click=lambda e: page.open(
							ft.TimePicker(
									error_invalid_text='Vreme nije validno',
									hour_label_text='H',
									minute_label_text= 'M',
									help_text='Izaberi vreme održavanja',
									on_change=handle_time_change,
									time_picker_entry_mode=ft.TimePickerEntryMode.INPUT,
									value=selected_time
							)
						),
					),
					time_tf
				]
			),
			limit_tf,
			ft.Row(
				[
					ft.ElevatedButton(	
						'Kreiraj simpozijum',
						height=50,
						expand=True,
						on_click =  lambda _: asyncio.run(on_submit())
					)
				]
			)
		]
	)

	return ft.SafeArea(container)