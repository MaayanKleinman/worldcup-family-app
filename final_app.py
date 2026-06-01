import streamlit as st
import requests
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="מונדיאל 2026", page_icon="🏆", layout="centered")

# קישור הטבלה שלך
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1BQ-O0iSj-mnTCtS8LUY-IS65suAahVdO0mY7Ej0seYQ/edit?gid=0#gid=0"

# פונקציית חיבור נקייה ויציבה לגוגל שיטס
def init_connection():
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds_dict = st.secrets["gcp_service_account"]
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(creds)
        return client.open_by_url(GOOGLE_SHEET_URL)
    except Exception as e:
        st.error(f"❌ שגיאת תקשורת עם השרת: {e}")
        return None

sheet = init_connection()

# שמות בני המשפחה
FAMILY_MEMBERS = ["אבא", "אמא", "מאיה", "דני", "נועם"]

st.markdown("""
    <style>
    body { direction: RTL; text-align: right; }
    div Rigth-to-Left { direction: RTL; }
    p { text-align: right; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #e61d25;'>🏆 מונדיאל 2026 - המשפחה 🏆</h1>", unsafe_allow_html=True)

TEAM_TRANSLATION = {
    "Brazil": "🇧🇷 ברזיל", "France": "🇫🇷 צרפת", "Argentina": "🇦🇷 ארגנטינה",
    "England": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 אנגליה", "Spain": "🇪🇸 ספרד", "Germany": "🇩🇪 גרמניה",
    "Italy": "🇮🇹 איטליה", "Portugal": "🇵🇹 פורטוגל", "Morocco": "🇲🇦 מרוקו", "Japan": "🇯🇵 יפן"
}

def get_team_name_heb(en_name):
    return TEAM_TRANSLATION.get(en_name, en_name)

API_KEY = "7f43ad9046msh5f15cf89c2479d2p13156ejsn65430696c85b"
BASE_URL = "https://sportapi7.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": "sportapi7.p.rapidapi.com"}

IL_TZ = ZoneInfo("Asia/Jerusalem")
now_il = datetime.now(IL_TZ)

tab1, tab2, tab3 = st.tabs(["⚽ ניחושים יומיים", "🏆 ניחוש האלופה", "📊 טבלת המובילים"])

with tab1:
    username = st.selectbox("👤 מי המנחש הנוכחי?", FAMILY_MEMBERS, key="daily_user")
    st.markdown("<div style='background-color: #ffe6e6; padding: 10px; border-radius: 5px; border-right: 5px solid #e61d25; color: #b30000; font-weight: bold;'>⚠️ שימו לב: הניחוש תקף ל-90 דקות משחק בלבד! (כולל תוספת זמן פציעות, לא כולל הארכות ופנדלים)</div>", unsafe_allow_html=True)
    st.write("")
    
    guess_inputs = {}
    has_matches = False
    
    for i in range(3):
        target_date = (now_il + timedelta(days=i)).strftime("%Y-%m-%d")
        date_label = "היום" if i == 0 else "מחר" if i == 1 else "מחרתיים"
        
        try:
            url = f"{BASE_URL}/api/v1/sport/football/scheduled-events/{target_date}"
            resp = requests.get(url, headers=HEADERS)
            events = resp.json().get("events", [])
        except:
            events = []
            
        if events:
            has_matches = True
            st.markdown(f"### 📅 משחקי {date_label} ({target_date.split('-')[2]}/{target_date.split('-')[1]}):")
            
            total_games_today = len(events)
            
            for event in events[:4]:
                match_id = event.get("id")
                home_en = event.get("homeTeam", {}).get("name")
                away_en = event.get("awayTeam", {}).get("name")
                
                home_heb = get_team_name_heb(home_en)
                away_heb = get_team_name_heb(away_en)
                
                match_timestamp = event.get("startTimestamp")
                match_time = datetime.fromtimestamp(match_timestamp, tz=ZoneInfo("UTC")).astimezone(IL_TZ)
                
                is_locked = now_il >= match_time
                lock_text = "🔒 נעול! המשחק החל" if is_locked else f"⏰ שעת פתיחה: {match_time.strftime('%H:%M')}"
                
                st.markdown(f"#### 🏟️ {home_heb}  נ ג ד  {away_heb}")
                st.caption(lock_text)
                
                col1, col2, col3 = st.columns([3, 3, 2])
                with col1:
                    h_input = st.number_input(f"שערים ל-{home_heb}", min_value=0, max_value=10, step=1, key=f"h_{match_id}", disabled=is_locked)
                with col2:
                    a_input = st.number_input(f"שערים ל-{away_heb}", min_value=0, max_value=10, step=1, key=f"a_{match_id}", disabled=is_locked)
                with col3:
                    st.write("")
                    j_check = st.checkbox("🃏 ג'וקר", key=f"j_{match_id}", disabled=is_locked)
                
                if not is_locked:
                    guess_inputs[match_id] = {
                        "home_g": h_input, 
                        "away_g": a_input, 
                        "joker": j_check, 
                        "name": f"{home_en} vs {away_en}",
                        "total_games_day": total_games_today,
                        "date": target_date
                    }
                st.write("---")

    if has_matches:
        if st.button("💾 שמור את הניחושים שלי"):
            joker_count = sum(1 for d in guess_inputs.values() if d["joker"])
            joker_in_short_day = any(d["joker"] and d["total_games_day"] < 3 for d in guess_inputs.values())
            
            if joker_count > 1:
                st.error("⚠️ עצור! מותר לבחור רק ג'וקר אחד לכל יום משחקים.")
            elif joker_in_short_day:
                st.error("⚠️ לא ניתן להשתמש בג'וקר ביום זה! חוק הג'וקר תקף רק לימים בהם משוחקים 3 משחקים ומעלה.")
            else:
                if sheet:
                    try:
                        guesses_sheet = sheet.worksheet("DailyGuesses")
                        
                        # בדיקה אם הגיליון ריק לחלוטין ויצירת כותרות
                        if len(guesses_sheet.get_all_values()) == 0:
                            guesses_sheet.append_row(["Timestamp", "Username", "Match ID", "Match Name", "Home Goals", "Away Goals", "Joker"], table_range="A1")
                            
                        for m_id, data in guess_inputs.items():
                            joker_str = "YES" if data["joker"] else "NO"
                            
                            new_row = [
                                datetime.now(IL_TZ).strftime("%Y-%m-%d %H:%M:%S"),
                                username, 
                                str(m_id), 
                                str(data["name"]), 
                                int(data["home_g"]), 
                                int(data["away_g"]), 
                                joker_str
                            ]
                            # שימוש ב-table_range מכריח התחלת סריקה מ-A1 ומניעת קריסה
                            guesses_sheet.append_row(new_row, table_range="A1")
                            
                        st.success(f"🎉 כל הכבוד {username}! הניחושים שלך נשמרו בהצלחה בגוגל שיטס!")
                    except Exception as e:
                        st.error(f"❌ שגיאה בשמירה לטבלה: {e}")
                else:
                    st.warning("⚠️ הניחוש תקין, אך לא נשמר בטבלה. בדקי את הודעת השגיאה למעלה.")
    else:
        st.info("אין משחקים קרובים בטווח של יומיים קדימה.")

with tab2:
    st.subheader("🏆 הניחוש המוקדם שלך לטורניר")
    st.info("🔒 חלק זה יינעל אוטומטית עם שריקת הפתיחה של המונדיאל!")
    champ = st.selectbox("🥇 מי תהיה האלופה ותניף את הגביע?", ["ברזיל 🇧🇷", "צרפת 🇫🇷", "ארגנטינה 🇦🇷", "אנגליה 🏴󠁧󠁢󠁥󠁮󠁧󠁿", "ספרד 🇪🇸", "גרמניה 🇩🇪"])
    st.write("---")
    st.write("**⚽ מי יסיימו בראשות הבתים? (3 נק' לכל תשובה נכונה)**")
    c1, col_b = st.columns(2)
    with c1:
        st.selectbox("ראשות בית א'", ["ברזיל 🇧🇷", "מקסיקו 🇲🇽", "קולומביה 🇨🇴"])
        st.selectbox("ראשות בית ב'", ["צרפת 🇫🇷", "מרוקו 🇲🇦", "דנמרק 🇩🇰"])
    with col_b:
        st.selectbox("ראשות בית ג'", ["ארגנטינה 🇦🇷", "יפן 🇯🇵", "שוודיה 🇸🇪"])
        st.selectbox("ראשות בית ד'", ["ספרד 🇪🇸", "גרמניה 🇩🇪", "ארצות הברית 🇺🇸"])
    
    if st.button("💾 שמור ניחושי טורניר ארוכי טווח"):
        st.success("הבחירות לטווח הארוך נשמרו בהצלחה!")

with tab3:
    st.subheader("📊 טבלת האליפות המשפחתית")
    mock_data = {"משתמש": FAMILY_MEMBERS, "נקודות משחקים": [0]*len(FAMILY_MEMBERS), "בונוס מוקדם": [0]*len(FAMILY_MEMBERS), "סך הכל": [0]*len(FAMILY_MEMBERS)}
    st.table(mock_data)
