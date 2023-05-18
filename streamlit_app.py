import streamlit as st
import sqlite3
import pandas as pd

# Verbindung zur SQLite-Datenbank herstellen
conn1 = sqlite3.connect('counter_data.db')
c1 = conn1.cursor()


# Tabelle erstellen, falls sie noch nicht existiert
c1.execute('''
CREATE TABLE IF NOT EXISTS counter_data (
    id INTEGER PRIMARY KEY,
    pils_count INTEGER,
    lemon_count INTEGER,
    curuba_count INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')
conn1.commit()
c1.execute('''
CREATE TABLE IF NOT EXISTS counter_total (
    id INTEGER PRIMARY KEY,
    pils_total INTEGER,
    lemon_total INTEGER,
    curuba_total INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')
conn1.commit()


# Zentriere und vergrößere die Überschrift
st.markdown("<h1 style='text-align: center; font-size: 40px;'>Preorder-Counter</h1>", unsafe_allow_html=True)

st.write("\n")
st.write("\n")

# Initialisiere die Zähler und Deltas für die verschiedenen Getränke
if 'pils_count' not in st.session_state:
    st.session_state.pils_count = 0
    st.session_state.pils_delta = 0

if 'lemon_count' not in st.session_state:
    st.session_state.lemon_count = 0
    st.session_state.lemon_delta = 0

if 'curuba_count' not in st.session_state:
    st.session_state.curuba_count = 0
    st.session_state.curuba_delta = 0



col1, col2, col3 = st.columns(3)

# Pils
with col1:
    if st.button('Pils +1', type='primary'):
        st.session_state.pils_count += 1
        st.session_state.pils_delta = 1
    if st.button('Pils -1', type='secondary') and st.session_state.pils_count > 0:
        st.session_state.pils_count -= 1
        st.session_state.pils_delta = -1
    st.metric(label="Pils", value=st.session_state.pils_count, delta=st.session_state.pils_delta)

# V+ Lemon
with col2:
    if st.button('V+ Lemon +1', type='primary'):
        st.session_state.lemon_count += 1
        st.session_state.lemon_delta = 1
    if st.button('V+ Lemon -1', type='secondary') and st.session_state.lemon_count > 0:
        st.session_state.lemon_count -= 1
        st.session_state.lemon_delta = -1
    st.metric(label="V+ Lemon", value=st.session_state.lemon_count, delta=st.session_state.lemon_delta)

# V+ Curuba
with col3:
    if st.button('V+ Curuba +1', type='primary'):
        st.session_state.curuba_count += 1
        st.session_state.curuba_delta = 1
    if st.button('V+ Curuba -1', type='secondary') and st.session_state.curuba_count > 0:
        st.session_state.curuba_count -= 1
        st.session_state.curuba_delta = -1
    st.metric(label="V+ Curuba", value=st.session_state.curuba_count, delta=st.session_state.curuba_delta)


st.write("\n")

with st.container():
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button('Speichern und zurücksetzen'):
            # Werte in der Datenbank speichern
            c1.execute('INSERT INTO counter_data (pils_count, lemon_count, curuba_count) VALUES (?, ?, ?)', (st.session_state.pils_count, st.session_state.lemon_count, st.session_state.curuba_count))
            conn1.commit()

            # Counter und Delta zurücksetzen
            st.session_state.pils_count = 0
            st.session_state.lemon_count = 0
            st.session_state.curuba_count = 0
            st.session_state.pils_delta = 0
            st.session_state.lemon_delta = 0
            st.session_state.curuba_delta = 0


# Daten aus der Datenbank abrufen und in einen DataFrame konvertieren
c1.execute("SELECT pils_count, lemon_count, curuba_count, timestamp FROM counter_data")
data = c1.fetchall()
columns = ["Pils", "V+ Lemon", "V+ Curuba", "Timestamp"]
df = pd.DataFrame(data, columns=columns)

# Erste Spalte entfernen (Index)
df = df.set_index('Timestamp')

# Reihenfolge der Zeilen umkehren
df_reversed = df[::-1]

# DataFrame anzeigen
st.dataframe(df_reversed)

# Mit Summenfunktion die Spalten zusammenaddieren
if st.button('Zusammenfassen'):
    c1.execute("SELECT SUM(pils_count), SUM(lemon_count), SUM(curuba_count) FROM counter_data")
    result = c1.fetchone()
    pils_sum = result[0]
    lemon_sum = result [1]
    curuba_sum = result [2]
    #Werte in die Datenbank einfügen
    c1.execute('INSERT INTO counter_total (pils_total, lemon_total, curuba_total) VALUES (?, ?, ?)', (pils_sum, lemon_sum, curuba_sum))
    conn1.commit()

c1.execute("SELECT pils_total, lemon_total, curuba_total, timestamp FROM counter_total")
data_total = c1.fetchall()
columns_total = ["Pils", "V+ Lemon", "V+ Curuba", "Timestamp"]
df_total = pd.DataFrame(data_total, columns=columns_total)
df_total = df_total.set_index('Timestamp')
df_total_reversed = df_total[::-1]
st.dataframe(df_total_reversed)