# NextPage

### Introduction
NextPage is an application designed to enrich the reading experience by utilizing data visualization and personalized book recommendations. By leveraging the Goodreads dataset, the project aims to provide users with insights into book trends and reader preferences, helping them discover books that match their interests.

### Data
- **Source:** The data used in this project is sourced from Kaggle, featuring an extensive collection of books and reviews from the Goodreads platform.

### Main Features
- **Data Visualization:** Offers valuable insights into book trends and reader preferences, helping users make informed decisions about their next reads.
- **Filtering:** Allows users to explore books based on various criteria such as genre, rating, and more, enabling a tailored browsing experience.
- **Book Recommendation System:** Utilizes similarity calculations based on rating and genre to recommend a curated list of 10 books that the user is likely to enjoy.

## Running the Application

### Requirements
Ensure you have all necessary dependencies installed to use the application. For detailed dependency information, please refer to the `requirements.txt` file.

### Setup Instructions
---
**Clone the repository:**
```
git clone https://github.com/1stChaS/NextPage.git
```


  ### Create a virtual environment and install dependencies
---
1. Change your directory to NextPage/code
```
cd NextPage/code
git checkout preview
```
2. Create virtual environment using this command.
```
python3.12 -m venv env
```

3. Activate the virtual environment
```
# On Linux or MacOS
```
source env/bin/activate
```

# On MS Windows
```
env\Scripts\activate
```

4. Installing Dependencies
```
pip install -r requirements.txt
```

5. Run the application:
# On Linux or MacOS
```
python3 main.py
```

# On MS Windows
```
python main.py
```

