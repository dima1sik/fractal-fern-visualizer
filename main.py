import sys                                                                                                         
import random                                                                            

from PySide6.QtCore import QTimer, Qt 
                                                                        
                                                                                          
from PySide6.QtWidgets import (
    QApplication,                                     
    QComboBox,                   
    QGroupBox,                    
    QHBoxLayout,                                       
    QLabel,                   
    QMainWindow,                           
    QPushButton,        
    QSlider,          
    QVBoxLayout,                                     
    QWidget,                
)
import pyqtgraph as pg
                                                                                                                

class BarnsleyFernApp(QMainWindow):                                                                          
    def __init__(self):                                                                             
        super().__init__()                                                    
        self.setWindowTitle("Barnsley Fern Visualizer")                                          
        self.resize(1120, 710)                                                                     

        self.setup_state()                                             
        self.setup_presets()                                                               
        self.setup_timer()                                                                          
        self.setup_ui()                                 

    def setup_state(self):
                                                                                   
        self.points = []                                                                                                              
        self.x = 0.0                                                                                                    
        self.y = 0.0                                                                                                    
        self.is_running = False                                                                                                                                   
        self.current_preset = "Classic Fern"                                                                                                                             

    def setup_presets(self):
                                                                                                               
        self.presets = {                                                                                                   
            "Classic Fern": {                                                     
                "probs": [0.01, 0.85, 0.07, 0.07],                                                              
                "transforms": [                                                                                                                           
                    lambda x, y: (0.0, 0.16 * y),                                                                                                           
                    lambda x, y: (0.85 * x + 0.04 * y, -0.04 * x + 0.85 * y + 1.6),                                                                                                                 
                    lambda x, y: (0.20 * x - 0.26 * y, 0.23 * x + 0.22 * y + 1.6),                                                                                             
                    lambda x, y: (-0.15 * x + 0.28 * y, 0.26 * x + 0.24 * y + 0.44),                                                                                          
                ],
            },
            "Thin Fern": {
                "probs": [0.01, 0.88, 0.055, 0.055],
                "transforms": [
                    lambda x, y: (0.0, 0.16 * y),
                    lambda x, y: (0.88 * x + 0.02 * y, -0.02 * x + 0.88 * y + 1.4),
                    lambda x, y: (0.16 * x - 0.22 * y, 0.20 * x + 0.20 * y + 1.6),
                    lambda x, y: (-0.12 * x + 0.24 * y, 0.22 * x + 0.20 * y + 0.44),
                ],
            },
            "Wide Fern": {
                "probs": [0.01, 0.82, 0.085, 0.085],
                "transforms": [
                    lambda x, y: (0.0, 0.18 * y),
                    lambda x, y: (0.82 * x + 0.08 * y, -0.05 * x + 0.82 * y + 1.6),
                    lambda x, y: (0.26 * x - 0.30 * y, 0.25 * x + 0.24 * y + 1.6),
                    lambda x, y: (-0.20 * x + 0.30 * y, 0.25 * x + 0.24 * y + 0.44),
                ],
            },
            "Dense Fern": {
                "probs": [0.02, 0.84, 0.07, 0.07],
                "transforms": [
                    lambda x, y: (0.0, 0.20 * y),
                    lambda x, y: (0.84 * x + 0.05 * y, -0.03 * x + 0.84 * y + 1.55),
                    lambda x, y: (0.22 * x - 0.24 * y, 0.24 * x + 0.22 * y + 1.6),
                    lambda x, y: (-0.16 * x + 0.26 * y, 0.24 * x + 0.22 * y + 0.44),
                ],
            },
        }

    def setup_timer(self): 
                                                                            
        self.timer = QTimer()                                                                
        self.timer.timeout.connect(self.update_fern)                                                                   
                                                                                                                  

    def setup_ui(self):                                                               
        central_widget = QWidget()                                                                                             
        self.setCentralWidget(central_widget)                                                              

        self.main_layout = QHBoxLayout(central_widget)                                           
                                                                                                      

        self.setup_plot_widget()                                                  
        self.setup_controls_panel()                                                   

    def setup_plot_widget(self):                                              
        self.plot_widget = pg.PlotWidget()                                                                                         
        self.plot_widget.setBackground("w")                                                     
        self.plot_widget.hideAxis("left")                                                          
        self.plot_widget.hideAxis("bottom")                                                       
        self.plot_widget.setAspectLocked(True)                                                                                                
        self.plot_widget.setXRange(-3, 3, padding=0)                                                                                                  
        self.plot_widget.setYRange(0, 10, padding=0)                                                                          

        self.scatter = pg.ScatterPlotItem(                                                                                                               
            size=2,                                            
            pen=None,                                              
            brush=pg.mkBrush(0, 180, 0),                                                    
        )
        self.plot_widget.addItem(self.scatter)                                                                                                       

        self.main_layout.addWidget(self.plot_widget, 4)                                                                                                   
                                                                                                              

    def setup_controls_panel(self):                                                     
        self.controls_layout = QVBoxLayout()                                                                                              

        self.create_title_label()            
        self.create_buttons()         
        self.create_parameters_group()                  
        self.create_status_labels()                 

        self.controls_layout.addStretch()                                                              
        self.main_layout.addLayout(self.controls_layout, 1)                                                          
                                  

    def create_title_label(self):                                        
        title_label = QLabel("Barnsley Fern")                                          
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")                                                       
        self.controls_layout.addWidget(title_label)                                        

    def create_buttons(self):                           
        self.start_button = QPushButton("Start")
        self.pause_button = QPushButton("Pause")
        self.reset_button = QPushButton("Reset")
                           

        self.start_button.clicked.connect(self.start_animation)
        self.pause_button.clicked.connect(self.pause_animation)
        self.reset_button.clicked.connect(self.reset_fern)
                                       

        self.controls_layout.addWidget(self.start_button)
        self.controls_layout.addWidget(self.pause_button)
        self.controls_layout.addWidget(self.reset_button)
                                                       

    def create_parameters_group(self):                                
        parameters_group = QGroupBox("Parameters")                                        
        parameters_layout = QVBoxLayout()                                                          
        parameters_group.setLayout(parameters_layout)                                       

        self.create_points_per_frame_controls(parameters_layout)
        self.create_max_points_controls(parameters_layout)
        self.create_point_size_controls(parameters_layout)
        self.create_speed_controls(parameters_layout)
        self.create_color_mode_controls(parameters_layout)
        self.create_preset_controls(parameters_layout)
                                               

        self.controls_layout.addWidget(parameters_group)                                                 

    def create_points_per_frame_controls(self, layout):                                                                  
        self.points_per_frame_label = QLabel("Points per frame: 500")                                                    
        self.points_per_frame_slider = QSlider(Qt.Horizontal)                                    
        self.points_per_frame_slider.setRange(10, 5000)                                    
        self.points_per_frame_slider.setValue(500)                                       
        self.points_per_frame_slider.valueChanged.connect(self.update_parameter_labels)                                                                          

        layout.addWidget(self.points_per_frame_label)                                                  
        layout.addWidget(self.points_per_frame_slider)                                         

    def create_max_points_controls(self, layout):                                           
        self.max_points_label = QLabel("Max points: 20000")                       
        self.max_points_slider = QSlider(Qt.Horizontal)                                    
        self.max_points_slider.setRange(1000, 100000)                   
        self.max_points_slider.setSingleStep(1000)                                                                                        
        self.max_points_slider.setValue(20000)                             
        self.max_points_slider.valueChanged.connect(self.update_parameter_labels)                                             

        layout.addWidget(self.max_points_label)                               
        layout.addWidget(self.max_points_slider)                                

    def create_point_size_controls(self, layout):                                                                                                 
        self.point_size_label = QLabel("Point size: 2")                                            
        self.point_size_slider = QSlider(Qt.Horizontal)                                   
        self.point_size_slider.setRange(1, 8)                            
        self.point_size_slider.setValue(2)                                       
        self.point_size_slider.valueChanged.connect(self.update_point_size)                                                                                        

        layout.addWidget(self.point_size_label)                                                     
        layout.addWidget(self.point_size_slider)                                         

    def create_speed_controls(self, layout):                                                                
        self.speed_label = QLabel("Timer interval: 30 ms")                                                    
        self.speed_slider = QSlider(Qt.Horizontal)                                   
        self.speed_slider.setRange(10, 200)                            
        self.speed_slider.setValue(30)                                       
        self.speed_slider.valueChanged.connect(self.update_speed)                                                                                       

        layout.addWidget(self.speed_label)                                                  
        layout.addWidget(self.speed_slider)                                        

    def create_color_mode_controls(self, layout):                                                       
        self.color_mode_label = QLabel("Color mode:")
        self.color_mode_combo = QComboBox()                                                                                                                
        self.color_mode_combo.addItems(["Classic Green", "Black & White", "By Transform"])                                                                                                                                
        self.color_mode_combo.currentTextChanged.connect(self.refresh_plot)                                                                                                                        

        layout.addWidget(self.color_mode_label)
        layout.addWidget(self.color_mode_combo)

    def create_preset_controls(self, layout):                                                               
        self.preset_label = QLabel("Fern preset:")
        self.preset_combo = QComboBox()                              
        self.preset_combo.addItems(["Classic Fern", "Thin Fern", "Wide Fern", "Dense Fern"])  
        self.preset_combo.currentTextChanged.connect(self.change_preset)

        layout.addWidget(self.preset_label)
        layout.addWidget(self.preset_combo)

    def create_status_labels(self):                                           
        self.status_label = QLabel("Status: Ready")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold;")                                         
        self.controls_layout.addWidget(self.status_label)                                            
 
        self.points_label = QLabel("Generated points: 0")
        self.points_label.setStyleSheet("font-size: 14px;")
        self.controls_layout.addWidget(self.points_label)                                                        

    def update_parameter_labels(self):                                                                            
        self.points_per_frame_label.setText(                                                                                                            
            f"Points per frame: {self.points_per_frame_slider.value()}"                                      
                                                                             
                                               
                                                                                                 
                                                                    
        )
        self.max_points_label.setText(                                                            
            f"Max points: {self.max_points_slider.value()}"                                           
        )

    def update_point_size(self):                                               
                                                                                                                         
        size = self.point_size_slider.value()                                                                                                                   
        self.point_size_label.setText(f"Point size: {size}")                                          
        self.scatter.setSize(size)                                              

    def update_speed(self):                              
                                                                                                                                
        interval = self.speed_slider.value()                                                                                                          
        self.speed_label.setText(f"Timer interval: {interval} ms")                                                        

        if self.is_running:                                                                                                                 
            self.timer.start(interval)                                                                                                                                   

    def start_animation(self): 
                                                                              
        if not self.is_running:                                                                                                                                    
            self.is_running = True                                                                                                                   
            self.status_label.setText("Status: Running")                                                                                                                 
            self.timer.start(self.speed_slider.value())                              
                                                                                                                            

    def pause_animation(self):
                                                                                
        if self.is_running:                                                                                                            
            self.is_running = False                                                                                                                
            self.timer.stop()                                                                                                                          
            self.status_label.setText("Status: Paused")                                                                                                                   

    def reset_fern(self): 
                                                                                       

        self.is_running = False                                                                                                                 
        self.timer.stop()                                                                                                     
        self.points = []                                                   
        self.x = 0.0                                                          
        self.y = 0.0                                                          
        self.scatter.setData([], [])                                      
        self.points_label.setText("Generated points: 0")                                              
        self.status_label.setText("Status: Ready")                                    

    def change_preset(self):
                                                                                                             

        self.current_preset = self.preset_combo.currentText()                                                                  
                                                                                                                    

        self.reset_fern()                                                 
                                                                                                       

    def choose_transform(self):
                                                                                                

        preset = self.presets[self.current_preset]
                                                                                    
                                                                                                              

        probs = preset["probs"]
                                                                     
                                                                                        

        transforms = preset["transforms"]
                                                                       
                                                                                      

        r = random.random()                                               
                                                                             

        cumulative = 0.0                                                           
                                                            

        for index, probability in enumerate(probs):                                                   
                                                                                                        

            cumulative += probability                                                                     
                                                                                                     

            if r <= cumulative:                                                                                   
                                                            

                return index, transforms[index]                                                                                                           
                                                                                 

        last_index = len(transforms) - 1                                                                 
                                                                                   

        return last_index, transforms[last_index]                                                           
                                                                             

    def next_point(self, x, y):
                                                                                                      

        transform_index, transform = self.choose_transform()                                                 
                                                                                                                        

        x_new, y_new = transform(x, y)                                                                            
                                                               

        return x_new, y_new, transform_index                                                 
                                                                                          


    def get_brushes(self):
                                                                                    

        mode = self.color_mode_combo.currentText()                                                                                
                                                           

        if mode == "Classic Green":                                                      
            return [pg.mkBrush(0, 180, 0) for _ in self.points]                                                                                           
                                                                                            

        if mode == "Black & White":                                                      
            return [pg.mkBrush(40, 40, 40) for _ in self.points]                                                                                
                                                                                      

        transform_colors = {                                                        
                                                                                      

            0: pg.mkBrush(20, 100, 20),                                                        
                                                                                                        
            1: pg.mkBrush(0, 170, 0),                                                        
                                                                           
            2: pg.mkBrush(100, 200, 100),                                                        
                                                              
            3: pg.mkBrush(0, 120, 60),                                                        
                                                                             
        }
        return [transform_colors[point[2]] for point in self.points]                                                              
                                                                                                                                                      

    def refresh_plot(self): 
                                                                              

        if not self.points:                                                           
                                                         

            self.scatter.setData([], [])                                                                    
                                                                

            return                                            
                                                                  

        xs = [point[0] for point in self.points]                               
                                                                        

        ys = [point[1] for point in self.points]                               
                                                                         

        brushes = self.get_brushes()                                            
                                                                                              

        self.scatter.setData(x=xs, y=ys, brush=brushes)                                                                                                      
                                                                                           

    def update_fern(self):
                                                                                                                 

        max_points = self.max_points_slider.value()                                                        
                                                              

        points_per_frame = self.points_per_frame_slider.value()                                                              
                                                                    

        if len(self.points) >= max_points:                                                                               
                                                                                       

            self.is_running = False                                                         
                                                                

            self.timer.stop()                                  
                                                                                       

            self.status_label.setText("Status: Finished")                                                      
                                                                             

            return                                      
                                                                           

        new_points_count = min(points_per_frame, max_points - len(self.points))                                                                  
                                                                                                                

        for _ in range(new_points_count):                                                                     
                                                                             

            self.x, self.y, transform_index = self.next_point(self.x, self.y)                                                                               
                                                                                                                    

            self.points.append((self.x, self.y, transform_index))                                                        
                                                                                                                             

        self.refresh_plot()                                           
                                                        

        self.points_label.setText(f"Generated points: {len(self.points)}")                                                         
                                                               


if __name__ == "__main__":                                                 
                                                      

    app = QApplication(sys.argv)                                                
                                                                                

    window = BarnsleyFernApp()                                                                                                                                                               
    window.show()                                                                                                       
    sys.exit(app.exec())                                                  
                                                                                                                                     