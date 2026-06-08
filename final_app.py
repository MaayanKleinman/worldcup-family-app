import streamlit as st
import requests
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="מונדיאל 2026", page_icon="🏆", layout="centered")

GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1BQ-O0iSj-mnTCtS8LUY-IS65suAahVdO0mY7Ej0seYQ/edit?gid=0#gid=0"

def init_connection():
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds_dict = dict(st.secrets["gcp_service_account"])
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(creds)
        return client.open_by_url(GOOGLE_SHEET_URL)
    except Exception as e:
        st.error(f"❌ שגיאת תקשורת עם גוגל שיטס: {e}")
        return None

sheet = init_connection()

@st.cache_data(ttl=60)
def get_cached_sheet_data(worksheet_name):
    if sheet:
        try:
            ws = sheet.worksheet(worksheet_name)
            return ws.get_all_values()
        except Exception:
            return []
    return []

# 👥 שמות המשתתפים הרשמיים של המשפחה
FAMILY_MEMBERS = ["נחש ינחש" , "מחליד", "המכשפה" , "צבצב", "יובל המנוול", "הזקן", "רתם המצחין", "עדיאל קורקוס"]

st.markdown("""
    <style>
    body { direction: RTL; text-align: right; }
    div Rigth-to-Left { direction: RTL; }
    p { text-align: right; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #e61d25;'>🏆 מונדיאל 2026 - המשפחה 🏆</h1>", unsafe_allow_html=True)

username = st.selectbox("👤 מי המנחש הנוכחי של המשפחה?", FAMILY_MEMBERS)
st.write("---")

TEAM_TRANSLATION = {
    "Mexico": "מקסיקו 🇲🇽", "South Africa": "דרום אפריקה 🇿🇦", "South Korea": "קוריאה הדרומית 🇰🇷", "Korea Republic": "קוריאה הדרומית 🇰🇷", "Korea": "קוריאה הדרומית 🇰🇷", "Czech Republic": "צ'כיה 🇨🇿", "Czechia": "צ'כיה 🇨🇿",
    "Canada": "קנדה 🇨🇦", "Bosnia and Herzegovina": "בוסניה והרצגובינה 🇧🇦", "Bosnia": "בוסניה והרצגובינה 🇧🇦", "Bosnia-Herzegovina": "בוסניה והרצגובינה 🇧🇦", "Qatar": "קטאר 🇶🇦", "Switzerland": "שווייץ 🇨🇭",
    "Brazil": "ברזיל 🇧🇷", "Morocco": "מרוקו 🇲🇦", "Haiti": "האיטי 🇭🇹", "Scotland": "סקוטלנד 🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    "USA": "ארצות הברית 🇺🇸", "United States": "ארצות הברית 🇺🇸", "United States of America": "ארצות הברית 🇺🇸", "Paraguay": "פרגוואי 🇵🇾", "Australia": "אוסטרליה 🇦🇺", "Turkey": "טורקיה 🇹🇷", "Türkiye": "טורקיה 🇹🇷",
    "Germany": "גרמניה 🇩🇪", "Curaçao": "קוראסאו 🇨🇼", "Curacao": "קוראסאו 🇨🇼", "Ivory Coast": "חוף השנהב 🇨🇮", "Côte d'Ivoire": "חוף השנהב 🇨🇮", "Cote d'Ivoire": "חוף השנהב 🇨🇮", "Ecuador": "אקוודור 🇪🇨",
    "Netherlands": "הולנד 🇳🇱", "Japan": "יפן 🇯🇵", "Sweden": "שוודיה 🇸🇪", "Tunisia": "טוניסיה 🇹🇳",
    "Belgium": "בלגיה 🇧🇪", "Egypt": "מצרים 🇪🇬", "Iran": "איראן 🇮🇷", "IR Iran": "איראן 🇮🇷", "New Zealand": "ניו זילנד 🇳🇿",
    "Spain": "ספרד 🇪🇸", "Cape Verde": "כף ורדה 🇨🇻", "Cabo Verde": "כף ורדה 🇨🇻", "Cape Verde Islands": "כף ורדה 🇨🇻", "Saudi Arabia": "ערב הסעודית 🇸🇦", "Uruguay": "אורוגוואי 🇺🇾",
    "France": "צרפת 🇫🇷", "Senegal": "סנגל 🇸🇳", "Iraq": "עיראק 🇮🇶", "Norway": "נורווגיה 🇳🇴",
    "Argentina": "ארגנטינה 🇦🇷", "Algeria": "אלג'יריה 🇩🇿", "Austria": "אוסטריה 🇦🇹", "Jordan": "ירדן 🇯🇴",
    "Portugal": "פורטוגל 🇵🇹", "DR Congo": "קונגו הדמוקרטית 🇨🇩", "Congo DR": "קונגו הדמוקרטית 🇨🇩", "Democratic Republic of the Congo": "קונגו הדמוקרטית 🇨🇩", "Uzbekistan": "אוזבקיסטן 🇺🇿", "Colombia": "קולומביה 🇨🇴",
    "England": "אנגליה 🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Croatia": "קרואטיה 🇭🇷", "Ghana": "גאנה 🇬🇭", "Panama": "פנמה 🇵🇦"
}

def get_team_name_heb(en_name):
    return TEAM_TRANSLATION.get(en_name, en_name)

def clean_string(text):
    if not text: return ""
    return "".join([c for c in text if c.isalnum()]).lower()

def safe_int(value, default=0):
    try:
        return int(str(value).strip())
    except (ValueError, TypeError):
        return default

TOKEN = st.secrets["football_data_token"]
HEADERS = {"X-Auth-Token": TOKEN}

IL_TZ = ZoneInfo("Asia/Jerusalem")
now_il = datetime.now(IL_TZ) 

TOURNAMENT_START_TIME = datetime(2026, 6, 11, 22, 0, tzinfo=IL_TZ)
is_tournament_started = now_il >= TOURNAMENT_START_TIME

@st.cache_data(ttl=120)
def fetch_world_cup_matches():
    try:
        url = "https://api.football-data.org/v4/competitions/WC/matches"
        resp = requests.get(url, headers=HEADERS)
        resp.raise_for_status()
        return resp.json().get("matches", [])
    except Exception:
        return None

@st.cache_data(ttl=120)
def fetch_world_cup_standings():
    try:
        url = "https://api.football-data.org/v4/competitions/WC/standings"
        resp = requests.get(url, headers=HEADERS)
        resp.raise_for_status()
        return resp.json().get("standings", [])
    except Exception:
        return None

all_wc_matches = fetch_world_cup_matches()
all_wc_standings = fetch_world_cup_standings()

if all_wc_matches is None:
    st.error("❌ תקלה קריטית בשליפת המשחקים משרתי פיפ\"א! לא ניתן להמשיך. אנא רעננו את העמוד או נסו מאוחר יותר.")
    st.stop()

if all_wc_standings is None:
    st.warning("⚠️ תקלה זמנית מול פיפ\"א בטעינת טבלאות הבתים. ניתן להמשיך למלא ניחושים יומיים כרגיל! (ייתכן שבונוס הבתים בטבלה לא מעודכן כרגע).")
    all_wc_standings = [] 

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

ALL_48_TEAMS = sorted(list(set(teams_a + teams_b + teams_c + teams_d + teams_e + teams_f + teams_g + teams_h + teams_i + teams_j + teams_k + teams_l)))

tab1, tab2, tab3 = st.tabs(["⚽ ניחושים יומיים", "🏆 ניחוש האלופה", "📊 טבלת המובילים"])

with tab1:
    st.markdown("<div style='background-color: #ffe6e6; padding: 10px; border-radius: 5px; border-right: 5px solid #e61d25; color: #b30000; font-weight: bold;'>⚠️ שימו לב: הניחוש תקף ל-90 דקות משחק בלבד! (כולל תוספת זמן פציעות, לא כולל הארכות ופנדלים)</div>", unsafe_allow_html=True)
    st.write("")
    
    user_daily_guesses = {}
    all_guesses = get_cached_sheet_data("DailyGuesses")
    if all_guesses:
        for row in all_guesses:
            if len(row) > 6 and row[1].strip() == username.strip():
                user_daily_guesses[row[2].strip()] = {
                    "home": row[4], "away": row[5], "joker": row[6]
                }

    has_any_open_matches = False
    
    for i in range(7): # מוגדר כרגע ל-7 ימים קדימה עבור הטסטים שלך
        current_loop_date_str = (now_il + timedelta(days=i)).strftime("%Y-%m-%d")
        if i == 0:
            date_label = "היום"
        elif i == 1:
            date_label = "מחר"
        elif i == 2:
            date_label = "מחרתיים"
        else:
            date_label = f"בעוד {i} ימים"
        
        daily_events = []
        for m in all_wc_matches:
            utc_time_str = m.get("utcDate", "")
            if utc_time_str:
                utc_time_str = utc_time_str.replace("Z", "+00:00")
                match_time_il = datetime.fromisoformat(utc_time_str).astimezone(IL_TZ)
                if match_time_il.strftime("%Y-%m-%d") == current_loop_date_str:
                    daily_events.append(m)
            
        if daily_events:
            st.markdown(f"### 📅 משחקי {date_label} ({current_loop_date_str.split('-')[2]}/{current_loop_date_str.split('-')[1]}):")
            total_games_today = len(daily_events)
            
            day_inputs = {}
            day_has_open = False
            
            for match in daily_events:
                match_id = str(match.get("id"))
                home_en = match.get("homeTeam", {}).get("name")
                away_en = match.get("awayTeam", {}).get("name")
                home_heb = get_team_name_heb(home_en)
                away_heb = get_team_name_heb(away_en)
                
                utc_time_str = match.get("utcDate").replace("Z", "+00:00")
                match_time = datetime.fromisoformat(utc_time_str).astimezone(IL_TZ)
                is_locked = now_il >= match_time or match.get("status") == "FINISHED"
                
                existing = user_daily_guesses.get(match_id, {})
                default_home = safe_int(existing.get("home"))
                default_away = safe_int(existing.get("away"))
                default_joker = existing.get("joker", "NO") == "YES"
                
                if match.get("status") == "FINISHED":
                    score_home = match.get("score", {}).get("fullTime", {}).get("home")
                    score_away = match.get("score", {}).get("fullTime", {}).get("away")
                    lock_text = f"🏁 המשחק הסתיים! תוצאת אמת: {home_heb} {score_home} - {score_away} {away_heb}"
                elif is_locked:
                    lock_text = f"🔒 נעול! המשחק החל (הניחוש שלך: {default_home} - {default_away})"
                else:
                    lock_text = f"⏰ שעת פתיחה: {match_time.strftime('%H:%M')}"
                    day_has_open = True
                    has_any_open_matches = True
                    
                st.markdown(f"#### 🏟️ {home_heb}  נ ג ד  {away_heb}")
                st.caption(lock_text)
                
                col1, col2, col3 = st.columns([3, 3, 2])
                with col1:
                    # הוספת הוי הירוק לשם הקבוצה מעל התיבה
                    h_label = f"✅ שערים ל-{home_heb}" if existing else f"שערים ל-{home_heb}"
                    h_input = st.number_input(h_label, min_value=0, max_value=10, step=1, key=f"h_{match_id}_{username}", value=default_home, disabled=is_locked)
                with col2:
                    a_label = f"✅ שערים ל-{away_heb}" if existing else f"שערים ל-{away_heb}"
                    a_input = st.number_input(a_label, min_value=0, max_value=10, step=1, key=f"a_{match_id}_{username}", value=default_away, disabled=is_locked)
                with col3:
                    st.write("")
                    # הוספת חיווי גם לג'וקר
                    j_label = "🃏 ג'וקר (✅ נשמר)" if existing else "🃏 ג'וקר"
                    j_check = st.checkbox(j_label, key=f"j_{match_id}_{username}", value=default_joker, disabled=is_locked)
                
                day_inputs[match_id] = {
                    "home_g": h_input, "away_g": a_input, "joker": j_check, "is_locked": is_locked,
                    "name": f"{home_en} vs {away_en}", "total_games_day": total_games_today
                }
                st.write("---")

            if day_has_open:
                if st.button(f"💾 שמור את ניחושי {date_label}", key=f"save_{current_loop_date_str}_{username}"):
                    joker_count = sum(1 for d in day_inputs.values() if d["joker"])
                    joker_in_short_day = any(d["joker"] and d["total_games_day"] < 3 for d in day_inputs.values())
                    
                    if joker_count > 1:
                        st.error(f"⚠️ עצור! מותר לבחור רק ג'וקר אחד עבור משחקי {date_label}.")
                    elif joker_in_short_day:
                        st.error("⚠️ לא ניתן להשתמש בג'וקר ביום זה! חוק הג'וקר תקף רק לימים בהם משוחקים 3 משחקים ומעלה.")
                    else:
                        if sheet:
                            try:
                                # 💉 --- תחילת בלוק הזרקת נתוני דמה לבדיקות (למחוק בסוף!) --- 💉
                                # לוקח אוטומטית את שני המשחקים הראשונים שמופיעים לך במסך וקובע להם תוצאה
                                if len(all_wc_matches) >= 2:
                                    fake_id_1 = str(all_wc_matches[0].get("id"))
                                    fake_id_2 = str(all_wc_matches[1].get("id"))
                
                                    actual_results[fake_id_1] = {"home": 2, "away": 1} # תוצאת אמת למשחק הראשון: 2-1
                                    actual_results[fake_id_2] = {"home": 0, "away": 0} # תוצאת אמת למשחק השני: 0-0
                                
                                # אלופה וסגנית מדומות לטובת בדיקת הבונוסים
                                actual_champion = clean_string("צרפת 🇫🇷")
                                actual_group_runners_up["GROUP_A"] = clean_string("מקסיקו 🇲🇽")
                                # 💉 --- סוף בלוק הזרקת הנתונים --- 💉
                                guesses_sheet = sheet.worksheet("DailyGuesses")
                                all_rows = get_cached_sheet_data("DailyGuesses")
                                    
                                for m_id, data in day_inputs.items():
                                    if data["is_locked"]: continue
                                    
                                    joker_str = "YES" if data["joker"] else "NO"
                                    new_row = [
                                        datetime.now(IL_TZ).strftime("%Y-%m-%d %H:%M:%S"),
                                        username, str(m_id), str(data["name"]), int(data["home_g"]), int(data["away_g"]), joker_str
                                    ]
                                    
                                    existing_row_idx = None
                                    for idx, row in enumerate(all_rows):
                                        if len(row) > 2 and row[1].strip() == username.strip() and row[2].strip() == str(m_id).strip():
                                            existing_row_idx = idx + 1
                                            break
                                    
                                    if existing_row_idx:
                                        guesses_sheet.update(f"A{existing_row_idx}:G{existing_row_idx}", [new_row])
                                    else:
                                        guesses_sheet.append_row(new_row, table_range="A1")
                                
                                get_cached_sheet_data.clear() 
                                st.success(f"🎉 כל הכבוד {username}! הניחושים שלך ליום {date_label} נשמרו בהצלחה!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ שגיאה בשמירה: {e}")
            else:
                st.info(f"🔒 כל המשחקים של יום {date_label} כבר נעולים או הסתיימו.")

    if not has_any_open_matches:
        st.info("אין משחקים פתוחים לניחוש כרגע בטווח הימים הקרוב.")

with tab2:
    st.markdown("### 🏆 הניחוש המוקדם שלך לטורניר")
    
    if is_tournament_started:
        st.error("🔒 הטורניר החל רשמית! חלק זה נעול לחלוטין ולא ניתן לשנות ניחושים יותר.")
    else:
        st.info("⏰ חלק זה יינעל אוטומטית ב-11 ליוני 2026 בשעה 22:00 עם שריקת הפתיחה של המונדיאל!")
    
    saved_t_guesses = []
    all_t_rows = get_cached_sheet_data("TournamentGuesses")
    if all_t_rows:
        for row in all_t_rows:
            if len(row) > 1 and row[1].strip() == username.strip():
                saved_t_guesses = row
                break

    def get_idx(lst, val):
        return lst.index(val) if val in lst else 0

    def_champ = get_idx(ALL_48_TEAMS, saved_t_guesses[2]) if len(saved_t_guesses) > 2 else 0
    def_a = get_idx(teams_a, saved_t_guesses[3]) if len(saved_t_guesses) > 3 else 0
    def_b = get_idx(teams_b, saved_t_guesses[4]) if len(saved_t_guesses) > 4 else 0
    def_c = get_idx(teams_c, saved_t_guesses[5]) if len(saved_t_guesses) > 5 else 0
    def_d = get_idx(teams_d, saved_t_guesses[6]) if len(saved_t_guesses) > 6 else 0
    def_e = get_idx(teams_e, saved_t_guesses[7]) if len(saved_t_guesses) > 7 else 0
    def_f = get_idx(teams_f, saved_t_guesses[8]) if len(saved_t_guesses) > 8 else 0
    def_g = get_idx(teams_g, saved_t_guesses[9]) if len(saved_t_guesses) > 9 else 0
    def_h = get_idx(teams_h, saved_t_guesses[10]) if len(saved_t_guesses) > 10 else 0
    def_i = get_idx(teams_i, saved_t_guesses[11]) if len(saved_t_guesses) > 11 else 0
    def_j = get_idx(teams_j, saved_t_guesses[12]) if len(saved_t_guesses) > 12 else 0
    def_k = get_idx(teams_k, saved_t_guesses[13]) if len(saved_t_guesses) > 13 else 0
    def_l = get_idx(teams_l, saved_t_guesses[14]) if len(saved_t_guesses) > 14 else 0

    champ = st.selectbox("🥇 מי תהיה האלופה ותניף את הגביע בסוף הטורניר?", ALL_48_TEAMS, index=def_champ, disabled=is_tournament_started, key=f"champ_{username}")
    st.write("---")
    st.markdown("#### ⚽ מי יסיימו במקום השני בבתים? (2 נק' לכל תשובה נכונה)")
    
    col1, col2 = st.columns(2)
    with col1:
        group_a = st.selectbox("מקום שני בית א'", teams_a, index=def_a, disabled=is_tournament_started, key=f"g_a_{username}")
        group_b = st.selectbox("מקום שני בית ב'", teams_b, index=def_b, disabled=is_tournament_started, key=f"g_b_{username}")
        group_c = st.selectbox("מקום שני בית ג'", teams_c, index=def_c, disabled=is_tournament_started, key=f"g_c_{username}")
        group_d = st.selectbox("מקום שני בית ד'", teams_d, index=def_d, disabled=is_tournament_started, key=f"g_d_{username}")
        group_e = st.selectbox("מקום שני בית ה'", teams_e, index=def_e, disabled=is_tournament_started, key=f"g_e_{username}")
        group_f = st.selectbox("מקום שני בית ו'", teams_f, index=def_f, disabled=is_tournament_started, key=f"g_f_{username}")
    with col2:
        group_g = st.selectbox("מקום שני בית ז'", teams_g, index=def_g, disabled=is_tournament_started, key=f"g_g_{username}")
        group_h = st.selectbox("מקום שני בית ח'", teams_h, index=def_h, disabled=is_tournament_started, key=f"g_h_{username}")
        group_i = st.selectbox("מקום שני בית ט'", teams_i, index=def_i, disabled=is_tournament_started, key=f"g_i_{username}")
        group_j = st.selectbox("מקום שני בית י'", teams_j, index=def_j, disabled=is_tournament_started, key=f"g_j_{username}")
        group_k = st.selectbox("מקום שני בית י\"א", teams_k, index=def_k, disabled=is_tournament_started, key=f"g_k_{username}")
        group_l = st.selectbox("מקום שני בית י\"ב", teams_l, index=def_l, disabled=is_tournament_started, key=f"g_l_{username}")

    st.write("---")
    if st.button("💾 שמור ניחושי טורניר ארוכי טווח", disabled=is_tournament_started, key=f"save_tour_{username}"):
        if sheet:
            try:
                tournament_sheet = sheet.worksheet("TournamentGuesses")
                current_all_t_rows = get_cached_sheet_data("TournamentGuesses")
                
                if len(current_all_t_rows) == 0:
                    headers = ["Timestamp", "Username", "Champion", "Group A", "Group B", "Group C", "Group D", "Group E", "Group F", "Group G", "Group H", "Group I", "Group J", "Group K", "Group L"]
                    tournament_sheet.append_row(headers, table_range="A1")
                    current_all_t_rows = [headers] 
                
                t_row = [
                    datetime.now(IL_TZ).strftime("%Y-%m-%d %H:%M:%S"),
                    username, champ, group_a, group_b, group_c, group_d, group_e, group_f, group_g, group_h, group_i, group_j, group_k, group_l
                ]
                
                existing_t_idx = None
                for idx, row in enumerate(current_all_t_rows):
                    if len(row) > 1 and row[1].strip() == username.strip():
                        existing_t_idx = idx + 1
                        break
                        
                if existing_t_idx:
                    tournament_sheet.update(f"A{existing_t_idx}:O{existing_t_idx}", [t_row])
                else:
                    tournament_sheet.append_row(t_row, table_range="A1")
                
                get_cached_sheet_data.clear() 
                st.success(f"🎉 כל הכבוד {username}! הניחושים לטווח הארוך עודכנו בטבלה!")
            except Exception as e:
                st.error(f"❌ שגיאה בשמירה ללשונית הטורניר: {e}")

with tab3:
    st.markdown("### 📊 טבלת האליפות המשפחתית")
    scores_table = {member: {"משחקים": 0, "בונוס טורניר": 0, "סך הכל": 0} for member in FAMILY_MEMBERS}
    
    if sheet:
        try:
            actual_results = {}
            actual_champion = None
            
            for m in all_wc_matches:
                if m.get("status") == "FINISHED":
                    full_time = m.get("score", {}).get("fullTime", {})
                    if full_time.get("home") is not None and full_time.get("away") is not None:
                        actual_results[str(m.get("id"))] = {"home": int(full_time.get("home")), "away": int(full_time.get("away"))}
                    
                    if m.get("stage") == "FINAL":
                        winner_code = m.get("score", {}).get("winner")
                        if winner_code == "HOME_TEAM":
                            actual_champion = clean_string(get_team_name_heb(m.get("homeTeam", {}).get("name")))
                        elif winner_code == "AWAY_TEAM":
                            actual_champion = clean_string(get_team_name_heb(m.get("awayTeam", {}).get("name")))
            
            actual_group_runners_up = {}
            for group_data in all_wc_standings:
                g_name = group_data.get("group")
                g_table = group_data.get("table", [])
                if len(g_table) > 1:
                    second_team_en = g_table[1].get("team", {}).get("name")
                    actual_group_runners_up[g_name] = clean_string(get_team_name_heb(second_team_en))

            user_guesses = get_cached_sheet_data("DailyGuesses")
            if len(user_guesses) > 0:
                for row in user_guesses:
                    if len(row) < 7: continue
                    g_user = row[1]
                    g_match_id = row[2]
                    try:
                        g_home = int(row[4])
                        g_away = int(row[5])
                    except ValueError:
                        continue 
                    g_joker = row[6] == "YES"
                    
                    if g_match_id in actual_results:
                        real = actual_results[g_match_id]
                        match_points = 0
                        
                        if g_home == real["home"] and g_away == real["away"]:
                            match_points = 3
                        elif (g_home > g_away and real["home"] > real["away"]) or \
                             (g_home < g_away and real["home"] < real["away"]) or \
                             (g_home == g_away and real["home"] == real["away"]):
                            match_points = 1 
                            
                        if g_joker: 
                            match_points *= 2
                            
                        if g_user in scores_table: 
                            scores_table[g_user]["משחקים"] += match_points

            t_guesses = get_cached_sheet_data("TournamentGuesses")
            
            group_columns_mapping = [
                ("GROUP_A", 3), ("GROUP_B", 4), ("GROUP_C", 5), ("GROUP_D", 6),
                ("GROUP_E", 7), ("GROUP_F", 8), ("GROUP_G", 9), ("GROUP_H", 10),
                ("GROUP_I", 11), ("GROUP_J", 12), ("GROUP_K", 13), ("GROUP_L", 14)
            ]
            
            if len(t_guesses) > 0:
                for row in t_guesses:
                    if len(row) < 3: continue 
                    t_user = row[1]
                    if t_user in scores_table:
                        bonus_points = 0
                        
                        for group_key, col_idx in group_columns_mapping:
                            if group_key in actual_group_runners_up and len(row) > col_idx:
                                user_pick_clean = clean_string(row[col_idx])
                                if actual_group_runners_up[group_key] in user_pick_clean:
                                    bonus_points += 2 
                                    
                        if actual_champion and len(row) > 2:
                            user_champ_clean = clean_string(row[2])
                            if actual_champion in user_champ_clean:
                                bonus_points += 8 
                                
                        scores_table[t_user]["בונוס טורניר"] += bonus_points

            for member in scores_table:
                scores_table[member]["סך הכל"] = scores_table[member]["משחקים"] + scores_table[member]["בונוס טורניר"]
                
        except Exception as e:
            st.warning(f"טעינת נקודות: {e}")
            
    formatted_data = [{"משתמש": m, "⚽ נקודות משחקים": d["משחקים"], "🏆 בונוס טורניר": d["בונוס טורניר"], "🔥 סך הכל": d["סך הכל"]} for m, d in scores_table.items()]
    formatted_data = sorted(formatted_data, key=lambda x: x["🔥 סך הכל"], reverse=True)
    st.table(formatted_data)
