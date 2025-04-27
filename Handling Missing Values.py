import pandas as pd

d = {
'height': [175, 160, 185, None, 170, 160, None],
'weight': [70, 60, None, 80, None, 55, 68],
'education': ['Bachelor', 'Master', 'PhD', 'Bachelor', 'Master', 'PhD', 'Bachelor'],
'region': ['North', 'South', 'West', 'East', 'North', 'West', 'East']
}
df = pd.DataFrame(d)
print("Initial DataFrame:")
print(df)

def fill_m(df_in, r_col):
    n_cols = df_in.select_dtypes(include='number').columns
    r_meds = df_in.groupby(r_col)[n_cols].median()
    for c in n_cols:
        for r in df_in[r_col].unique():
             if r in r_meds.index:
                 m_val = r_meds.loc[r, c]
                 if pd.notna(m_val):
                     df_in.loc[(df_in[r_col] == r) & (df_in[c].isna()), c] = m_val
    return df_in

df_f = fill_m(df.copy(), 'region')
print("\nDataFrame after replacing missing values with region-specific median:")
print(df_f)
