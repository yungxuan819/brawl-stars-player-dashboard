# 🎮 Brawl Stars Player Dashboard

A data engineering and analytics project that pulls live player data from the **Brawl Stars API**, processes it through a full ETL pipeline, stores it in SQLite, and visualizes it in an interactive **Tableau dashboard** — giving players a deep look at their performance stats.

---

## 📊 Dashboard Preview

![Dashboard Overview](https://github.com/user-attachments/assets/f6c22f49-2362-45b2-a92a-c8c1dcb10db0)
![Dashboard Detail](https://github.com/user-attachments/assets/00b7f655-818f-4f4e-afa6-bba3b1d358c5)

---

## 🗂️ Project Structure

```
brawl-stars-player-dashboard/
│
├── brawl_etl.py              # ETL pipeline: Extract → Transform → Load
├── convert_to_csv.ipynb      # Exports SQLite tables to CSV
├── data_cleaning.ipynb       # Data cleaning and preprocessing
│
├── brawl_data_2.db           # SQLite database (raw + loaded data)
├── cleaned_battlelog.csv     # Cleaned battle log data
├── cleaned_brawlers.csv      # Cleaned brawlers data
├── cleaned_players.csv       # Cleaned player profile data
│
└── Brawl Stars Dashboard.twb # Tableau workbook
```

---

## ⚙️ How It Works

### 1. Extract
`brawl_etl.py` calls the [Brawl Stars API](https://developer.brawlstars.com/) to retrieve:
- **Player profiles** — trophies, club info, and stats
- **Battle logs** — recent match history and results
- **Brawlers** — all available brawlers and their attributes

### 2. Transform
Raw JSON responses are flattened and normalized into structured DataFrames using `pandas`.

### 3. Load
The transformed data is loaded into a local **SQLite database** (`brawl_data_2.db`) with three tables: `player`, `battlelog`, and `brawlers`.

### 4. Clean & Export
- `data_cleaning.ipynb` handles missing values, type casting, and feature selection
- `convert_to_csv.ipynb` exports the cleaned tables to CSV for use in Tableau

### 5. Visualize
The cleaned CSVs are connected to a **Tableau workbook** that renders interactive charts for performance analysis.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- A valid [Brawl Stars API token](https://developer.brawlstars.com/)
- Tableau Desktop (to open the `.twb` file)

### Installation

```bash
git clone https://github.com/yungxuan819/brawl-stars-player-dashboard.git
cd brawl-stars-player-dashboard
pip install requests pandas
```

### Configuration

Create a `config.py` file in the root directory:

```python
API_TOKEN = "your_api_token_here"
PLAYER_TAG = ["#YOURPLAYERTAG"]  # Add multiple tags to analyze more players
```

### Run the Pipeline

```bash
python brawl_etl.py
```

Then open and run the notebooks in order:
1. `convert_to_csv.ipynb`
2. `data_cleaning.ipynb`

Finally, open `Brawl Stars Dashboard.twb` in Tableau and connect it to the cleaned CSV files.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | ETL pipeline, data processing |
| Brawl Stars API | Data source |
| pandas | Data transformation |
| SQLite | Local data storage |
| Jupyter Notebook | Data cleaning & export |
| Tableau | Dashboard & visualization |

---

## 📌 Notes

- The API rate limit is handled with a 200ms delay between requests (`time.sleep(0.2)`).
- `config.py` is excluded from the repo — never commit your API token.
- The `.twb` Tableau file references local CSV paths; you may need to re-link the data sources after cloning.
