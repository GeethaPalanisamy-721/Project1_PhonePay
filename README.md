**PhonePe Data Analytics Dashboard**

This project analyzes PhonePe digital payment data (2020–2024) to generate actionable insights on transactions, users, and insurance performance across India. It combines MySQL for storage, Python for processing, and Streamlit + Plotly for interactive visualization.

**Overview**

The dashboard helps businesses and analysts understand:
	• Payment trends and user growth
	• Insurance adoption and geographical distribution
	• Top-performing regions and emerging markets
It supports use cases such as customer segmentation, fraud detection, regional benchmarking, and marketing optimization.

**Architecture**

	• Data Source: PhonePe public GitHub repository (aggregated JSON)
	• Database: MySQL relational schema with aggregated, map, and top-level tables
	• Application Layer: Streamlit app with Plotly visualizations
	• Visualization: Choropleth maps for state-wise analysis
  
**Setup**
1.Clone the repository
git clone <your-repo-link>
cd phonepe-dashboard

2.Install dependencies
pip install -r requirements.txt

3.Configure environment variables in .env
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=phonepe_db

4.Ensure India GeoJSON file is placed at /data/india_states.geojson
5.Run the app
streamlit run app.py

**Example query**
SELECT State, SUM(transaction_count) AS value
FROM transaction_agg
WHERE YEAR BETWEEN 2020 AND 2024
GROUP BY State;

**Key Insights**
	• Identification of top-performing states
	• National transaction summaries
	• Insurance adoption trends
	• User growth distribution
	• Regional digital penetration patterns
  
**Conclusion**
This project demonstrates an end-to-end data pipeline with SQL aggregation, interactive dashboards, and business-centric analytics. It highlights the practical application of data science in fintech and digital payments.
Skills Demonstrated
	• Data Modeling
	• SQL Aggregation & Optimization
	• ETL Pipeline Development
	• Data Visualization
	• Dashboard Design
	• Business-Oriented Analytics

**Author**
Geetha Palanisamy
Data Analyst | Python | SQL | Power BI | Streamlit
