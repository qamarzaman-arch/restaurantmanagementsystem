from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QGridLayout, QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtCharts import QChart, QChartView, QPieSeries, QBarSeries, QBarSet, QBarCategoryAxis, QLineSeries, QValueAxis, QDateTimeAxis
from PyQt6.QtGui import QPainter

class DashboardScreen(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)

        layout.addWidget(QLabel("<h1 style='color: #2c3e50;'>Dashboard</h1>"))

        # Stats Cards
        stats_layout = QGridLayout()
        self.total_sales = self.create_stat_card("Sales Today", "0.00")
        self.total_expenses = self.create_stat_card("Expenses Today", "0.00")
        self.total_orders = self.create_stat_card("Orders Today", "0")
        self.active_tables = self.create_stat_card("Active Tables", "0")
        self.low_stock_card = self.create_stat_card("Low Stock Items", "0")
        self.low_stock_card.setStyleSheet(self.low_stock_card.styleSheet() + " QFrame { border-left: 5px solid #e74c3c; }")

        stats_layout.addWidget(self.total_sales, 0, 0)
        stats_layout.addWidget(self.total_expenses, 0, 1)
        stats_layout.addWidget(self.total_orders, 0, 2)
        stats_layout.addWidget(self.active_tables, 1, 0)
        stats_layout.addWidget(self.low_stock_card, 1, 1)
        layout.addLayout(stats_layout)

        # Charts Row 1
        charts_layout1 = QHBoxLayout()
        self.category_chart_view = self.create_category_chart()
        self.top_items_chart_view = self.create_top_items_chart()

        charts_layout1.addWidget(self.category_chart_view, 1)
        charts_layout1.addWidget(self.top_items_chart_view, 1)
        layout.addLayout(charts_layout1)

        # Charts Row 2
        self.trend_chart_view = self.create_trend_chart()
        layout.addWidget(self.trend_chart_view)

        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        self.refresh_stats()

    def create_stat_card(self, title, value):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #dcdde1;
                padding: 15px;
            }
        """)
        layout = QVBoxLayout(frame)
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #7f8c8d; font-size: 13px;")
        layout.addWidget(title_label)
        value_label = QLabel(value)
        value_label.setStyleSheet("color: #2c3e50; font-size: 22px; font-weight: bold;")
        layout.addWidget(value_label)
        frame.value_label = value_label
        return frame

    def create_category_chart(self):
        chart = QChart()
        chart.setTitle("Sales by Category")
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        chart_view.setMinimumHeight(300)
        return chart_view

    def create_top_items_chart(self):
        chart = QChart()
        chart.setTitle("Top 5 Selling Items")
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        chart_view.setMinimumHeight(300)
        return chart_view

    def create_trend_chart(self):
        chart = QChart()
        chart.setTitle("7-Day Sales Trend")
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        chart_view.setMinimumHeight(300)
        return chart_view

    def refresh_stats(self):
        # Update Stats Cards
        orders = self.db.get_all_orders(status='Completed')
        # Filter for today
        import datetime
        today = datetime.date.today().isoformat()
        today_orders = [o for o in orders if o['created_at'].startswith(today)]
        total_revenue = sum(o['total'] for o in today_orders)
        count = len(today_orders)

        total_expenses = self.db.get_total_expenses_today()

        tables = self.db.get_tables()
        active = len([t for t in tables if t['status'] == 'Occupied'])

        inventory = self.db.get_inventory()
        low_stock_count = len([i for i in inventory if i['quantity'] <= i['min_threshold']])

        self.total_sales.value_label.setText(f"Rs. {total_revenue:.2f}")
        self.total_expenses.value_label.setText(f"Rs. {total_expenses:.2f}")
        self.total_orders.value_label.setText(str(count))
        self.active_tables.value_label.setText(str(active))
        self.low_stock_card.value_label.setText(str(low_stock_count))

        self.update_charts()

    def update_charts(self):
        self.update_category_chart()
        self.update_top_items_chart()
        self.update_trend_chart()

    def update_category_chart(self):
        series = QPieSeries()
        data = self.db.get_sales_by_category()
        for item in data:
            series.append(item['name'], item['total_sales'])

        self.category_chart_view.chart().removeAllSeries()
        self.category_chart_view.chart().addSeries(series)
        self.category_chart_view.chart().legend().setAlignment(Qt.AlignmentFlag.AlignRight)

    def update_top_items_chart(self):
        series = QBarSeries()
        set0 = QBarSet("Quantity")

        data = self.db.get_top_selling_items()
        categories = []
        for item in data:
            set0.append(item['total_qty'])
            categories.append(item['name'])

        series.append(set0)

        chart = self.top_items_chart_view.chart()
        chart.removeAllSeries()
        chart.addSeries(series)

        # Clear existing axes
        for axis in chart.axes():
            chart.removeAxis(axis)

        axisX = QBarCategoryAxis()
        axisX.append(categories)
        chart.addAxis(axisX, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axisX)

        axisY = QValueAxis()
        chart.addAxis(axisY, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axisY)

    def update_trend_chart(self):
        series = QLineSeries()
        series.setName("Sales")

        data = self.db.get_weekly_sales_trend()
        categories = []
        for i, item in enumerate(data):
            series.append(i, item['daily_total'])
            categories.append(item['sale_date'])

        chart = self.trend_chart_view.chart()
        chart.removeAllSeries()
        chart.addSeries(series)

        for axis in chart.axes():
            chart.removeAxis(axis)

        axisX = QBarCategoryAxis()
        axisX.append(categories)
        chart.addAxis(axisX, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setTitleText("Total Sales (Rs.)")
        chart.addAxis(axisY, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axisY)
