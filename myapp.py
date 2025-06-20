# Import libraries
import pandas as pd 
import plotly.express as px
import streamlit as st   

st.set_page_config(
    page_title='Mahabir Singh Analytics Portal',
    page_icon='📊'
)

# Title
st.title(':rainbow[Data Analytics Portal]')
st.subheader(':gray[Explore Data with ease.]', divider='rainbow')

# File uploader
file = st.file_uploader('Drop CSV or Excel file', type=['csv', 'xlsx'])
if file:
    if file.name.endswith('csv'):
        data = pd.read_csv(file)
    else:
        data = pd.read_excel(file)

    st.dataframe(data)
    st.info('File successfully uploaded!', icon='🚨')

    # Basic Information Section
    st.subheader(':rainbow[Basic Information of the Dataset]', divider='rainbow')
    tab1, tab2, tab3, tab4 = st.tabs(['Summary', 'Top and Bottom Rows', 'Data Types', 'Columns'])

    with tab1:
        st.write(f'There are {data.shape[0]} rows and {data.shape[1]} columns in the dataset')
        st.subheader(':gray[Statistical Summary]')
        st.dataframe(data.describe())

    with tab2:
        st.subheader(':gray[Top Rows]')
        toprows = st.slider('Number of rows to display', 1, data.shape[0], key='topslider')
        st.dataframe(data.head(toprows))

        st.subheader(':gray[Bottom Rows]')
        bottomrows = st.slider('Number of rows to display', 1, data.shape[0], key='bottomslider')
        st.dataframe(data.tail(bottomrows))

    with tab3:
        st.subheader(':gray[Data Types of Columns]')
        st.dataframe(data.dtypes)

    with tab4:
        st.subheader('Column Names in Dataset')
        st.write(list(data.columns))

    # Column Value Count Section
    st.subheader(':rainbow[Column Values to Count]', divider='rainbow')
    with st.expander('Value Count'):
        col1, col2 = st.columns(2)
        with col1:
            column = st.selectbox('Choose column', options=list(data.columns))
        with col2:
            toprows = st.number_input('Top rows', min_value=1, step=1)

        if st.button('Count'):
            result = data[column].value_counts().reset_index().head(toprows)
            result.columns = [column, 'count']
            st.dataframe(result)

            # Visualization
            st.subheader('Visualization', divider='gray')

            # 📌 Adding "Learn More" links for each chart type
            fig1 = px.bar(result, x=column, y='count', text='count', template='plotly_white')
            st.plotly_chart(fig1)
            st.markdown('[📖 Learn about Bar Charts](https://www.geeksforgeeks.org/bar-graphs/)')

            fig2 = px.line(result, x=column, y='count', text='count', template='plotly_white')
            st.plotly_chart(fig2)
            st.markdown('[📖 Learn about Line Charts](https://www.geeksforgeeks.org/line-chart-in-matplotlib-python/)')

            fig3 = px.pie(result, names=column, values='count')
            st.plotly_chart(fig3)
            st.markdown('[📖 Learn about Pie Charts](https://www.geeksforgeeks.org/pie-charts/)')

    # GroupBy Section
    st.subheader(':rainbow[Groupby: Simplify Your Data Analysis]', divider='rainbow')
    st.write('Summarize data by specific categories and groups')

    with st.expander('Group By your columns'):
        col1, col2, col3 = st.columns(3)
        with col1:
            groupby_cols = st.multiselect('Choose columns to group by', options=list(data.columns))
        with col2:
            operation_col = st.selectbox('Choose column for operation', options=list(data.columns))
        with col3:
            operation = st.selectbox('Choose operation', options=['sum', 'max', 'min', 'mean', 'median', 'count'])

        if groupby_cols:
            # Check if selected column is numeric
            if data[operation_col].dtype in ['int64', 'float64']:
                result = data.groupby(groupby_cols).agg(
                    newcol=(operation_col, operation)
                ).reset_index()

                st.dataframe(result)

                # Data Visualization
                st.subheader(':gray[Data Visualization]', divider='gray')
                graphs = st.selectbox('Choose graph type', options=['line', 'bar', 'scatter', 'pie', 'sunburst'])

                if graphs == 'line':
                    x_axis = st.selectbox('Choose X axis', options=list(result.columns))
                    y_axis = st.selectbox('Choose Y axis', options=list(result.columns))
                    color = st.selectbox('Color Information', options=[None] + list(result.columns))
                    fig = px.line(result, x=x_axis, y=y_axis, color=color, markers='o')
                    st.plotly_chart(fig)
                    st.markdown('[📖 Learn about Line Charts](https://www.geeksforgeeks.org/line-chart-in-matplotlib-python/)')

                elif graphs == 'bar':
                    x_axis = st.selectbox('Choose X axis', options=list(result.columns))
                    y_axis = st.selectbox('Choose Y axis', options=list(result.columns))
                    color = st.selectbox('Color Information', options=[None] + list(result.columns))
                    facet_col = st.selectbox('Column Information', options=[None] + list(result.columns))
                    fig = px.bar(result, x=x_axis, y=y_axis, color=color, facet_col=facet_col, barmode='group')
                    st.plotly_chart(fig)
                    st.markdown('[📖 Learn about Bar Charts](https://www.geeksforgeeks.org/bar-graphs/)')

                elif graphs == 'scatter':
                    x_axis = st.selectbox('Choose X axis', options=list(result.columns))
                    y_axis = st.selectbox('Choose Y axis', options=list(result.columns))
                    color = st.selectbox('Color Information', options=[None] + list(result.columns))
                    size = st.selectbox('Size Column', options=[None] + list(result.columns))
                    fig = px.scatter(result, x=x_axis, y=y_axis, color=color, size=size)
                    st.plotly_chart(fig)
                    st.markdown('[📖 Learn about Scatter Plots](https://www.geeksforgeeks.org/scatter-plot/)')

                elif graphs == 'pie':
                    values = st.selectbox('Choose numerical values', options=list(result.columns))
                    names = st.selectbox('Choose labels', options=list(result.columns))
                    fig = px.pie(result, values=values, names=names)
                    st.plotly_chart(fig)
                    st.markdown('[📖 Learn about Pie Charts](https://www.geeksforgeeks.org/pie-charts/)')

                elif graphs == 'sunburst':
                    path = st.multiselect('Choose path', options=list(result.columns))
                    fig = px.sunburst(result, path=path, values='newcol')
                    st.plotly_chart(fig)
                    st.markdown('[📖 Learn about Sunburst Charts](https://www.edrawmind.com/article/sunburst-chart-template.html)')

            else:
                st.warning(f"⚠️ The selected column '{operation_col}' is not numeric. '{operation}' operation cannot be applied.", icon="⚠️")
