from datetime import date
import pandas as pd

data = pd.read_csv('PortfolioDetails.csv', delimiter=';')

# remove unnecessary columns
remove_columns = ['Plan', 
                  'Instrumententyp', 
                  'Instrument', 
                  'Marktpreis',
                  'Verfügbar ab', 
                  'Ablaufdatum', 
                  'Ausstehende Menge', 
                  'Verfügbare Menge', 
                  'Geschätzter aktueller ausstehender Wert', 
                  'Geschätzter aktueller verfügbarer Wert']
data.drop(columns= remove_columns, inplace=True)

# rename necessary columns
rename_columns = {'Allokationsdatum' : 'date',
                  'Beitragsart' : 'type',
                  'Ausübungspreis / Einstandspreis' : 'price',
                  'Zugewiesene Menge' : 'shares'
                  }
data.rename(columns= rename_columns, inplace=True)

# filter by current month
data['tmpDate'] = data['date']
data['tmpDate'] = pd.to_datetime(data['tmpDate'], infer_datetime_format=True)
today = pd.Timestamp.now()
month = today.floor('d') + pd.offsets.MonthEnd(0) - pd.offsets.MonthBegin(1)
data = data[(data['tmpDate'] > month)]
data.drop(columns=['tmpDate'], inplace=True)

# insert metadata
insert_columns = [
    #(column, value, loc)
    ('fee', 0, 1),
    ('isin', 'CH0012032048', 2),
    ('tax', 0, 5),
    ('currency', 'CHF', 7)
]
for column, value, loc in insert_columns:
    data.insert(column=column, value=value, loc=loc)

# rename columns
replace_values = [
    #(original, new)
    ('Kauf', 'Buy'),
    ('Unternehmensbeitrag', 'Buy'),
]

for original, newValue in replace_values:
    data.replace(original, newValue, inplace= True)

# remove 'CHF' from price column    
data['price'] = data['price'].str[4:]

# reorder columns
column_oder = [
    'date',
    'fee',
    'isin',
    'shares',
    'price',
    'tax',
    'type',
    'currency'
]
data = data[column_oder]

# export
data.to_csv('PortfolioDetails-' + str(date.today()) + '.csv', sep=';')
