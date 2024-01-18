import matplotlib
matplotlib.use('agg')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.mosaicplot import mosaic

from pathlib import Path

DATA_PATH = Path('data')
PLOTS_PATH = Path('plots')

def main():
    df = pd.read_csv(DATA_PATH / 'REACH_HR_TEST_DATA_analyst.docx-EmbeddedFile.xlsm - Annex  1 - REACH Assessment Tes.csv')

    # Look for any odd values
    for col in df.columns:
        print(df[col].value_counts())

    # Create a new variable using the following table mapping
    improved_list = ['Protected dug well', 'Piped water to yard or plot', 'Piped water into dwelling (house)',
                    'Bottled Water', 'Tube well or borehold', 'Public tap or standpipe', 'Protected spring']

    # Create empty variable
    df['improved_water_source'] = ''
    # Assign value to variable based on criteria in table from Problem 2
    df.loc[df['drinking_water_source'].isin(improved_list), 'improved_water_source'] = 'Improved water source'
    df.loc[~df['drinking_water_source'].isin(improved_list), 'improved_water_source'] = 'Unimproved water source'
    df.loc[df['drinking_water_source'] == 'Other', 'improved_water_source'] = np.nan

    # Single headed households
    df_single = df.loc[df['single_headed_household'] == 'Yes']
    df_single.groupby('data_collection_round')['improved_water_source'].value_counts(dropna=False)
    df_single.groupby('data_collection_round')['improved_water_source'].value_counts(dropna=False, normalize=True)
    mosaic(df_single, ['data_collection_round', 'improved_water_source'], title='Single headed household')
    plt.tight_layout()
    plt.show()
    plt.savefig(PLOTS_PATH / 'Single_headed_household.png')

    # Diarrhea under 5

    df_improved = df.loc[df['improved_water_source'] == 'Improved water source']
    df_improved.groupby('data_collection_round')['diarrhea_under_5'].value_counts(dropna=False)
    df_improved.groupby('data_collection_round')['diarrhea_under_5'].value_counts(dropna=False, normalize=True)
    mosaic(df_improved, ['data_collection_round', 'diarrhea_under_5'], title='Diarrhea under 5 among households with improved water sources')
    plt.tight_layout()
    plt.show()
    plt.savefig(PLOTS_PATH / 'Diarrhea_under_5_improved_water_source.png')

if __name__ == '__main__':
    main()
    