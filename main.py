from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from addons.ruffier import *
from addons.instructions import * 

age = 7
name = ""
p1, p2, p3 = 0, 0, 0
font = 'addons/sans-beach/Sans Beach.ttf'  # Ruta a la fuente personalizada
font_size = '20sp'  # Tamaño de fuente para los textos
class InstScr(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        instr = Label(text=txt_instruction, font_name=font, font_size=font_size)
        lb1 = Label(text="Ingresar nombre:", halign='right', font_name=font, font_size=font_size)
        self.in_name = TextInput(multiline=False, font_name=font, font_size=font_size)
        lb2 = Label(text="Ingresa la edad:", halign='right', font_name=font, font_size=font_size)
        self.in_age = TextInput(text='7', multiline=False, font_name=font, font_size=font_size)

        self.btn = Button(text="Siguiente", size_hint=(0.3, 0.2), pos_hint={'center_x': 0.5}, font_name=font, font_size=font_size)
        self.btn.bind(on_press=self.next)

        line1 = BoxLayout(size_hint=(0.8, None), height='30sp')
        line2 = BoxLayout(size_hint=(0.8, None), height='30sp')
        line1.add_widget(lb1)
        line1.add_widget(self.in_name)
        line2.add_widget(lb2)
        line2.add_widget(self.in_age)
        outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
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
    def __init__(self, **kw):
        super().__init__(**kw)
        instr = Label(text=txt_test1, font_name=font, font_size=font_size)
        line = BoxLayout(size_hint=(0.8, None), height='30sp')
        lbl_result = Label(text="Ingresar el resultado: ", halign='right', font_name=font, font_size=font_size)
        self.in_result = TextInput(text='0', multiline=False, font_name=font, font_size=font_size)
        line.add_widget(lbl_result)
        line.add_widget(self.in_result)

        self.btn = Button(text="Siguiente", size_hint=(0.3, 0.2), pos_hint={'center_x': 0.5}, font_name=font, font_size=font_size)
        self.btn.bind(on_press=self.next)

        outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
        outer.add_widget(instr)
        outer.add_widget(line)
        outer.add_widget(self.btn)
        self.add_widget(outer)

    def next(self, instance):
        global p1
        try:
            p1 = int(self.in_result.text)
        except ValueError:
            p1 = 0
        self.manager.current = 'sits'

class ChekSits(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        instr = Label(text=txt_sits, font_name=font, font_size=font_size) 
        self.btn = Button(text='Siguiente',font_name=font, font_size=font_size, size_hint=(0.3, 0.2), pos_hint={'center_x': 0.5})
        self.btn.bind(on_press=self.next)
        outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
        outer.add_widget(instr)
        outer.add_widget(self.btn)
        self.add_widget(outer)
    
    def next(self, instance):
        self.manager.current = 'pulse2'

class PulseSrc2(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        instr = Label(text=txt_test3, font_name=font, font_size=font_size)
        line = BoxLayout(size_hint=(0.8, None), height='30sp')
        lbl_result = Label(text="Ingresar el resultado: ", font_name=font, font_size=font_size, halign='right')
        self.in_result = TextInput(text='0', multiline=False)
        line.add_widget(lbl_result)
        line.add_widget(self.in_result)
        
        line2 = BoxLayout(size_hint=(0.8, None), height='30sp')
        lbl_result2 = Label(text='Resultado despues de descanso: ', font_name=font, font_size=font_size, halign='right')
        self.in_result2 = TextInput(text='0', multiline=False)
        line2.add_widget(lbl_result2)
        line2.add_widget(self.in_result2)

        self.btn = Button(text="Siguiente", size_hint=(0.3, 0.2), pos_hint={'center_x': 0.5}, font_name=font, font_size=font_size)
        self.btn.bind(on_press=self.next)

        outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
        outer.add_widget(instr)
        outer.add_widget(line)
        outer.add_widget(line2)
        outer.add_widget(self.btn)
        self.add_widget(outer)

    def next(self, instance):
        global p2, p3
        try:
            p2 = int(self.in_result.text)
            p3 = int(self.in_result2.text) 
        except ValueError:
            p2, p3 = 0, 0
        self.manager.current = 'result'

class Result(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
        self.instr = Label(text='', font_name=font, font_size=font_size)
        self.outer.add_widget(self.instr)
        self.add_widget(self.outer)
    
    def on_enter(self):
        global name, p1, p2, p3, age
        
        # 1. Traer los textos base definidos en ruffier.py
        # Usamos 'globals().get' o valores por defecto por si ruffier.py está vacío
        txt_index = globals().get('txt_index', "Tu índice de Ruffier: ")
        txt_workheart = globals().get('txt_workheart', "Eficiencia cardíaca: ")
        txt_res = globals().get('txt_res', [
            "bajo.\n¡Ve a ver a tu médico lo antes posible!",
            "satisfactorio.\n¡Ve a ver a tu médico!",
            "promedio.\nPodría valer la pena realizar pruebas adicionales con el médico.",
            "superior al promedio",
            "alto"
        ])

        # 2. LÓGICA MATEMÁTICA DEL TEST DE RUFFIER
        if age < 7:
            self.instr.text = name + '\n' + "No hay datos para menores de 7 años."
            return

        # Multiplicamos por 4 cada pulso porque se tomaron en 15 segundos
        S = 4 * (p1 + p2 + p3)
        r_index = (S - 200) / 10
        
        # 3. DETERMINAR EL NIVEL "INSATISFACTORIO" SEGÚN LA EDAD
        # Para 7-8 años empieza en 21, y baja 1.5 puntos cada 2 años
        if age in [7, 8]:
            insat = 21.0
        elif age in [9, 10]:
            insat = 19.5
        elif age in [11, 12]:
            insat = 18.0
        elif age in [13, 14]:
            insat = 16.5
        else: # 15 años o más
            insat = 15.0

        # Escala de rangos restando las distancias de la tabla (4, 5, 5.5)
        debil = insat - 4
        satisf = debil - 5
        bueno = satisf - 5.5

        # 4. EVALUAR EL ÍNDICE OBTENIDO
        if r_index >= insat:
            res = txt_res[0]   # Bajo / Insatisfactorio
        elif r_index >= debil:
            res = txt_res[1]   # Débil
        elif r_index >= satisf:
            res = txt_res[2]   # Satisfactorio (Promedio)
        elif r_index >= bueno:
            res = txt_res[3]   # Bueno (Superior al promedio)
        else:
            res = txt_res[4]   # Perfecto (Alto)

        # 5. MOSTRAR RESULTADO EN PANTALLA
        self.instr.text = f"{name}\n\n{txt_index}{r_index}\n{txt_workheart}{res}"

class HeartCheck(App):
    def build(self):
        self.title = "Test de Ruffier"
        sm = ScreenManager()
        sm.add_widget(InstScr(name='instr'))
        sm.add_widget(PulseSrc(name='pulse1'))
        sm.add_widget(ChekSits(name='sits'))
        sm.add_widget(PulseSrc2(name='pulse2'))
        sm.add_widget(Result(name='result'))
        return sm

if __name__ == '__main__':
    HeartCheck().run()