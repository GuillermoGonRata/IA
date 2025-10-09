# Spam Detection Project

## Overview
The Spam Detection Project aims to develop a robust system for identifying unwanted emails (spam) using various detection techniques. The project utilizes a dataset of emails, which includes both spam and legitimate emails, to create and evaluate spam detection rules.

## Project Structure
The project is organized into the following directories and files:

- **data/**: Contains the dataset of emails.
  - `emails.csv`: A CSV file with columns for sender, subject, content, links, attachments, and a label indicating whether the email is spam or not.

- **src/**: Contains the source code for the spam detection system.
  - `SpamIndex.py`: Implements the main spam detection logic, including the `SpamDetectorReglas` class that analyzes emails based on predefined rules.
  - `rules.py`: Defines additional rules for spam detection, encapsulating specific detection logic for modular management.

- **notebooks/**: Contains Jupyter notebooks for data analysis.
  - `data_analysis.ipynb`: Used for exploring the email dataset, including visualizations and statistical analyses to identify patterns in spam and legitimate emails.

- **tests/**: Contains unit tests for the project.
  - `test_rules.py`: Includes tests for the functions and classes defined in `rules.py` to ensure the spam detection rules work as expected.

- **requirements.txt**: Lists the dependencies required for the project, such as pandas and other libraries needed for data processing and analysis.

## Objectives
- Develop a comprehensive understanding of spam detection mechanisms and email filtering principles.
- Gain practical experience in collecting, organizing, and analyzing data related to spam detection.
- Enhance critical thinking skills by creating and documenting rules for identifying unwanted emails.
- Foster collaboration and peer learning through the exchange and testing of spam detection systems.
- Reflect on the effectiveness of spam detection strategies and identify areas for improvement.

## Setup Instructions
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies using the following command:
   ```
   pip install -r requirements.txt
   ```
4. Ensure that the dataset (`emails.csv`) is located in the `data/` directory.

## Usage Guidelines
- To run the spam detection system, execute the `SpamIndex.py` script in the `src/` directory.
- Use the Jupyter notebook in the `notebooks/` directory for data analysis and exploration.
- Run the unit tests in the `tests/` directory to verify the functionality of the spam detection rules.

## Contribution
Contributions to the project are welcome! Please feel free to submit issues or pull requests for improvements or additional features.