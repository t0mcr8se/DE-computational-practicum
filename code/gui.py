import pyqtgraph as pg

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *
from smth import *
import numpy as np
# Setting canvas colors
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


class MainWindow(QDialog):
    def __init__(self):
        super().__init__()

        # Default parameters
        self.params = {
            "x0": 1,
            "y0": 2,
            "xn": 6,
            "steps": 10,
            "n0": 10,
            "N": 100
        }

        # Message for invalid input
        self.message_invalid_input = "You should provide a valid input:\n\n" \
                                     "1)  Each field 'steps', 'n0', 'N' should contain a positive integer.\n" \
                                     "2)  Each field 'x0', 'y0', 'X' should contain a real number.\n" \
                                     "3) 'x0' should be greater than 'X'.\n" \
                                     "4) 'x0' and 'X' should belong to an interval of validity.\n\n" \
                                     "Please, try again!"

        # # Message for greeting
        # self.message_greetings = "Hello, user!\n\n" \
        #                          "Please, provide input in the following format:\n\n" \
        #                          "1)  Each field 'steps', 'n0', 'N' should contain a positive integer.\n" \
        #                          "2)  Each field 'x0', 'y0', 'X' should contain a real number.\n" \
        #                          "3) 'x0' should be greater than 'X'.\n" \
        #                          "4) 'x0' and 'X' should belong to an interval of validity.\n\n" \
        #                          "Press OK and have fun!"
        # QMessageBox.information(self, 'Hello!', self.message_greetings)

        self.set_geometry(width = 800, height = 600)
        self.add_widgets()
        self.update_plots()

        self.show()

    def set_geometry(self, x_margin = 80, y_margin = 80, width = 1200, height = 600):
        self.setWindowTitle("Numerical methods")
        self.setGeometry(x_margin, y_margin, width, height)
        self.setMinimumSize(QSize(width, height))
        self.setMaximumSize(QSize(width, height))

    def add_widgets(self):
        # Grid for widgets
        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        # Button to plot
        self.button_trigger = QPushButton(text = "Apply Methods")
        self.button_trigger.clicked.connect(self.read_text_boxes)

        # Plots
        self.graph_plots = pg.PlotWidget()
        self.graph_plots.addLegend()
        self.graph_plots.showGrid(x = True, y = True)

        self.lte_plots = pg.PlotWidget()
        self.lte_plots.addLegend()
        self.lte_plots.showGrid(x = True, y = True)

        self.gte_plots = pg.PlotWidget()
        self.gte_plots.addLegend()
        self.gte_plots.showGrid(x = True, y = True)

        # Tab widget for different plots
        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(self.graph_plots, "Plots")
        self.tabWidget.addTab(self.lte_plots, "LTE")
        self.tabWidget.addTab(self.gte_plots, "GTE")

        # Labels
        self.label_x0 = QLabel('x0')
        self.textbox_x0 = QLineEdit()
        self.textbox_x0.setText(f"{self.params['x0']:.4f}")

        self.label_y0 = QLabel('y0')
        self.textbox_y0 = QLineEdit()
        self.textbox_y0.setText(f"{self.params['y0']:.4f}")

        self.label_xn = QLabel('X')
        self.textbox_xn = QLineEdit()
        self.textbox_xn.setText(f"{self.params['xn']:.4f}")

        self.label_steps = QLabel('Steps')
        self.textbox_steps = QLineEdit()
        self.textbox_steps.setText(f"{self.params['steps']}")

        self.label_n0 = QLabel('n0')
        self.textbox_n0 = QLineEdit()
        self.textbox_n0.setText(f"{self.params['n0']}")

        self.label_N = QLabel('N')
        self.textbox_N = QLineEdit()
        self.textbox_N.setText(f"{self.params['N']}")

        # Arranging widgets
        self.grid.addWidget(self.tabWidget, 0, 2, 0, 3)

        self.grid.addWidget(self.label_x0, 0, 0)
        self.grid.addWidget(self.textbox_x0, 0, 1)

        self.grid.addWidget(self.label_y0, 1, 0)
        self.grid.addWidget(self.textbox_y0, 1, 1)

        self.grid.addWidget(self.label_xn, 2, 0)
        self.grid.addWidget(self.textbox_xn, 2, 1)

        self.grid.addWidget(self.label_steps, 3, 0)
        self.grid.addWidget(self.textbox_steps, 3, 1)

        self.grid.addWidget(self.label_n0, 4, 0)
        self.grid.addWidget(self.textbox_n0, 4, 1)

        self.grid.addWidget(self.label_N, 5, 0)
        self.grid.addWidget(self.textbox_N, 5, 1)

        self.grid.addWidget(self.button_trigger, 6, 0, 1, 2)

        self.setLayout(self.grid)

    def read_text_boxes(self):
        # Read input from user
        x0 = self.textbox_x0.text()
        y0 = self.textbox_y0.text()
        xn = self.textbox_xn.text()
        steps = self.textbox_steps.text()
        n0 = self.textbox_n0.text()
        N = self.textbox_N.text()

        # Verify it
        if not NumericalMethod.valid_input({"x0": x0, "y0": y0, "xn": xn, "steps": steps, "n0": n0, "N": N}):
            QMessageBox.warning(self, 'Invalid input!', self.message_invalid_input)
            return

        # If OK, update parameters
        self.params = {
            "x0": float(x0),
            "y0": float(y0),
            "xn": float(xn),
            "steps": int(steps),
            "n0": int(n0),
            "N": int(N)
        }

        # Redraw plots
        self.update_plots()

    def update_plots(self):
        # Preparing canvas
        self.graph_plots.clear()
        self.lte_plots.clear()
        self.gte_plots.clear()

        # Convenient colors in RGB format
        colors = {
            'exact': pg.mkPen((51, 0, 0), width = 3),
            'euler': pg.mkPen((0, 153, 76), width = 4),
            'heun': pg.mkPen((255, 165, 0), width = 4),
            'runge': pg.mkPen((51, 51, 255), width = 4),
        }

        # Retrieve data for the first 2 plots
        x_exact, y_exact = NumericalMethod.exact_solution(self.params)
        x_euler, y_euler, lte_euler, gte_euler = Euler.apply(self.params)
        x_heun, y_heun, lte_heun, gte_heun = Heun.apply(self.params)
        x_runge, y_runge, lte_runge, gte_runge = Runge.apply(self.params)

        # Calculate worst GTE
        euler_worst_errors = []
        heun_worst_errors = []
        runge_worst_errors = []

        step_sizes = np.arange(self.params['n0'], self.params['N'] + 1)

        for n in step_sizes:
            tmp_values = self.params.copy()
            tmp_values['steps'] = n

            _, _, _, gte_euler = Euler.apply(tmp_values)
            _, _, _, gte_heun = Heun.apply(tmp_values)
            _, _, _, gte_runge = Runge.apply(tmp_values)

            euler_worst_errors.append(max(gte_euler))
            heun_worst_errors.append(max(gte_heun))
            runge_worst_errors.append(max(gte_runge))

        # Plot approximations
        self.graph_plots.plot(x_exact, y_exact, pen = colors['exact'], name = "Exact solution")
        self.graph_plots.plot(x_euler, y_euler, pen = colors['euler'], name = "Euler's method")
        self.graph_plots.plot(x_heun, y_heun, pen = colors['heun'], name = "Heun's method")
        self.graph_plots.plot(x_runge, y_runge, pen = colors['runge'], name = "Runge-Kutta method")

        # Plot LTE
        self.lte_plots.plot(x_euler, lte_euler, pen = colors['euler'], name = "Euler's method")
        self.lte_plots.plot(x_heun, lte_heun, pen = colors['heun'], name = "Heun's method")
        self.lte_plots.plot(x_runge, lte_runge, pen = colors['runge'], name = "Runge-Kutta method")

        # Plot worst GTE
        self.gte_plots.plot(step_sizes, euler_worst_errors, pen = colors['euler'], name = "Euler's method")
        self.gte_plots.plot(step_sizes, heun_worst_errors, pen = colors['heun'], name = "Heun's method")
        self.gte_plots.plot(step_sizes, runge_worst_errors, pen = colors['runge'], name = "Runge-Kutta method")