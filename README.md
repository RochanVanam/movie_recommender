# Movie Recommendation System
## Overview
This program recommends movies and TV shows based on a title of the user's choice. To run the program, follow the instructions below.

## Requirements
- Python 3.x
- Pandas
- Scikit-Learn

All required libraries and frameworks can be found at the top of ```movie_recommendations.py```.

## Installation
Clone the repository to your local machine using ```git clone https://github.com/RochanVanam/movie_recommender.git```.

## Usage
1. Make sure you have all the requirements properly installed.
2. Run ```movie_recommendations.py```.
3. The program uses 6 datasets, and combines the datasets into one dataset called ```processed_data.csv``` after preprocessing. If the combined dataset does not exist (the data is not preprocessed), it may take a minute until the next step.
4. The program will prompt you for a title to recommend movies/TV shows on. For your reference, a file called ```titles.txt``` contains all of the movie and TV show titles in the datasets. Enter a title.
5. The program will repeatedly prompt you until you want to stop. To stop the program, simply stop running it or exit the program.

## Data
The program uses 6 datasets ```amazonprime.csv```, ```appletv.csv```, ```disneyplus.csv```, ```hbomax.csv```, ```netflix.csv```, and ```paramountplus.csv``` located in the ```data/``` directory. These datasets contain information about movies and TV shows for their respective streaming platform. All datasets were created by Diego Enrique, and I obtained them on Kaggle. The links for the datasets are below.

- [Amazon Prime](https://www.kaggle.com/datasets/dgoenrique/amazon-prime-movies-and-tv-shows)
- [Apple TV](https://www.kaggle.com/datasets/dgoenrique/apple-tv-movies-and-tv-shows)
- [Disney Plus](https://www.kaggle.com/datasets/dgoenrique/disney-movies-and-tv-shows)
- [HBO Max](https://www.kaggle.com/datasets/dgoenrique/hbo-max-movies-and-tv-shows)
- [Netflix](https://www.kaggle.com/datasets/dgoenrique/netflix-movies-and-tv-shows)
- [Paramount Plus](https://www.kaggle.com/datasets/dgoenrique/paramount-movies-and-tv-shows)

Thank you!

**Rochan V:**
- [GitHub](https://github.com/RochanVanam)
- [LinkedIn](https://www.linkedin.com/in/rochanvanam/)
