import sys
import pandas as pd
import plotly.express as px


def main(csv_file_path):
    pd.options.plotting.backend = "plotly"
    df = pd.read_csv(csv_file_path)

    #create new dataframe for graph  
    chat_log_count = df.groupby('conversation_id').size().reset_index(name='log_count')
    graph_df = df[['conversation_id', 'created_at', 'title']].drop_duplicates().merge(chat_log_count, on='conversation_id')

    #create histogram
    x = graph_df['created_at']
    y = graph_df['log_count']

    df = px.data.tips()
    fig = px.histogram(graph_df, x=x, y=y, color="title", marginal="rug", hover_data=graph_df.columns)

    fig.write_html('chatgpt_chat_graph.html')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python draw_graph.py </path/to/chatgpt_parsed_chat_log.csv>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
    