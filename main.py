# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

from addons.ruffier import *
from addons.instructions import * # ⚠️ IMPORTACIÓN DEL TEMPORIZADOR PERSONALIZADO
from addons.ruffier_timer import RuffierTimerWidget

# Variables globales de control para los resultados
age = 7
name = ""
p1, p2, p3 = 0, 0, 0

# Paleta de colores idéntica a tu ruffier_timer.py
COLOR_FONDO = (0.08, 0.09, 0.12, 1)      
COLOR_INPUT_BG = (0.15, 0.17, 0.22, 1)   
COLOR_BOTON = (0.0, 0.5, 0.8, 1)         
COLOR_TEXTO = (0.9, 0.9, 0.9, 1)         

font = 'addons/sans-beach/Sans Beach.ttf'  
font_size = '20sp'  

def aplicar_fondo_oscuro(screen_instance):
    """Pinta el fondo de la escena con el mismo color oscuro del temporizador"""
    with screen_instance.canvas.before:
        Color(rgba=COLOR_FONDO)
        screen_instance.rect_fondo = Rectangle(pos=screen_instance.pos, size=screen_instance.size)
    screen_instance.bind(pos=lambda src, pos: setattr(src.rect_fondo, 'pos', pos))
    screen_instance.bind(size=lambda src, size: setattr(src.rect_fondo, 'size', size))


class InstScr(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        aplicar_fondo_oscuro(self)

        instr = Label(text=txt_instruction, font_name=font, font_size=font_size, color=COLOR_TEXTO)
        lb1 = Label(text="Ingresar nombre:  ", halign='right', font_name=font, font_size=font_size, color=COLOR_TEXTO)
        self.in_name = TextInput(multiline=False, font_name=font, font_size=font_size, 
                                 background_normal='', background_color=COLOR_INPUT_BG, foreground_color=COLOR_TEXTO)
        
        lb2 = Label(text="Ingresa la edad:  ", halign='right', font_name=font, font_size=font_size, color=COLOR_TEXTO)
        self.in_age = TextInput(text='7', multiline=False, font_name=font, font_size=font_size,
                                 background_normal='', background_color=COLOR_INPUT_BG, foreground_color=COLOR_TEXTO)

        self.btn = Button(text="Siguiente", size_hint=(0.5, 0.15), pos_hint={'center_x': 0.5}, 
                          font_name=font, font_size=font_size, bold=True, background_normal='', background_color=COLOR_BOTON)
        self.btn.bind(on_press=self.next)

        line1 = BoxLayout(size_hint=(0.8, None), height='40sp', pos_hint={'center_x': 0.5}, spacing=10)
        line2 = BoxLayout(size_hint=(0.8, None), height='40sp', pos_hint={'center_x': 0.5}, spacing=10)
        line1.add_widget(lb1)
        line1.add_widget(self.in_name)
        line2.add_widget(lb2)
        line2.add_widget(self.in_age)
        
        outer = BoxLayout(orientation='vertical', padding=30, spacing=20)
        outer.add_widget(instr)
        outer.add_widget(line1)
        outer.add_widget(line2)
        outer.add_widget(self.btn)
        self.add_widget(outer)

    def next(self, instance):
        global name, age
        name = self.in_name.text
        try:
            age = int(self.in_age.text)
        except ValueError:
            age = 7 
        self.manager.current = 'pulse1'


class PulseSrc(Screen):
    """PANTALLA PULSO 1: Muestra el cronómetro de 15 segundos y cuenta espacios"""
    def __init__(self, **kw):
        super().__init__(**kw)
        aplicar_fondo_oscuro(self)
        
        self.outer = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # 🟢 IMPORTADO: Teclado activo (a_c=True) para capturar espacios en 15 segundos
        self.ruffieradd = RuffierTimerWidget(a_c=True, tiempo_total=15.0)  
        
        self.btn_next = Button(text='Siguiente (Ir a Sentadillas)', font_name=font, font_size=font_size, bold=True,
                               size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5},
                               background_normal='', background_color=COLOR_BOTON)
        self.btn_next.bind(on_press=self.next)

        self.outer.add_widget(self.ruffieradd)
        self.outer.add_widget(self.btn_next)
        self.add_widget(self.outer)

    def on_enter(self):
        # Cada vez que entramos a la pantalla, se reinicia el teclado y empieza a correr
        Clock.schedule_once(lambda dt: self.ruffieradd.iniciar_toma(), 0.1)

    def next(self, instance):
        global p1
        # Guardamos de forma automática el contador de espacios del widget
        p1 = self.ruffieradd.contador_pulsaciones
        self.manager.current = 'sits'


class ChekSits(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        aplicar_fondo_oscuro(self)

        instr = Label(text=txt_sits, font_name=font, font_size=font_size, color=COLOR_TEXTO) 
        self.btn = Button(text='Siguiente', font_name=font, font_size=font_size, bold=True,
                          size_hint=(0.5, 0.12), pos_hint={'center_x': 0.5}, background_normal='', background_color=COLOR_BOTON)
        self.btn.bind(on_press=self.next)
        
        outer = BoxLayout(orientation='vertical', padding=30, spacing=20)
        outer.add_widget(instr)
        outer.add_widget(self.btn)
        self.add_widget(outer)
    
    def next(self, instance):
        self.manager.current = 'pulse2'


class PulseSrc2(Screen):
    """PANTALLA PULSO 2 Y DESCANSO: Usa ruffier_timer de forma doble y automatizada"""
    def __init__(self, **kw):
        super().__init__(**kw)
        aplicar_fondo_oscuro(self)

        self.outer = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Etiqueta de estado para guiar al usuario
        self.lbl_estado = Label(text="PREPÁRATE PARA EL DESCANSO", font_name=font, font_size='22sp', bold=True, size_hint_y=0.1, color=COLOR_TEXTO)
        self.outer.add_widget(self.lbl_estado)

        # 🟢 IMPORTADO 1: Cronómetro de Descanso (45 segundos, teclado apagado)
        self.cronometro_descanso = RuffierTimerWidget(a_c=False, tiempo_total=45.0)
        self.cronometro_descanso.on_timeout_callback = self.iniciar_segunda_toma
        
        # 🟢 IMPORTADO 2: Cronómetro Pulso Final (15 segundos, teclado encendido)
        self.cronometro_final = RuffierTimerWidget(a_c=True, tiempo_total=15.0)
        
        # Agregamos primero el de descanso a la pantalla
        self.outer.add_widget(self.cronometro_descanso)

        # Botón para continuar manualmente al terminar todo
        self.btn = Button(text="Calcular Resultados", size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5}, 
                          font_name=font, font_size=font_size, bold=True, background_normal='', background_color=COLOR_BOTON)
        self.btn.bind(on_press=self.next)
        self.outer.add_widget(self.btn)
        
        self.add_widget(self.outer)

    def on_enter(self):
        # Al entrar, arranca directamente el reloj de descanso de 45 segundos
        self.lbl_estado.text = "FASE DE DESCANSO (Relájate)"
        Clock.schedule_once(lambda dt: self.cronometro_descanso.iniciar_toma(), 0.1)

    def iniciar_segunda_toma(self, *args):
        """Se ejecuta sola cuando los 45 segundos de descanso llegan a cero"""
        self.lbl_estado.text = "¡TOMA DE PULSO FINAL! (Presiona Espacio)"
        
        # Quitamos el reloj viejo de descanso y ponemos el reloj que cuenta espacios
        self.outer.remove_widget(self.cronometro_descanso)
        self.outer.insert_widget(1, self.cronometro_final) 
        
        # Iniciamos el segundero de 15 segundos para el pulso 3
        self.cronometro_final.iniciar_toma()

    def next(self, instance):
        global p2, p3
        # Como en este caso el usuario descansó y se tomó el pulso seguido:
        # p2 será una estimación fija/promedio o tomada en el descanso, y p3 serán los espacios reales guardados.
        p2 = int(self.cronometro_descanso.contador_pulsaciones) # Será 0 porque a_c estaba en False
        p3 = int(self.cronometro_final.contador_pulsaciones)    # Captura real con barra espaciadora
        
        # Nota: Si en tu fórmula requieres ingresar un p2 manual, puedes cambiar esta lógica, 
        # pero aquí p3 ya se guarda de forma 100% automatizada por el espacio.
        self.manager.current = 'result'


class Result(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        aplicar_fondo_oscuro(self)

        self.outer = BoxLayout(orientation='vertical', padding=30, spacing=20)
        self.instr = Label(text='', font_name=font, font_size=font_size, color=COLOR_TEXTO, halign='center')
        
        self.btn_exit = Button(text="Finalizar", size_hint=(0.4, 0.12), pos_hint={'center_x': 0.5},
                               font_name=font, font_size=font_size, bold=True, background_normal='', background_color=COLOR_BOTON)
        self.btn_exit.bind(on_press=lambda inst: App.get_running_app().stop())

        self.outer.add_widget(self.instr)
        self.outer.add_widget(self.btn_exit)
        self.add_widget(self.outer)
    
    def on_enter(self):
        global name, p1, p2, p3, age
        
        txt_index = globals().get('txt_index', "Tu índice de Ruffier: ")
        txt_workheart = globals().get('txt_workheart', "Eficiencia cardíaca: ")
        txt_res = globals().get('txt_res', [
            "bajo.\n¡Ve a ver a tu médico lo antes posible!",
            "satisfactorio.\n¡Ve a ver a tu médico!",
            "promedio.\nPodría valer la pena realizar pruebas adicionales.",
            "superior al promedio",
            "alto"
        ])

        if age < 7:
            self.instr.text = name + '\n' + "No hay datos para menores de 7 años."
            return

        # Multiplicación automatizada por 4 para proyectar a 1 minuto
        S = 4 * (p1 + p2 + p3)
        r_index = (S - 200) / 10
        
        if age in [7, 8]:
            insat = 21.0
        elif age in [9, 10]:
            insat = 19.5
        elif age in [11, 12]:
            insat = 18.0
        elif age in [13, 14]:
            insat = 16.5
        else:
            insat = 15.0

        debil = insat - 4
        satisf = debil - 5
        bueno = satisf - 5.5

        if r_index >= insat:
            res = txt_res[0]   
        elif r_index >= debil:
            res = txt_res[1]   
        elif r_index >= satisf:
            res = txt_res[2]   
        elif r_index >= bueno:
            res = txt_res[3]   
        else:
            res = txt_res[4]   

        self.instr.text = f"{name}\n\n{txt_index}{r_index}\n\n{txt_workheart}{res}"


class PruebasXD(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        aplicar_fondo_oscuro(self)
        
        outer = BoxLayout(orientation='vertical', padding=20, spacing=15)
        self.ruffieradd = RuffierTimerWidget(a_c=False, tiempo_total=5.0)  
        
        self.btn_skip = Button(text='Saltar Inicialización', font_name=font, font_size=font_size, bold=True,
                               size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5}, background_normal='', background_color=COLOR_BOTON)
        self.btn_skip.bind(on_press=lambda inst: setattr(self.manager, 'current', 'instr'))

        outer.add_widget(self.ruffieradd)
        outer.add_widget(self.btn_skip)
        self.add_widget(outer)


class HeartCheck(App):
    def build(self):
        self.title = "Test de Ruffier"
        sm = ScreenManager()
        sm.add_widget(PruebasXD(name='prueba'))
        sm.add_widget(InstScr(name='instr'))
        sm.add_widget(PulseSrc(name='pulse1'))
        sm.add_widget(ChekSits(name='sits'))
        sm.add_widget(PulseSrc2(name='pulse2'))
        sm.add_widget(Result(name='result'))
        return sm

if __name__ == '__main__':
    HeartCheck().run()