
import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Airbnb Data Analysis",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏠 Airbnb Analysis")
st.markdown("---")




@st.cache_data
def load_data():
    df = pd.read_csv('Airbnb_Cleaned.csv')
    return df

df = load_data()

# -----------------------
# Sidebar navigation
# -----------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Data Overview",
        "Data Visualization Playground",
        "Correlation Heatmap",
        'Analysis Questions'
        
    ]
)

# -----------------------
# Sidebar Filters
# -----------------------
st.sidebar.markdown("---")
st.sidebar.title("Filters")

# Room Type Filter
room_types = df['room_type'].unique().tolist()
selected_room_types = st.sidebar.multiselect(
    "Select Room Types",
    room_types,
    default=room_types
)

# Neighbourhood Filter
neighbourhoods = df['neighbourhood_group'].unique().tolist()
selected_neighbourhoods = st.sidebar.multiselect(
    "Select Neighbourhoods",
    neighbourhoods,
    default=neighbourhoods
)

df_filtered = df[
    (df['room_type'].isin(selected_room_types)) &
    (df['neighbourhood_group'].isin(selected_neighbourhoods))
]

    

# ==================================================
# PAGE 1: DATA OVERVIEW
# ==================================================
if page == "Data Overview":
    
    st.header("📊 Dataset Overview")
    st.write("""
    This analysis explores Airbnb listings data in order to understand pricing patterns, demand drivers, 
    and market segmentation across different neighborhoods and room types, located in the USA.
    """)


    # Displaying basic statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Listings", f"{len(df_filtered):,}")
    with col2:
        st.metric("Avg Price", f"${df_filtered['price'].mean():.2f}")
    with col3:
        st.metric("Neighborhoods", df_filtered['neighbourhood_group'].nunique())
    with col4:
        st.metric("Room Types", df_filtered['room_type'].nunique())

    st.markdown("---")


    # Displaying the dataset
    st.header("👀 Airbnb Data")
    st.dataframe(df_filtered, use_container_width=True)
    

    # Key Insights
    st.header("🔑 Key Insights")
    insights = f"""
    - **Average Price:** ${df_filtered['price'].mean():.2f} per night
    - **Price Range:** ${df_filtered['price'].min():.0f} - ${df_filtered['price'].max():.0f}
    - **Most Common Room Type:** {df_filtered['room_type'].mode()[0] if len(df_filtered) > 0 else 'N/A'}
    - **Most Popular Neighborhood:** {df_filtered['neighbourhood_group'].mode()[0] if len(df_filtered) > 0 else 'N/A'}
    - **Average Reviews per Month:** {df_filtered['reviews_per_month'].mean():.2f}
    """
    st.info(insights)
    
    st.markdown("---")
    
    
    # Data Dictionary
    st.header("📚 Data Dictionary")
    st.write("Description of all columns in the dataset:")

    column_descriptions = {
        'id': 'Unique identifier for each listing',
        'neighbourhood_group': 'Main neighborhood where the listing is located (e.g., Manhattan, Brooklyn)',
        'room_type': 'Type of room: Entire home/apt, Private room, Shared room, Hotel room',
        'price': 'Price per night in USD',
        'minimum_nights': 'Minimum number of nights required for booking',
        'number_of_reviews': 'Total count of reviews received by the listing',
        'last_review_date': 'Date of the most recent review',
        'reviews_per_month': 'Average number of reviews per month (demand proxy)',
        'calculated_host_listings_count': 'Total number of listings owned by this host',
        'availability_365': 'Number of days available in the next 365 days',
        'host_identity_verified': 'Whether the host identity has been verified (Yes/No)',
        'cancellation_policy': 'Type of cancellation policy (Flexible, Moderate, Strict, etc.)',
        'construction_year': 'Year the building was constructed',
        'service_fee': 'Airbnb service fee per booking in USD',
        'review_rate_number': 'Average rating score (0-5 scale)',
        'instant_bookable': 'Whether the listing can be instantly booked (Yes/No)',
        'review_bracket': 'Review count categorized into brackets',
        'review_permonth_bracket': 'Reviews per month categorized into brackets',
        'host_type': 'Type of host (Individual, Company, etc.)',
        'price_range': 'Price categorized into ranges',
        'reviews_bin': 'Review count binned into ranges',
        'price_bin': 'Price binned into ranges',
        'service_fee_bins': 'Service fee binned into ranges',
        'year': 'Year of the last review'
    }

    # Displaying columns in organized tabs
    col_names = df_filtered.columns.tolist()

    st.subheader("📋 Column Details")
    for col in col_names:
        with st.expander(f"**{col}**"):
            desc = column_descriptions.get(col, "No description available")
            dtype = str(df_filtered[col].dtype)
            non_null = df_filtered[col].notna().sum()
            null_count = df_filtered[col].isna().sum()
            
            st.write(f"**Description:** {desc}")
            st.write(f"**Data Type:** `{dtype}`")
            st.write(f"**Non-null Count:** {non_null:,}")
            st.write(f"**Null Count:** {null_count}")
            
            if dtype in ['int64', 'float64']:
                st.write(f"**Min:** {df_filtered[col].min()}")
                st.write(f"**Max:** {df_filtered[col].max()}")
                st.write(f"**Mean:** {df_filtered[col].mean():.2f}")
            else:
                st.write(f"**Unique Values:** {df_filtered[col].nunique()}")
                if df_filtered[col].nunique() <= 10:
                    st.write(f"**Values:** {', '.join(df_filtered[col].unique().astype(str))}")

    st.markdown("---")

    

    
# ==================================================
# PAGE 2: Data Visualization Playground
# ==================================================
if page == "Data Visualization Playground":
    st.subheader("📊 Data Visualization Playground")

    st.write(
        "Explore relationships in the cleaned dataset with univariate or bivariate plots."
    )

    # Separate numeric and categorical columns
    numeric_cols = df_filtered.select_dtypes(include=["int64", "float64"]).columns.tolist().copy()
    if 'id' in numeric_cols:
        numeric_cols.remove('id')
    categorical_cols = df_filtered.select_dtypes(include=["object", "category"]).columns.tolist()

    if len(numeric_cols) + len(categorical_cols) < 1:
        st.warning("No columns available for plotting.")
    else:
        # Plot type selector
        plot_type = st.radio(
            "Select plot type",
            ["Univariate", "Bivariate"],
            horizontal=True
        )

        if plot_type == "Univariate":
            col = st.selectbox(
                "Select a column",
                numeric_cols + categorical_cols
            )

            if col in numeric_cols:
                fig = px.scatter(
                    df_filtered,
                    y=col,
                    title=f"Univariate Scatter Plot: {col}"
                )
            if col in categorical_cols:
                counts = df_filtered[col].value_counts().reset_index()
                counts.columns = [col, "count"]  

                fig = px.bar(
                    counts,
                    x=col,
                    y="count",
                    title=f"Univariate Bar Plot: {col}"
                    
                )


            st.plotly_chart(fig, use_container_width=True)

        else:  # Bivariate
            x_col = st.selectbox(
                "Select X-axis column",
                numeric_cols + categorical_cols
            )
            y_col = st.selectbox(
                "Select Y-axis column",
                numeric_cols + categorical_cols
            )

            # Numeric vs Numeric → scatter
            if x_col in numeric_cols and y_col in numeric_cols:
                fig = px.scatter(
                    df_filtered,
                    x=x_col,
                    y=y_col,
                    title=f"{y_col} vs {x_col}"
                )

            # Categorical vs Numeric → bar
            elif x_col in categorical_cols and y_col in numeric_cols:
                grouped = df_filtered.groupby(x_col)[y_col].mean().reset_index()
                fig = px.bar(
                    grouped,
                    x=x_col,
                    y=y_col,
                    title=f"Average {y_col} by {x_col}",
                    text_auto='.3s'
                )

            elif x_col in numeric_cols and y_col in categorical_cols:
                grouped = df_filtered.groupby(y_col)[x_col].mean().reset_index()
                fig = px.bar(
                    grouped,
                    x=y_col,
                    y=x_col,
                    title=f"Average {x_col} by {y_col}",
                    text_auto='.3s'
                )


            # Categorical vs Categorical → grouped bar
            elif x_col in categorical_cols and y_col in categorical_cols:
                fig = px.histogram(
                    df_filtered,
                    x=x_col,
                    color=y_col,
                    barmode="group",
                    title=f"{x_col} vs {y_col}"
                )

            st.plotly_chart(fig, use_container_width=True)
            
            
            
# ==================================================
# PAGE 3: CORRELATION HEATMAP
# ==================================================

elif page == "Correlation Heatmap":

    st.subheader("🔗 Correlation Heatmap")
    
    st.write("""
    This correlation heatmap shows the pairwise correlations between numeric features in the dataset.
    Correlation values range from -1 to 1, where:
- **1** indicates a perfect positive correlation (as one variable increases, the other also increases).
- **-1** indicates a perfect negative correlation (as one variable increases, the other decreases).
- **0** indicates no correlation (the variables do not have a linear relationship).
    """)
    
    corr= df_filtered.corr(numeric_only=True).round(2).drop(['id'], axis=1).drop(['id'], axis=0)

    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu",
        title="Correlation Heatmap",
        width=800, height=800
    )

    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# PAGE 4: Analysis Questions
# ==================================================

elif page == "Analysis Questions":
    st.subheader("❓ Analysis Questions & Charts")

    # Q1
    st.markdown("#### 1) What is the relation between listing price and factors like : service fee, room type, location, reviews, host size, etc..?")
    st.write("""- The strong linear relationship between price and service fee indicates that service fee is mostly caclulated as a percentage from price. 
                While the points surrounding the straight line suggests some hosts use other methods like a fixed figure to set the service fee amount.""") 
    fig_price_service = px.scatter(df_filtered, x='price', y='service_fee', labels={'price': 'Price ($)', 'service_fee': 'Service Fee ($)'}, title='Price vs Service Fee')
    st.plotly_chart(fig_price_service, use_container_width=True)
    st.write("""- Airbnb market is dominated by small hosts.""")
    st.write("""- A minority of hosts control many listings.""") 
    st.write("""- Professional hosts exist across all price levels.""")
    st.write("""- Price is independent of host size.""")
    fig_price_host = px.scatter(df_filtered, x='price', y='calculated_host_listings_count', labels={'calculated_host_listings_count': 'Listings per Host'}, title='Price vs Host Listings Count')
    st.plotly_chart(fig_price_host, use_container_width=True)
    
    # Q2
    st.markdown("#### 2) What is the distribution of room types by neighbourhood?")
    st.write("""- Manhattan and Brooklyn dominate the market, with the highest number of listings, especially entire homes and private rooms.""")
    st.write("""- Queens has moderate supply, while Staten Island and the Bronx contribute only a small share of total listings across all room types.""")    
    fig_room_neigh = px.histogram(df_filtered, x='neighbourhood_group', color='room_type', title='Listings by Neighbourhood Group and Room Type', labels={'neighbourhood_group': 'Neighbourhood', 'room_type': 'Room Type'})
    st.plotly_chart(fig_room_neigh, use_container_width=True)

    # Q3
    st.markdown("#### 3) What is the average price per neighbhourhood?")
    st.write("""- The average prices are nearly identical across all neighbourhood groups, indicating minimal price variation by neighbourhood.""")
    neighborhood_price = df_filtered.groupby('neighbourhood_group')['price'].mean().round(2).sort_values(ascending=False).reset_index()
    fig_nb = px.bar(neighborhood_price, x='neighbourhood_group', y='price', title='Average Price by Neighbourhood Group', text_auto='.3s', labels={'price': 'Price', 'neighbourhood_group': 'Neighbourhood'}, color='neighbourhood_group')
    st.plotly_chart(fig_nb, use_container_width=True)

    # Q4
    st.markdown("#### 4) What is the average price per room type?")
    st.write("""- Average prices are relatively similar across room types, with hotel rooms slightly higher, indicating limited price differentiation by accommodation category.""")
    room_price = df_filtered.groupby('room_type')['price'].mean().round(2).sort_values(ascending=False).reset_index()
    fig_room = px.bar(room_price, x='room_type', y='price', title='Average Price by Room Type', text_auto='.3s', labels={'price': 'Price', 'room_type': 'Room Type'}, color='room_type')
    st.plotly_chart(fig_room, use_container_width=True)

    # Q5
    st.markdown("#### 5) What is the average minimum nights for each type of listing (aka room type) in each neighbourhood?")
    st.write("""- Entire homes/apartments generally require longer minimum stays, especially in Manhattan, indicating a focus on longer bookings.""")
    st.write("""- Hotel and shared rooms tend to have shorter minimum night requirements, making them more flexible for short-term stays.""")
    room_nights = df_filtered.groupby(['room_type','neighbourhood_group'])['minimum_nights'].mean().round(2).reset_index()
    fig_nights = px.bar(room_nights, x='neighbourhood_group', y='minimum_nights', color='room_type', barmode='group', title='Average Minimum Nights by Neighbourhood Group & Room Type', labels={'minimum_nights': 'Minimum Nights', 'neighbourhood_group': 'Neighbourhood', 'room_type' : 'Room Type'})
    st.plotly_chart(fig_nights, use_container_width=True)

    # Q6
    st.markdown("#### 6) What is the average rating for each type of listing (aka room type) in each neighbourhood?")
    st.write("""- Average ratings are fairly consistent across all neighbourhoods and room types, generally ranging between 3.2 and 3.9.""")
    st.write("""- Hotel rooms and private rooms tend to receive slightly higher ratings compared to entire homes and shared rooms in most neighbourhoods.""")
    if 'review_rate_number' in df_filtered.columns:
        room_rating = df_filtered.groupby(['room_type','neighbourhood_group'])['review_rate_number'].mean().round(2).reset_index()
        fig_rating = px.bar(room_rating, x='neighbourhood_group', y='review_rate_number', color='room_type', barmode='group', title='Average Review Rate Number by Neighbourhood Group & Room Type', labels={'review_rate_number': 'Rating Number', 'neighbourhood_group': 'Neighbourhood', 'room_type' : 'Room Type'})
        st.plotly_chart(fig_rating, use_container_width=True)

    # Q7
    st.markdown("#### 7) What is the trend of Price by Last Review Year and Neighbourhood Group?")
    st.write("""- After some early fluctuations, average prices across all neighbourhoods remain relatively stable from 2017 onward.""")
    if 'year' in df_filtered.columns:
        price_trend = df_filtered[df_filtered['year'] != 2000].groupby(['year','neighbourhood_group'])['price'].mean().reset_index().round(2)
        fig_trend = px.line(price_trend, x='year', y='price', color='neighbourhood_group', markers=True, title='Trend of Price by Last Review Year and Neighbourhood')
        st.plotly_chart(fig_trend, use_container_width=True)

    # Q8
    st.markdown("#### 8) What is the average price per Neighbhorhood per Room Type?")
    st.write("""- Average prices are fairly consistent across neighbourhoods for most room types, though hotel rooms show greater variation compared to other accommodation categories.""")  
    plot_price = df_filtered.groupby(['neighbourhood_group','room_type'])['price'].mean().round(2).reset_index()
    fig_price_by_room = px.bar(plot_price, x='neighbourhood_group', y='price', color='room_type', barmode='group', title='Average Price per Neighborhood per Room Type', labels={'neighbourhood_group': 'Neighborhood Group', 'price': 'Price', 'room_type': 'Room Type'})
    st.plotly_chart(fig_price_by_room, use_container_width=True)

    # Q9
    st.markdown("#### 9) What is the average Number of Reviews per Neighbhorhood per Room Type?")
    st.write("""- Manhattan shows the highest average number of reviews, particularly for hotel rooms, indicating stronger guest activity and demand.""")
    st.write("""- Staten Island and the Bronx have noticeably fewer reviews across most room types, suggesting lower overall booking volume.""")
    plot_review = df_filtered.groupby(['neighbourhood_group','room_type'])['number_of_reviews'].mean().round(2).reset_index()
    fig_reviews_by_room = px.bar(plot_review, x='neighbourhood_group', y='number_of_reviews', color='room_type', barmode='group', title='Average number of reviews per Neighborhood per Room Type', labels={'neighbourhood_group': 'Neighborhood Group', 'number_of_reviews': 'number of reviews', 'room_type': 'Room Type'})
    st.plotly_chart(fig_reviews_by_room, use_container_width=True)

    # Q10
    st.markdown("#### 10) What is the average price by cancellation policy and instant bookable status?")
    st.write("""- Listings with strict cancellation policies tend to have slightly higher average prices compared to flexible and moderate policies.""")
    st.write("""- Instant bookable status shows minimal impact on price, as average prices remain relatively similar across True and False categories.""")
    if 'cancellation_policy' in df_filtered.columns and 'instant_bookable' in df_filtered.columns:
        agg = df_filtered[df_filtered['instant_bookable'].notna() & df_filtered['cancellation_policy'].notna()].groupby(['cancellation_policy','instant_bookable'])['price'].mean().reset_index()
        fig_policy = px.bar(agg, x='cancellation_policy', y='price', color='instant_bookable', barmode='group', title='Average Price by Cancellation Policy & Instant Bookable', text_auto='.3s', labels={'price': 'Price', 'cancellation_policy': 'Cancellation Policy', 'instant_bookable': 'Instant Bookable'})
        st.plotly_chart(fig_policy, use_container_width=True)

    # Q11
    st.markdown("#### 11) Which locations have the strongest demand?")
    st.write("""- Queens shows the highest average reviews per month, indicating relatively stronger booking activity.""")
    st.write("""- Brooklyn and Manhattan have slightly lower averages, suggesting demand is more evenly distributed rather than heavily concentrated.""")
    location_demand = df_filtered.groupby('neighbourhood_group').agg({'reviews_per_month':'mean','number_of_reviews':'mean','availability_365':'mean','price':'mean','id':'count'}).rename(columns={'id':'listing_count'})
    location_demand = location_demand.round(2).reset_index()
    fig_demand = px.bar(location_demand, x='neighbourhood_group', y='reviews_per_month', title='Average Reviews per Month by Neighbourhood', labels={'reviews_per_month': 'Avg Reviews per Month', 'neighbourhood_group': 'Neighbourhood'}, color='neighbourhood_group')
    st.plotly_chart(fig_demand, use_container_width=True)

    st.markdown("---")
