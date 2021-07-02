from kivy.app import App
from kivy.uix.widget import Widget  # used to work with box layout
from kivy.properties import StringProperty, \
    ObjectProperty  # used to pass link the elements in the .kv file to the attributes in the code
from kivy.lang import Builder  # used to work with builder and apply any design file
from kivy.core.window import Window  # used to change the color of the back ground
from kivy.uix.screenmanager import ScreenManager, Screen  # used to apply multiple screens

import SummarizeFunction
from webScraping import ReadFromWebSite
from ReadDocument import ReadingFromPDF
from wordcounter.wordcounter import WordCounter


# building different pages
running_app = App.get_running_app()


class MainPage(Screen):
    pass


myText = ""


class TextPage(Screen):

    def __init__(self, text="", type_id=None, **kwargs):
        super(TextPage, self).__init__(**kwargs)
        self.text = text
        self.type_id = type_id

    ##########################################################

    def test(self):
        # print(self.text)
        # # self.ids.userWrittenText.text = "Hey we are here"
        # self.ids.userWrittenText.text = self.text
        # self.ids.userWrittenText.text = myText
        print("printed: " + self.ids.userWrittenText.text)
        summarized_text = SummarizeFunction.Summarize(self.ids.userWrittenText.text, self.ids.slider.value)
        self.ids.summarized_label_id.text = summarized_text

        word_counter = WordCounter(self.ids.userWrittenText.text, delimiter=' ')
        doc_len = word_counter.get_word_count()

        word_counter = WordCounter(summarized_text, delimiter=' ')
        sum_len = word_counter.get_word_count()

        rate = str( round(sum_len/doc_len,3)*100 ) + '%'
        self.ids.compression_Ratio_Label_ID.text = rate

        print("done")

    ##########################################################
    def compression_Rate_Picked(self, value):
        self.ids.compression_Ratio_Label_ID.text = value


class FilePage(Screen):

    def selectedFile(self, filePath):
        self.ids.fileSelectedtxt.text = filePath[0]
        layout = self.manager.get_screen('textPage').layout
        # print("test: "+ReadingFromPDF(filename=filePath[0], f=1, l=4))
        layout.text = ReadingFromPDF(filename=filePath[0], f=50, l=52)


class UrlPage(Screen):
    def UserUrl(self, url):
        self.ids.urltxt.text = url
        layout = self.manager.get_screen('textPage').layout
        layout.text = ReadFromWebSite(WEBSITE=url)

    pass


class PageManager(ScreenManager):
    pass


######################################################

# calling and building the design file (GUI)


TheApp = Builder.load_file('summarizeEnterpriseGUI.kv')


######################################################


######################################################
class SummarizeEnterprise(App):

    def build(self):
        # setting the color of the background
        Window.clearcolor = (52 / 255.0, 73 / 255.0, 94 / 255.0, 1)
        #####################################################
        # sm = ScreenManager()
        # sm.add_widget(MainPage())
        # sm.add_widget(TextPage(FileName_or_URL="", TypeTextRecieved=0))
        # sm.add_widget(FilePage())
        # sm.add_widget(UrlPage())

        return TheApp  # sm


if __name__ == '__main__':
    SummarizeEnterprise().run()