import customtkinter as ctk
from .components.sidebar import Sidebar
from .components.navigation_bar import NavigationBar
from .views import *
from modules.data_manager import DataManager
from modules.fasttext_manager import FastTextManager


class MainWindow(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(fill="both", expand=True)

        self.data_manager = DataManager()
        self.fasttext_manager = FastTextManager()

        self.steps = [
            ("Data Loading", DataLoadingView),
            ("Data Exploration", DataExplorationView),
            ("Data Cleaning", DataCleaningView),
            ("Text Processing", TextProcessingView),
            ("Label Preparation", LabelPreparationView),
            ("Data Splitting", DataSplittingView),
            ("Model Configuration", ModelConfigurationView),
            ("Model Training", ModelTrainingView),
            ("Model Export", ModelExportView)
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

        self.load_model_button = ctk.CTkButton(
            self, text="Load Model", fg_color="#4CAF50", command=self.open_load_model_view
        )
        self.load_model_button.place(relx=0.01, rely=0.8, relwidth=0.18, relheight=0.04)

        self.current_frame = None
        self.switch_frame(self.current_index)

    def switch_frame(self, index):
        if self.current_frame is not None:
            self.current_frame.place_forget()

        self.current_index = index
        view_class = self.steps[index][1]

        if view_class in [ModelConfigurationView, ModelTrainingView, ModelExportView]:
            manager = self.fasttext_manager
            manager_arg_name = "fasttext_manager"
        else:
            manager = self.data_manager
            manager_arg_name = "data_manager"

        if index not in self.view_instances:
            kwargs = {
                "master": self.container,
                "navigation_bar": self.navigation_bar
            }
            kwargs[manager_arg_name] = manager

            self.view_instances[index] = view_class(**kwargs)
            self.navigation_bar.set_next_enabled(False)

        self.current_frame = self.view_instances[index]
        self.current_frame.place(relx=0, rely=0.1, relwidth=1.0, relheight=0.9)

        self.navigation_bar.update_title(self.steps[index][0])
        self.navigation_bar.set_back_enabled(index > 0)

        if isinstance(self.current_frame, (DataCleaningView, TextProcessingView, LabelPreparationView)):
            self.navigation_bar.set_next_enabled(True)

        self.sidebar.highlight_step(index)

    def go_back(self):
        if self.current_index > 0:
            self.switch_frame(self.current_index - 1)

    def go_next(self):
        if self.current_index < len(self.steps) - 1:
            self.switch_frame(self.current_index + 1)

    def open_load_model_view(self):
        load_model_view = LoadModelView(
            master=self.container,
            fasttext_manager=self.fasttext_manager
        )
        if self.current_frame is not None:
            self.current_frame.place_forget()

        self.current_frame = load_model_view
        self.current_frame.place(relx=0, rely=0.1, relwidth=1.0, relheight=0.9)
        self.navigation_bar.update_title("Load Pretrained Model")
