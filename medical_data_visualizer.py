import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# não vou comentar
df = pd.read_csv('medical_examination.csv')

df['overweight'] = df['weight'] / ((df['height'] / 100) ** 2)
df['overweight'] = (df['overweight'] > 25).astype(int)

df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)
def draw_cat_plot():
    df_cat = pd.melt(df, 
                     id_vars=['cardio'], 
                     value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    df_cat = df_cat.groupby(['cardio', 'variable', 'value'], as_index=False).size().rename(columns={"size": "total"})

    fig = sns.catplot(x='variable', y='total', hue='value', col='cardio', 
                      data=df_cat, kind='bar', height=5, aspect=1)

    fig = fig.fig
    fig.savefig('catplot.png')
    return fig



def draw_heat_map():
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # 12. Calcular a matriz de correlação
    corr = df_heat.corr()

    # 13. Gerar máscara para a parte superior do triângulo
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 14. Definir figura e eixos
    fig, ax = plt.subplots(figsize=(12, 8))

    # 15. Desenhar o mapa de calor usando sns.heatmap
    sns.heatmap(corr, mask=mask, annot=True, fmt=".1f", linewidths=0.5, ax=ax)

    # 16. Salvar e retornar a figura
    fig.savefig('heatmap.png')
    return fig
