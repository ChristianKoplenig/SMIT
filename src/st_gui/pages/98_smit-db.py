import streamlit as st

conn = st.connection('flyio', type='sql')

with conn.session as session:
    session.execute()
    session.commit()
#df = conn.query('SELECT * FROM someuser;', ttl="10m")

st.write('# Smit database on fly.io')
# # Print results.
# for row in df.itertuples():
#     st.write(f"{row.username}")