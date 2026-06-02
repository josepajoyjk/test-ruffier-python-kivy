# ruffier_timer.py
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.clock import Clock
from kivy.core.window import Window  
from kivy.lang import Builder
from kivy.uix.label import Label

# Registramos el diseño exclusivo de este componente

Builder.load_string('''
<RuffierTimerWidget>:
    orientation: 'vertical'
    padding: 30
    spacing: 20
    canvas.before:
        Color:
            rgba: 0.08, 0.09, 0.12, 1
        Rectangle:
            pos: self.pos
            size: self.size

    Label:
        text: "TEST DE RUFFIER - CONTROL DE PULSO"
        font_name: 'addons/sans-beach/Sans Beach.ttf'
        font_size: '22sp'
        bold: True
        size_hint_y: 0.1
        color: 0.9, 0.9, 0.9, 1

    RelativeLayout:
        size_hint_y: 0.6
        canvas:
            Color:
                rgba: 0.15, 0.17, 0.22, 1
            Line:
                # CAMBIO: Usar el centro local del layout
                circle: (self.width / 2, self.height / 2, min(self.width, self.height) * 0.38)
                width: 10
            Color:
                rgba: (0.1, 0.7, 0.9, 1) if root.tiempo_restante > 0 else (0.9, 0.2, 0.3, 1)
            Line:
                # CAMBIO: Usar el centro local del layout
                circle: (self.width / 2, self.height / 2, min(self.width, self.height) * 0.38, 0, root.angulo_progreso)
                width: 10

        Label:
            text: root.texto_tiempo
            font_name: 'addons/sans-beach/Sans Beach.ttf'
            font_size: '75sp'
            bold: True
            # El Label sí usa pos_hint relativo, por lo que el centro 0.5 lo ubica perfecto
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}

    BoxLayout:
        orientation: 'vertical'
        size_hint_y: 0.2
        
        Label:
            font_name: 'addons/sans-beach/Sans Beach.ttf'
            text: f"PULSACIONES REGISTRADAS: {root.contador_pulsaciones}" if root.activar_teclado else ""
            font_size: '28sp'
            bold: True
            color: 0.2, 0.8, 0.4, 1
            
        Label:
            font_name: 'addons/sans-beach/Sans Beach.ttf'
            text: ("[ Presione ESPACIO por cada latido ]" if root.cronometro_activo else "[ Presione Iniciar para comenzar ]") if root.activar_teclado else ""
            font_size: '14sp'
            color: 0.6, 0.6, 0.6, 1

    Button:
        # CAMBIO: Ahora el botón muestra dinámicamente los segundos configurados
        text: f'Iniciar Toma ({int(root.tiempo_configurado)} Segundos)'
        font_name: 'addons/sans-beach/Sans Beach.ttf'
        size_hint: (0.5, 0.1)
        pos_hint: {'center_x': 0.5}
        background_normal: ''
        background_color: 0.0, 0.5, 0.8, 1
        font_size: '18sp'
        bold: True
        on_press: root.iniciar_toma()
''')

class RuffierTimerWidget(BoxLayout):
    tiempo_configurado = NumericProperty(15.0) # Guardamos el límite que tú decidas pasarle
    tiempo_restante = NumericProperty(15.0)
    angulo_progreso = NumericProperty(360.0)
    texto_tiempo = StringProperty("15.00")
    contador_pulsaciones = NumericProperty(0)
    activar_teclado = BooleanProperty(False) 
    cronometro_activo = BooleanProperty(False)

    # Agregamos 'tiempo_total' con 15.0 como valor por defecto por si no le pasas nada
    def __init__(self, a_c=False, tiempo_total=15.0, **kwargs):
        self.activar_teclado = a_c
        self.tiempo_configurado = float(tiempo_total)
        self.tiempo_restante = float(tiempo_total)
        self.texto_tiempo = f"{self.tiempo_restante:.2f}"
        
        super().__init__(**kwargs)
        
        self.evento_reloj = None
        self.on_timeout_callback = None 
        
        if self.activar_teclado:
            Window.bind(on_key_down=self.detectar_latido)

    def iniciar_toma(self):
        if self.evento_reloj:
            Clock.unschedule(self.evento_reloj)
        
        # Reiniciamos basándonos en el tiempo que configuraste al crear el widget
        self.tiempo_restante = self.tiempo_configurado
        self.angulo_progreso = 360.0
        self.texto_tiempo = f"{self.tiempo_restante:.2f}"
        self.contador_pulsaciones = 0
        self.cronometro_activo = True 
        
        self.evento_reloj = Clock.schedule_interval(self.actualizar_cronometro, 0.05)

    def actualizar_cronometro(self, dt):
        self.tiempo_restante -= dt

        if self.tiempo_restante <= 0:
            self.tiempo_restante = 0.0
            self.angulo_progreso = 0.0
            self.texto_tiempo = "¡Terminado!"
            self.cronometro_activo = False 
            Clock.unschedule(self.evento_reloj)
            
            if self.on_timeout_callback:
                self.on_timeout_callback(self.contador_pulsaciones)
        else:
            self.texto_tiempo = f"{self.tiempo_restante:.2f}"
            # CAMBIO: El cálculo del ángulo ahora es relativo al tiempo configurado
            self.angulo_progreso = (self.tiempo_restante / self.tiempo_configurado) * 360.0

    def detectar_latido(self, window, key, scancode, codepoint, modifiers):
        if key == 32: # Espacio
            if self.cronometro_activo:
                self.contador_pulsaciones += 1
            return True