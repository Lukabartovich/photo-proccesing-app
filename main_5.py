from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from time import strftime
import cv2

"""
0.53, 0.33, 0.54, 1
0.1, 0.73, 0.88, 1  
0.77, 0.36, 0.18, 1

"""


Builder.load_file('layout_5.kv')


class Cameras(Screen):
    def start(self):
        self.ids.camera.play = True
        self.ids.camera.texture = self.ids.camera.texture
        self.ids.camera.opacity = 1

    def capture(self):
        file_name = strftime('%Y%m%d-%H%M%S')
        self.ids.camera.export_to_png(f'files/{file_name}.png')
        self.manager.current = 'change'
        self.manager.current_screen.ids.image.source = \
            f'files/{file_name}.png'


class Change(Screen):
    def b_and_w(self):
        file_name = strftime('%Y%m%d-%H%M%S')
        path = self.ids.image.source
        image = cv2.imread(path, 0)

        gray = cv2.imwrite(f'change/{file_name}.png', image)
        self.manager.current = 'save'
        self.manager.current_screen.ids.image2.source = \
            f'change/{file_name}.png'

        print(self.manager.current_screen.ids.image2.source)

    def blur(self):
        file_name = strftime('%Y%m%d-%H%M%S')
        path = self.ids.image.source
        image = cv2.imread(path)

        cascade = cv2.CascadeClassifier('faces.xml')

        faces = cascade.detectMultiScale(image, 1.1, 4)

        for (x, y, w, h) in faces:
            image[y:y+h, x:x+w] = cv2.blur(image[y:y+h, x:x+w], (80, 80))

        blured = cv2.imwrite(f'change/{file_name}.png', image)
        self.manager.current = 'save'
        self.manager.current_screen.ids.image2.source = \
            f'change/{file_name}.png'

    def normal(self):
        file_name = strftime('%Y%m%d-%H%M%S')
        path = self.ids.image.source
        self.manager.current = 'save'
        self.manager.current_screen.ids.image2.source = \
            path


class Save(Screen):
    def back(self):
        self.manager.current = 'cameras'
        self.manager.current_screen.ids.camera.play = False
        self.manager.current_screen.ids.camera.opacity = 0


class Root(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return Root()

if __name__ == '__main__':
    MainApp().run()