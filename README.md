# Contact Scoring System
Contact scoring system for sales lead prioritization using CSV data.

## Description
This project processes contact information from a CSV file and calculates a score for each contact based on three criteria: role, company size, and country. Contacts are then sorted according to their relevance for sales.

## Scoring Criteria
- **Role**: Higher scores for roles with greater decision-making power (CEO, CFO, CTO)
- **Company Size**: Higher scores for larger companies
- **Country**: Scores based on importance levels defined by tiers

## Usage
```
python challenge.py
```

## Requirements
- Python 3.x
- pandas

## File Structure
- `challenge.py`: Main script
- `data.csv`: Input data
- `contact_plan.csv`: Result sorted by relevance
