import pandas as pd
import numpy as np

# Create dummy data for facebook_campaigns.csv
fb_data = {
    'date': pd.to_datetime(pd.date_range(start='2023-01-01', periods=10, freq='D')),
    'campaign_name': [f'FB_Campaign_{i}' for i in range(10)],
    'impressions': np.random.randint(1000, 10000, 10),
    'clicks': np.random.randint(50, 500, 10),
    'conversions': np.random.randint(5, 50, 10),
    'spend': np.random.uniform(100, 1000, 10).round(2)
}
fb_df = pd.DataFrame(fb_data)
fb_df.to_csv('/facebook_campaigns.csv', index=False)

# Create dummy data for instagram_campaigns.csv
ig_data = {
    'date': pd.to_datetime(pd.date_range(start='2023-01-01', periods=10, freq='D')),
    'campaign_name': [f'IG_Campaign_{i}' for i in range(10)],
    'impressions': np.random.randint(800, 8000, 10),
    'clicks': np.random.randint(40, 400, 10),
    'conversions': np.random.randint(4, 40, 10),
    'spend': np.random.uniform(80, 800, 10).round(2)
}
ig_df = pd.DataFrame(ig_data)
ig_df.to_csv('/instagram_campaigns.csv', index=False)

# Create dummy data for sfmc_email_campaigns.csv
sfmc_data = {
    'date': pd.to_datetime(pd.date_range(start='2023-01-01', periods=10, freq='D')),
    'campaign_name': [f'SFMC_Campaign_{i}' for i in range(10)],
    'emails_sent': np.random.randint(5000, 20000, 10),
    'opens': np.random.randint(1000, 8000, 10),
    'clicks': np.random.randint(100, 2000, 10),
    'conversions': np.random.randint(10, 100, 10) # Added conversions column
}
sfmc_df = pd.DataFrame(sfmc_data)
sfmc_df.to_csv('/sfmc_email_campaigns.csv', index=False)

print("Dummy CSV files created: facebook_campaigns.csv, instagram_campaigns.csv, sfmc_email_campaigns.csv")
