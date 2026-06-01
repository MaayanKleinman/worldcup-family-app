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
        creds_dict = dict(st.secrets["gcp_service_account"])
        
        # מתקן את קידוד השורות כדי שהמפתח ייקרא בצורה תקינה
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
        
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

# בחירת המנחש בחלק העליון
username = st.selectbox("👤 מי המנחש הנוכחי של המשפחה?", FAMILY_MEMBERS)
st.write("---")

TEAM_TRANSLATION = {
    "Brazil": "ברזיל 🇧🇷", "France": "צרפת 🇫🇷", "Argentina": "ארגנטינה 🇦🇷",
    "England": "אנגליה 🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Spain": "ספרד 🇪🇸", "Germany": "גרמניה 🇩🇪",
    "Italy": "איטליה 🇮🇹", "Portugal": "פורטוגל 🇵🇹", "Morocco": "מרוקו 🇲🇦", "Japan": "יפן 🇯🇵"
}

def get_team_name_heb(en_name):
    return TEAM_TRANSLATION.get(en_name, en_name)

API_KEY = "7f43ad9046msh5f15cf89c2479d2p13156ejsn65430696c85b"
BASE_URL = "https://sportapi7.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": "sportapi7.p.rapidapi.com"}

IL_TZ = ZoneInfo("Asia/Jerusalem")
now_il = datetime.now(IL_TZ)

# הגדרת הבתים הרשמית (מתוך הרשימה שלך)
teams_a = ["מקסיקו 🇲🇽", "דרום אפריקה 🇿🇦", "קוריאה הדרומית 🇰🇷", "צ'כיה 🇨🇿"]
teams_b = ["קנדה 🇨🇦", "בוסניה והרצגובינה 🇧🇦", "קטאר 🇶🇦", "שווייץ 🇨🇭"]
teams_c = ["ברזיל 🇧🇷", "מרוקו 🇲🇦", "האיטי 🇭🇹", "סקוטלנד 🏴󠁧󠁢󠁳󠁣󠁴󠁿"]
teams_d = ["ארצות הברית 🇺🇸", "פרגוואי 🇵🇾", "אוסטרליה 🇦🇺", "טורקיה 🇹🇷"]
teams_e = ["גרמניה 🇩🇪", "קוראסאו 🇨🇼", "חוף השנהב 🇨🇮", "אקוודור 🇪🇨"]
teams_f = ["הולנד 🇳🇱", "יפן 🇯🇵", "שוודיה 🇸🇪", "טוניסיה 🇹🇳"]
teams_g = ["בלגיה 🇧🇪", "מצרים 🇪🇬", "איראן 🇮🇷", "ניו זילנד 🇳🇿"]
teams_h = ["ספרד 🇪🇸", "כף ורדה 🇨🇻", "ערב הסעודית 🇸🇦", "אורוגוואי 🇺🇾"]
teams_i = ["צרפת 🇫🇷", "סנגל 🇸🇳", "עיראק 🇮🇶", "נורווגיה 🇳🇴"]
teams_j = ["ארגנטינה 🇦🇷", "אלג'יריה 🇩🇿", "אוסטריה 🇦🇹", "ירדן 🇯🇴"]
teams_k = ["פורטוגל 🇵🇹", "קונגו הדמוקרטית 🇨🇩", "אוזבקיסטן 🇺🇿", "קולומביה 🇨🇴"]
teams_l = ["אנגליה 🏴󠁧󠁢󠁥󠁮󠁧󠁿", "קרואטיה 🇭🇷", "גאנה 🇬🇭", "פנמה 🇵🇦"]

# יצירה אוטומטית של רשימת כל 48 הנבחרות הייחודיות, ממוינות אלפביתית למסך האלופה
ALL_48_TEAMS = sorted(list(set(teams_a + teams_b + teams_c + teams_d + teams_e + teams_f + teams_g + teams_h + teams_i + teams_j + teams_k + teams_l)))

tab1, tab2, tab3 = st.tabs(["⚽ ניחושים יומיים", "🏆 ניחוש האלופה", "📊 טבלת המובילים"])

with tab1:
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
            
        # בלוק סימולציה זמני לבדיקות
        if not events and i == 0:
            now_utc_ts = int(datetime.now(ZoneInfo("UTC")).timestamp())
            events = [
                {
                    "id": "test_match_1",
                    "homeTeam": {"name": "Argentina"},
                    "awayTeam": {"name": "Brazil"},
                    "startTimestamp": now_utc_ts + 7200
                },
                {
                    "id": "test_match_2",
                    "homeTeam": {"name": "France"},
                    "awayTeam": {"name": "England"},
                    "startTimestamp": now_utc_ts + 10800
                }
            ]
            
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
        if st.button("💾 שמור את הניחושים היומיים שלי"):
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
                        if len(guesses_sheet.get_all_values()) == 0:
                            guesses_sheet.append_row(["Timestamp", "Username", "Match ID", "Match Name", "Home Goals", "Away Goals", "Joker"], table_range="A1")
                            
                        for m_id, data in guess_inputs.items():
                            joker_str = "YES" if data["joker"] else "NO"
                            new_row = [
                                datetime.now(IL_TZ).strftime("%Y-%m-%d %H:%M:%S"),
                                username, str(m_id), str(data["name"]), int(data["home_g"]), int(data["away_g"]), joker_str
                            ]
                            guesses_sheet.append_row(new_row, table_range="A1")
                        st.success(f"🎉 כל הכבוד {username}! הניחושים שלך נשמרו בהצלחה!")
                    except Exception as e:
                        st.error(f"❌ שגיאה בשמירה לטבלה: {e}")
                else:
                    st.warning("⚠️ אין חיבור לטבלה.")
    else:
        st.info("אין משחקים קרובים בטווח של יומיים קדימה.")

with tab2:
    st.markdown("### 🏆 הניחוש המוקדם שלך לטורניר")
    st.info("🔒 חלק זה יינעל אוטומטית עם שריקת הפתיחה של המונדיאל!")
    
    # שימוש ברשימה המלאה והמסודרת של כל 48 הנבחרות
    champ = st.selectbox("🥇 מי תהיה האלופה ותניף את הגביע בסוף הטורניר?", ALL_48_TEAMS)
    st.write("---")
    
    st.markdown("#### ⚽ מי יסיימו בראשות הבתים? (3 נק' לכל תשובה נכונה)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        group_a = st.selectbox("ראשות בית א'", teams_a)
        group_b = st.selectbox("ראשות בית ב'", teams_b)
        group_c = st.selectbox("ראשות בית ג'", teams_c)
        group_d = st.selectbox("ראשות בית ד'", teams_d)
        group_e = st.selectbox("ראשות בית ה'", teams_e)
        group_f = st.selectbox("ראשות בית ו'", teams_f)

    with col2:
        group_g = st.selectbox("ראשות בית ז'", teams_g)
        group_h = st.selectbox("ראשות בית ח'", teams_h)
        group_i = st.selectbox("ראשות בית ט'", teams_i)
        group_j = st.selectbox("ראשות בית י'", teams_j)
        group_k = st.selectbox("ראשות בית י\"א", teams_k)
        group_l = st.selectbox("ראשות בית י\"ב", teams_l)

    st.write("---")
    if st.button("💾 שמור ניחושי טורניר ארוכי טווח"):
        if sheet:
            try:
                tournament_sheet = sheet.worksheet("TournamentGuesses")
                
                if len(tournament_sheet.get_all_values()) == 0:
                    headers = ["Timestamp", "Username", "Champion", "Group A", "Group B", "Group C", "Group D", "Group E", "Group F", "Group G", "Group H", "Group I", "Group J", "Group K", "Group L"]
                    tournament_sheet.append_row(headers, table_range="A1")
                
                t_row = [
                    datetime.now(IL_TZ).strftime("%Y-%m-%d %H:%M:%S"),
                    username, champ, group_a, group_b, group_c, group_d, group_e, group_f, group_g, group_h, group_i, group_j, group_k, group_l
                ]
                tournament_sheet.append_row(t_row, table_range="A1")
                st.success(f"🎉 כל הכבוד {username}! הניחושים לטווח הארוך (כולל כל 12 הבתים) נשמרו בטבלה!")
            except Exception as e:
                st.error(f"❌ שגיאה בשמירה ללשונית הטורניר: {e}")
        else:
            st.error("⚠️ השרת אינו מחובר לגוגל שיטס.")

with tab3:
    st.subheader("📊 טבלת האליפות המשפחתית")
    mock_data = {"משתמש": FAMILY_MEMBERS, "נקודות משחקים": [0]*len(FAMILY_MEMBERS), "בונוס מוקדם": [0]*len(FAMILY_MEMBERS), "סך הכל": [0]*len(FAMILY_MEMBERS)}
    st.table(mock_data)
