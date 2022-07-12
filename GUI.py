from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.lang import Builder
import pdf_and_pil

KV = '''
<FirstWindow>:
    GridLayout:
        cols: 1
        rows: 3
        TextInput:
            id: name_of_document
        Button:
            text: 'Create'
            on_press: 
                root.make_pdf()
        Button:
            id: inver
            text: "Inversion"
            on_press:
                root.invert()

FirstWindow: 
                '''


class FirstWindow(Screen):
    def __init__(self, **kwargs):
        super(FirstWindow, self).__init__(**kwargs)

        self.inversion = True

    def invert(self):
        if self.inversion == True:
            self.inversion = False
            self.ids.inver.background_color = (1, 0, 0)
        else:
            self.inversion = True
            self.ids.inver.background_color = (0, 1, 0)



    def make_pdf(self):
        print()
        main.save_pdf(self.ids.name_of_document.text,self.inversion)


class PDFPrintingTool(App):
    def build(self):
        Window.clearcolor = (1, 1, 1)
        return Builder.load_string(KV)



