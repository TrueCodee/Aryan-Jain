# 🌍 FIFA World Cup Dashboard

An interactive dashboard that visualizes FIFA World Cup winners and runner-ups from 1930 to 2022 using Choropleth maps.

![image](https://github.com/user-attachments/assets/953b6065-018f-4f45-b813-8fb32703eda9)

---

## 🔗 Demo

**Live demo:** [https://aryan-jain-qwuq.onrender.com](https://aryan-jain-qwuq.onrender.com)

---

## 🎯 Features

- 🗺️ **Interactive Choropleth Map**: Visualize World Cup data on a world map with color-coded countries.
- 🎛️ **Multiple View Modes**:
  - View **all countries** that have ever won a World Cup.
  - Select a **country** to see its full World Cup performance history.
  - Select a **specific year** to view the **winner and runner-up**.
- 📊 **Detailed Statistics**: Display historical insights, number of wins, runner-up placements, and tournament years.

---

## ⚙️ Technologies Used

- **[Dash](https://dash.plotly.com/)** – Web framework for Python
- **[Plotly](https://plotly.com/python/)** – Interactive visualizations
- **[Pandas](https://pandas.pydata.org/)** – Data manipulation
- **[NumPy](https://numpy.org/)** – Numerical operations
- **[Gunicorn](https://gunicorn.org/)** – WSGI server for deployment
- **[Render](https://render.com/)** – Cloud platform for hosting the app

---

## 🚀 Installation and Setup

### ✅ Prerequisites

- Python 3.9 or higher
- Git installed

---

### 🔧 Local Setup

```bash
# Clone the repository
git clone https://github.com/username/fifa-world-cup-dashboard.git
cd fifa-world-cup-dashboard

# Create and activate virtual environment (optional)
python -m venv venv
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt

# Run the app
python app.py

# Open your browser and go to
http://127.0.0.1:8050/
```
## ☁️ Deployment

This app is configured for deployment using **[Render](https://render.com/)**.

### 🚀 Steps to Deploy

1. **Fork** this repository to your GitHub account.
2. **Create a free account** on [Render](https://render.com/).
3. **Create a new Web Service** and connect it to your GitHub repository.
4. Render will automatically detect `app.py` and `render.yaml`, and deploy your app.

---

## 📊 Dataset

The dataset (`data.csv`) contains information from all FIFA World Cup finals, including:

- `Year`
- `Winner`
- `Runner-Up`
- `Winner_Country_Code`
- `Runner_Up_Country_Code`

📌 **Source**: [Wikipedia – List of FIFA World Cup finals](https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals)

---

## 🧭 Project Structure
fifa-world-cup-dashboard/
├── app.py                  # Main Dash app
├── data.csv                # FIFA World Cup finals data
├── requirements.txt        # Python dependencies
├── render.yaml             # Render deployment config
└── README.md               # Documentation


---

## 🎓 Assignment Context

This project was developed for **CP 321 – Data Visualization**, fulfilling the following requirements:

- ✅ Create and prepare a custom dataset
- ✅ Build an interactive dashboard using Dash and Plotly
- ✅ Enable users to:
  - View all countries that have won a World Cup
  - Select a country to see its World Cup wins
  - Select a year to see that World Cup's winner and runner-up
- ✅ Publish the application on a public server

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 🙏 Acknowledgments

- Data sourced from: [Wikipedia – FIFA World Cup finals](https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals)
- Inspired by the CP 321 – Data Visualization course and assignment


