import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QComboBox, QScrollArea
from predict_me_unified import get_top_books, predict_book_choice, get_top_dvds, predict_dvd_choice, get_top_musics, predict_music_choice, get_top_videos, predict_video_choice

JSON_FILE_PATH = '/Users/spencer/Desktop/CS-458-Fall-2023/Amazon Final Project/json/amazon-meta.json'


class PredictMeApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main Window Properties
        self.setWindowTitle('Predict Me: Recommendations')
        self.setGeometry(100, 100, 800, 600)

        # Central Widget and Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Category Selection
        self.category_combo = QComboBox()
        self.category_combo.addItems(['Books', 'DVDs', 'Music', 'Videos'])
        layout.addWidget(self.category_combo)

        # Suggest Button
        self.suggest_button = QPushButton('Suggest Top 5')
        self.suggest_button.clicked.connect(self.suggest_top_five)
        layout.addWidget(self.suggest_button)

        # Predict Button
        self.predict_button = QPushButton('Predict My Choice')
        self.predict_button.clicked.connect(self.predict_choice)
        layout.addWidget(self.predict_button)


        self.scroll_area = QScrollArea()
        self.results_label = QLabel('Results will be displayed here')
        self.results_label.setWordWrap(True)  # Enable word wrap
        self.scroll_area.setWidget(self.results_label)
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)
        self.category_combo.setMaximumWidth(200)
        self.suggest_button.setMaximumWidth(200)
        self.predict_button.setMaximumWidth(200)


    def suggest_top_five(self):
        category = self.category_combo.currentText()
        if category == 'Books':
            results = get_top_books(JSON_FILE_PATH)
        elif category == 'DVDs':
            results = get_top_dvds(JSON_FILE_PATH)
        elif category == 'Music':
            results = get_top_musics(JSON_FILE_PATH)
        elif category == 'Videos':
            results = get_top_videos(JSON_FILE_PATH)

        # Formatting the results for display
        formatted_results = f"Top 5 Suggested {category} Based on Avg Rating and Num Ratings:\n"
        for item in results:
            title = item.get('title', 'N/A')
            avg_rating = item.get('avg_rating', 'N/A')
            num_ratings = item.get('num_ratings', 'N/A')
            formatted_results += f"Title: {title}, Avg Rating: {avg_rating}, Num Ratings: {num_ratings}\n"
        
        self.results_label.setText(formatted_results)



    def predict_choice(self):
        category = self.category_combo.currentText()
        if category == 'Books':
            prediction = predict_book_choice(JSON_FILE_PATH)
        elif category == 'DVDs':
            prediction = predict_dvd_choice(JSON_FILE_PATH)
        elif category == 'Music':
            prediction = predict_music_choice(JSON_FILE_PATH)
        elif category == 'Videos':
            prediction = predict_video_choice(JSON_FILE_PATH)

        # Sort by predicted_salesrank and get the top 5
        top_predictions = prediction.sort_values(by='predicted_salesrank').head(5)

        # Formatting the prediction for display
        formatted_prediction = "\n".join([f"{item['title']}: {item['predicted_salesrank']}" for item in top_predictions.to_dict(orient='records')])
        self.results_label.setText(f"Top 5 Predicted {category} Choices:\n{formatted_prediction}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = PredictMeApp()
    main_window.show()
    sys.exit(app.exec_())
    
