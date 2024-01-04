import streamlit as st

conn = st.connection('flyio', type='sql')

st.write('# Smit database on fly.io')

df = conn.query('SELECT * FROM auth;', ttl="10m")
st.write(df)

# with conn.session as session:
#     session.execute()
#     session.commit()