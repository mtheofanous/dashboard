import streamlit as st
import pandas as pd
import plotly.io as pio
from io import StringIO
from visualizacion_1 import DataVisualizer  # Adjust the import based on your file structure

# Ensure kaleido is installed
import kaleido

def load_data():
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)

            # Convert relevant columns to datetime
            df['fecha_alta'] = pd.to_datetime(df['fecha_alta'], errors='coerce')
            df['fecha_primer_contacto'] = pd.to_datetime(df['fecha_primer_contacto'], errors='coerce')
            df['fecha_ultimo_estado'] = pd.to_datetime(df['fecha_ultimo_estado'], errors='coerce')
            df['mes_alta'] = df['fecha_alta'].dt.month_name()
            df['dia_semana_alta'] = df['fecha_alta'].dt.day_name()
            df['hora_alta'] = df['fecha_alta'].dt.hour
            df['mes_contacto'] = df['fecha_primer_contacto'].dt.month_name()
            df['dia_semana_contacto'] = df['fecha_primer_contacto'].dt.day_name()
            df['hora_contacto'] = df['fecha_primer_contacto'].dt.hour
            df['mes_ultimo_estado'] = df['fecha_ultimo_estado'].dt.month_name()
            df['dia_semana_ultimo_estado'] = df['fecha_ultimo_estado'].dt.day_name()
            df['hora_ultimo_estado'] = df['fecha_ultimo_estado'].dt.hour
            df['age_group'] = ['Menor de edad' if age < 18 else 'Adulto hasta 59' if age < 60 else '60+' for age in df['persona_edad']]
            return df
        except Exception as e:
            st.error(f"Error reading the file: {e}")
            return pd.DataFrame()
    else:
        st.warning("Please upload a CSV file.")
        return pd.DataFrame()

def to_csv(df):
    """Convert DataFrame to CSV."""
    return df.to_csv(index=False).encode('utf-8')

def export_plot_as_png(fig):
    """Converts Plotly figure to PNG and returns the binary data."""
    if fig:
        img_bytes = pio.to_image(fig, format="png")
        return img_bytes
    return None

def main():
    st.title('Data Visualization Dashboard')

    # Load data
    df = load_data()
    
    if not df.empty:
        # Create an instance of the DataVisualizer class
        visualizer = DataVisualizer(df)

        # Sidebar for user input
        st.sidebar.title('Select Visualization')
        options = [
            'Tablas', 
            'Distribución de aseguradoras', 
            'Estado por aseguradora', 
            'Aseguradora por franja horaria',
            'Distribución de edades', 
            'Distribución de grupos de edades',
            'Primer contacto por aseguradora', 
            'Distribución de recomendaciones por aseguradora',
            'Recomendación Sunburst'
        ]
        choice = st.sidebar.selectbox('Select an option', options)

        placeholder = st.empty()

        with placeholder.container():
            

            # Display selected visualization
            if choice == 'Tablas':
                all_columns = ['aseguradora', 'estado', 'persona_genero', 'franja_horaria','estado_primer_movimiento', 'recomendacion', 'dia_semana_contacto', 'dia_semana_ultimo_estado', 'age_group']# df.columns.tolist() # Get columns ['aseguradora', 'estado', 'franja_horaria',
                #'fecha_ultimo_estado', 'mes_alta', 'dia_semana_alta', 'hora_alta', 'mes_contacto',]
                groupby_columns = st.multiselect('Select columns to group by', options=all_columns, default=['aseguradora','recomendacion'])
                if st.button('Show Table'):
                    if groupby_columns:
                        result_df = visualizer.tablas(groupby_columns)
                        
                        # Display the table
                        st.dataframe(result_df)
                        
                        # Add download button
                        # csv = to_csv(result_df, index=False, encoding = 'utf-8')
                        csv = result_df.to_csv(index=False).encode('utf-8-sig')
                        st.download_button(
                            label="Download Table as CSV",
                            data=csv,
                            file_name=f'table_{groupby_columns}.csv',
                            mime='text/csv'
                        )
                    else:
                        st.error('Please select at least one column to group by.')
            
            elif choice == 'Distribución de aseguradoras':
                fig = visualizer.distribución_de_aseguradoras()
                if fig:
                    st.plotly_chart(fig)

            elif choice == 'Estado por aseguradora':
                fig = visualizer.estado_por_aseguradora()
                if fig:
                    st.plotly_chart(fig)
            
            elif choice == 'Aseguradora por franja horaria':
                fig = visualizer.aseguradora_por_franja_horaria()
                if fig:
                    st.plotly_chart(fig)
            
            elif choice == 'Distribución de edades':
                fig = visualizer.distribución_de_edades()
                if fig:
                    st.plotly_chart(fig)
            
            elif choice == 'Distribución de grupos de edades':
                fig = visualizer.distribución_groupo_de_edades()
                if fig:
                    st.plotly_chart(fig)
            
            elif choice == 'Primer contacto por aseguradora':
                fig = visualizer.primer_contacto_por_aseguradora()
                if fig:
                    st.plotly_chart(fig)
            
            elif choice == 'Distribución de recomendaciones por aseguradora':
                fig = visualizer.distribucion_de_recomendaciones_por_aseguradora()
                if fig:
                    st.plotly_chart(fig)
            
            elif choice == 'Recomendación Sunburst':
                fig = visualizer.recomendacion_sunburst()
                if fig:
                    st.plotly_chart(fig)

# Run the app
if __name__ == '__main__':
    main()
