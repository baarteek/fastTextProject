import customtkinter as ctk
from .components.sidebar import Sidebar
from .components.navigation_bar import NavigationBar
from .views import *
from modules.data_manager import DataManager

class MainWindow(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(fill="both", expand=True)

        self.data_manager = DataManager()

        self.steps = [
            ("Data Loading", DataLoadingView),
            ("Data Exploration", DataExplorationView),
            ("Data Cleaning", DataCleaningView),
            ("Text Processing", TextProcessingView),
            ("Label Preparation", LabelPreparationView),
            ("Data Splitting", DataSplittingView),
            ("FastText Formatting", FastTextFormattingView),
            ("Data Validation", DataValidationView)
        ]
        self.current_index = 0
        self.view_instances = {} 

        self.sidebar = Sidebar(self, self.switch_frame, steps=[step[0] for step in self.steps])
        self.sidebar.place(relx=0, rely=0, relwidth=0.2, relheight=1.0)
        self.container = ctk.CTkFrame(self)
        self.container.place(relx=0.2, rely=0, relwidth=0.8, relheight=1.0)
        
        self.navigation_bar = NavigationBar(
            self.container, 
            title=self.steps[self.current_index][0], 
            on_back=self.go_back, 
            on_next=self.go_next
        )
        self.navigation_bar.place(relx=0, rely=0, relwidth=1.0, relheight=0.1)
        self.navigation_bar.set_next_enabled(False)

        self.current_frame = None
        self.switch_frame(self.current_index)

    def switch_frame(self, index):
        if self.current_frame is not None:
            self.current_frame.place_forget()

        self.current_index = index
        view_class = self.steps[index][1]

        if index not in self.view_instances:
            self.view_instances[index] = view_class(self.container, data_manager=self.data_manager, navigation_bar=self.navigation_bar)
            self.navigation_bar.set_next_enabled(False)

        self.current_frame = self.view_instances[index]
        self.current_frame.place(relx=0, rely=0.1, relwidth=1.0, relheight=0.9)

        self.navigation_bar.update_title(self.steps[index][0])
        self.navigation_bar.set_back_enabled(index > 0)

        if isinstance(self.current_frame, DataExplorationView) or isinstance(self.current_frame, DataCleaningView):
            self.navigation_bar.set_next_enabled(True)
        
        self.sidebar.highlight_step(index)

    def go_back(self):
        if self.current_index > 0:
            self.switch_frame(self.current_index - 1)

    def go_next(self):
        if self.current_index < len(self.steps) - 1:
            self.switch_frame(self.current_index + 1)
