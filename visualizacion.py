import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import kaleido

class DataVisualizer:
    def __init__(self, df):
        self.df = df.copy()  # Use a copy of the DataFrame to avoid modifying the original
        self.df['fecha_alta'] = pd.to_datetime(self.df['fecha_alta'])
        self.start_date = self.df['fecha_alta'].min().strftime('%Y/%m/%d')
        self.end_date = self.df['fecha_alta'].max().strftime('%Y/%m/%d')
        self.df_cleaned = self.df.dropna(subset=['recomendacion'])

        self.annotation = dict(
            x=0.1, y=1.05, showarrow=False,
            text=f'{self.start_date} - {self.end_date}',
            xref='paper', yref='paper',
            font=dict(size=12, color='black')
        )
        self.layout = dict(
            width=1000,
            height=800
        )

    def tablas(self, groupby_columns):
    # Validate if the provided columns are in the DataFrame
        invalid_columns = [col for col in groupby_columns if col not in self.df.columns]
        if invalid_columns:
            st.error(f"The following columns are not in the DataFrame: {', '.join(invalid_columns)}")
            return pd.DataFrame()  # Return an empty DataFrame on error

        # Group by the selected columns and count the occurrences
        group_df = self.df.groupby(groupby_columns).size().reset_index(name='count')

        # Create and display the table figure
        table_fig = go.Figure(data=[go.Table(
            header=dict(values=list(group_df.columns),
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[group_df[col] for col in group_df.columns],
                    fill_color='lavender',
                    align='left'))
        ])

        # Show the table in Streamlit
        st.plotly_chart(table_fig)

        # Create and display the bar plot
        bar_fig = go.Figure()

        # Add bars for each selected groupby column
        for col in groupby_columns:
            bar_fig.add_trace(go.Bar(
                x=group_df[col],
                y=group_df['count'],
                name=col,
            ))

        # Customize the layout
        for col in groupby_columns:
            bar_fig.update_layout(
                title='Bar Plot of Grouped Data',
                xaxis_title=f'{col}',
                yaxis_title='Count',
                barmode='group',
            )

        # Show the bar plot in Streamlit
        st.plotly_chart(bar_fig)

        return group_df

    def distribución_de_aseguradoras(self):
        fig = px.pie(self.df, names='aseguradora', title='Distribución de aseguradoras')
        fig.add_annotation(x=0.5, y=1.15, 
                        showarrow=False, text=f'{self.start_date} - {self.end_date}', 
                        xref='paper', yref='paper', font=dict(size=15, color='black'))
        st.plotly_chart(fig)

        fig = px.histogram(self.df, x='aseguradora', title='Distribución de aseguradoras', color='aseguradora')
        fig.add_annotation(**self.annotation)
        fig.update_layout(**self.layout)
        st.plotly_chart(fig)

    def estado_por_aseguradora(self):
        fig = px.histogram(self.df, x='estado', title='Distribución de estados por aseguradora', color='aseguradora')
        fig.add_annotation(**self.annotation)
        fig.update_layout(**self.layout)
        st.plotly_chart(fig)

        fig = px.histogram(self.df, x='aseguradora', title='Distribución de aseguradoras por estado', color='estado')
        fig.add_annotation(**self.annotation)
        fig.update_layout(**self.layout)
        st.plotly_chart(fig)

    def aseguradora_por_franja_horaria(self):
        fig = px.histogram(self.df, x='aseguradora', title='Distribución de aseguradoras por franja horaria', color='franja_horaria')
        fig.add_annotation(**self.annotation)
        fig.update_layout(**self.layout)
        st.plotly_chart(fig)

        fig = px.histogram(self.df, x='franja_horaria', title='Distribución de franjas horarias por aseguradora', color='aseguradora')
        fig.add_annotation(**self.annotation)
        fig.update_layout(**self.layout)
        st.plotly_chart(fig)

    def distribución_de_edades(self):
        fig = px.histogram(self.df, x='persona_edad', title='Distribución de edades', color='aseguradora')
        fig.add_annotation(**self.annotation)
        fig.update_layout(**self.layout)
        st.plotly_chart(fig)

        fig = px.scatter(self.df, x='persona_edad', title='Distribución de edad', color='persona_edad')
        fig.add_annotation(**self.annotation)
        fig.update_layout(**self.layout)
        st.plotly_chart(fig)

        # Aggregate the data
        age_counts = self.df['persona_edad'].value_counts().reset_index()
        age_counts.columns = ['persona_edad', 'count']

        fig = px.scatter(age_counts, x='persona_edad', y='count',
                        title='Distribución de edad',
                        color='persona_edad')
        fig.add_annotation(**self.annotation)
        fig.update_layout(**self.layout)
        st.plotly_chart(fig)

    def distribución_groupo_de_edades(self):
        fig = px.histogram(self.df, x='age_group', title='Distribución de edades por grupo', color='aseguradora')
        fig.add_annotation(**self.annotation)
        fig.update_layout(**self.layout)
        st.plotly_chart(fig)

        fig = px.histogram(self.df, x='aseguradora', title='Distribución de edades por aseguradora', color='age_group')
        fig.add_annotation(**self.annotation)
        fig.update_layout(**self.layout)
        st.plotly_chart(fig)

    def primer_contacto_por_aseguradora(self):
        fig = px.histogram(self.df, x='horas_primer_contacto', title='Distribución de horas de primer contacto por aseguradora', color='aseguradora')
        fig.add_annotation(**self.annotation)
        fig.update_layout(**self.layout)
        st.plotly_chart(fig)

        # hours_counts = self.df['horas_entre_alta_y_primer_contacto'].value_counts().reset_index()
        # hours_counts.columns = ['horas_entre_alta_y_primer_contacto', 'count']

        # fig = px.scatter(hours_counts, x='horas_entre_alta_y_primer_contacto', y='count',
        #                 title='Distribución de horas entre alta y primer contacto',
        #                 color='horas_entre_alta_y_primer_contacto')
        # fig.add_annotation(**self.annotation)
        # fig.update_layout(**self.layout)
        # st.plotly_chart(fig)

    def distribucion_de_recomendaciones_por_aseguradora(self):
        fig = px.histogram(self.df, x='recomendacion', title='Distribución de recomendaciones por aseguradora', color='aseguradora')
        fig.add_annotation(**self.annotation)
        fig.update_layout(**self.layout)
        st.plotly_chart(fig)

        fig = px.histogram(self.df, x='recomendacion', title='Distribución de recomendaciones por grupo de edad', color='age_group')
        fig.add_annotation(**self.annotation)
        fig.update_layout(**self.layout)
        st.plotly_chart(fig)

        fig = px.box(self.df, x='recomendacion', y='persona_edad', title='Distribución de recomendaciones por edad y aseguradora', color='aseguradora')
        fig.add_annotation(**self.annotation)
        fig.update_layout(**self.layout)
        st.plotly_chart(fig)

        # fig = px.box(self.df, x='recomendacion', y='persona_edad', title='Distribución de recomendaciones por edad')
        # fig.add_annotation(**self.annotation)
        # fig.update_layout(**self.layout)
        # st.plotly_chart(fig)

    def recomendacion_sunburst(self):
        fig = px.sunburst(self.df_cleaned, path=['aseguradora', 'recomendacion', 'age_group', 'persona_genero'], title='Distribución de recomendaciones por aseguradora, edad y género')
        fig.add_annotation(**self.annotation)
        fig.update_layout(**self.layout)
        st.plotly_chart(fig)


