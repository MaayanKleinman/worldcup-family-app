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
FAMILY_MEMBERS = ["אבא", "אמא", "מאיה", "דני", "נועם"]

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
    "Brazil": "ברזיל 🇧🇷", "France": "צרפת 🇫🇷", "Argentina": "ארגנטינה 🇦🇷",
    "England": "אנגליה 🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Spain": "ספרד 🇪🇸", "Germany": "גרמניה 🇩🇪",
    "Italy": "איטליה 🇮🇹", "Portugal": "פורטוגל 🇵🇹", "Morocco": "מרוקו 🇲🇦", "Japan": "יפן 🇯🇵",
    "Mexico": "מקסיקו 🇲🇽", "Canada": "קנדה 🇨🇦", "Czech Republic": "צ'כיה 🇨🇿", "Switzerland": "שווייץ 🇨🇭"
}

def get_team_name_heb(en_name):
    return TEAM_TRANSLATION.get(en_name, en_name)

def clean_string(text):
    if not text: return ""
    return "".join([c for c in text if c.isalnum()]).lower()

TOKEN = st.secrets["football_data_token"]
HEADERS = {"X-Auth-Token": TOKEN}

IL_TZ = ZoneInfo("Asia/Jerusalem")
now_il = datetime.now(IL_TZ)

# ⏱️ רענון מהיר וחכם - ה-Cache נשמר ל-120 שניות (2 דקות) בלבד! עדכון מהיר בלי לחסום את ה-API
@st.cache_data(ttl=120)
def fetch_world_cup_matches():
    try:
        url = "https://api.football-data.org/v4/competitions/WC/matches"
        resp = requests.get(url, headers=HEADERS)
        return resp.json().get("matches", [])
    except:
        return []

@st.cache_data(ttl=120)
def fetch_world_cup_standings():
    try:
        url = "https://api.football-data.org/v4/competitions/WC/standings"
        resp = requests.get(url, headers=HEADERS)
        return resp.json().get("standings", [])
    except:
        return []

all_wc_matches = fetch_world_cup_matches()
all_wc_standings = fetch_world_cup_standings()

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

target_date_str = now_il.strftime("%Y-%m-%d")
daily_events = [m for m in all_wc_matches if m.get("utcDate", "").startswith(target_date_str)]

if not daily_events:
    daily_events = [
        {
            "id": "test_match_1", "homeTeam": {"name": "Argentina"}, "awayTeam": {"name": "Brazil"}, 
            "utcDate": target_date_str + "T12:00:00Z", "status": "FINISHED", "score": {"fullTime": {"home": 2, "away": 1}}
        },
        {
            "id": "test_match_2", "homeTeam": {"name": "Mexico"}, "awayTeam": {"name": "Czech Republic"}, 
            "utcDate": target_date_str + "T23:59:00Z", "status": "TIMED", "score": {"fullTime": {"home": None, "away": None}}
        }
    ]

tab1, tab2, tab3 = st.tabs(["⚽ ניחושים יומיים", "🏆 ניחוש האלופה", "📊 טבלת המובילים"])

with tab1:
    st.markdown("<div style='background-color: #ffe6e6; padding: 10px; border-radius: 5px; border-right: 5px solid #e61d25; color: #b30000; font-weight: bold;'>⚠️ שימו לב: הניחוש תקף ל-90 דקות משחק בלבד! (כולל תוספת זמן פציעות, לא כולל הארכות ופנדלים)</div>", unsafe_allow_html=True)
    st.write("")
    
    guess_inputs = {}
    has_open_matches = False
    
    st.markdown(f"### 📅 משחקי היום ({target_date_str.split('-')[2]}/{target_date_str.split('-')[1]}):")
    
    for match in daily_events:
        match_id = match.get("id")
        home_en = match.get("homeTeam", {}).get("name")
        away_en = match.get("awayTeam", {}).get("name")
        home_heb = get_team_name_heb(home_en)
        away_heb = get_team_name_heb(away_en)
        
        utc_time_str = match.get("utcDate").replace("Z", "+00:00")
        match_time = datetime.fromisoformat(utc_time_str).astimezone(IL_TZ)
        is_locked = now_il >= match_time or match.get("status") == "FINISHED"
        
        if match.get("status") == "FINISHED":
            score_home = match.get("score", {}).get("fullTime", {}).get("home")
            score_away = match.get("score", {}).get("fullTime", {}).get("away")
            lock_text = f"🏁 המשחק הסתיים! תוצאת אמת: {home_heb} {score_home} - {score_away} {away_heb}"
        elif is_locked:
            lock_text = "🔒 נעול! המשחק החל"
        else:
            lock_text = f"⏰ שעת פתיחה: {match_time.strftime('%H:%M')}"
            has_open_matches = True
            
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
                "home_g": h_input, "away_g": a_input, "joker": j_check, 
                "name": f"{home_en} vs {away_en}", "total_games_day": len(daily_events), "date": target_date_str
            }
        st.write("---")

    if has_open_matches:
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
                        all_rows = guesses_sheet.get_all_values()
                        
                        if len(all_rows) == 0:
                            guesses_sheet.append_row(["Timestamp", "Username", "Match ID", "Match Name", "Home Goals", "Away Goals", "Joker"], table_range="A1")
                            all_rows = guesses_sheet.get_all_values()
                            
                        for m_id, data in guess_inputs.items():
                            joker_str = "YES" if data["joker"] else "NO"
                            new_row = [
                                datetime.now(IL_TZ).strftime("%Y-%m-%d %H:%M:%S"),
                                username, str(m_id), str(data["name"]), int(data["home_g"]), int(data["away_g"]), joker_str
                            ]
                            
                            existing_row_idx = None
                            for idx, row in enumerate(all_rows):
                                if idx == 0: continue
                                if len(row) > 2 and row[1] == username and row[2] == str(m_id):
                                    existing_row_idx = idx + 1
                                    break
                            
                            if existing_row_idx:
                                guesses_sheet.update(f"A{existing_row_idx}:G{existing_row_idx}", [new_row])
                            else:
                                guesses_sheet.append_row(new_row, table_range="A1")
                                
                        st.success(f"🎉 כל הכבוד {username}! הניחושים שלך עודכנו בהצלחה בטבלה!")
                    except Exception as e:
                        st.error(f"❌ שגיאה בשמירה: {e}")

with tab2:
    st.markdown("### 🏆 הניחוש המוקדם שלך לטורניר")
    st.info("🔒 חלק זה יינעל אוטומטית עם שריקת הפתיחה של המונדיאל!")
    
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
                all_t_rows = tournament_sheet.get_all_values()
                
                if len(all_t_rows) == 0:
                    headers = ["Timestamp", "Username", "Champion", "Group A", "Group B", "Group C", "Group D", "Group E", "Group F", "Group G", "Group H", "Group I", "Group J", "Group K", "Group L"]
                    tournament_sheet.append_row(headers, table_range="A1")
                    all_t_rows = tournament_sheet.get_all_values()
                
                t_row = [
                    datetime.now(IL_TZ).strftime("%Y-%m-%d %H:%M:%S"),
                    username, champ, group_a, group_b, group_c, group_d, group_e, group_f, group_g, group_h, group_i, group_j, group_k, group_l
                ]
                
                existing_t_idx = None
                for idx, row in enumerate(all_t_rows):
                    if idx == 0: continue
                    if len(row) > 1 and row[1] == username:
                        existing_t_idx = idx + 1
                        break
                        
                if existing_t_idx:
                    tournament_sheet.update(f"A{existing_t_idx}:O{existing_t_idx}", [t_row])
                else:
                    tournament_sheet.append_row(t_row, table_range="A1")
                    
                st.success(f"🎉 כל הכבוד {username}! הניחושים לטווח הארוך עודכנו בטבלה!")
            except Exception as e:
                st.error(f"❌ שגיאה בשמירה ללשונית הטורניר: {e}")

with tab3:
    st.markdown("### 📊 טבלת האליפות המשפחתית")
    scores_table = {member: {"משחקים": 0, "בונוס טורניר": 0, "סך הכל": 0} for member in FAMILY_MEMBERS}
    
    if sheet:
        try:
            # 1. עיבוד תוצאות אמת של משחקים מה-API + זיהוי אוטומטי של האלופה הרשמית מהגמר!
            actual_results = {}
            actual_champion = None
            
            # סריקה לאיתור האלופה הרשמית ממשחק הגמר
            for m in all_wc_matches:
                if m.get("status") == "FINISHED":
                    # איסוף תוצאות רגילות
                    full_time = m.get("score", {}).get("fullTime", {})
                    if full_time.get("home") is not None and full_time.get("away") is not None:
                        actual_results[str(m.get("id"))] = {"home": int(full_time.get("home")), "away": int(full_time.get("away"))}
                    
                    # בדיקה האם זה משחק הגמר כדי לנעול אלופה
                    if m.get("stage") == "FINAL":
                        winner_code = m.get("score", {}).get("winner") # "HOME_TEAM" או "AWAY_TEAM"
                        if winner_code == "HOME_TEAM":
                            actual_champion = clean_string(get_team_name_heb(m.get("homeTeam", {}).get("name")))
                        elif winner_code == "AWAY_TEAM":
                            actual_champion = clean_string(get_team_name_heb(m.get("awayTeam", {}).get("name")))
            
            # 🧪 סימולציה זמנית לבדיקות: אם הטורניר לא התחיל, נזריק אלופה ומשחק דמה כדי שתראו שזה עובד!
            if not actual_results:
                actual_results["test_match_1"] = {"home": 2, "away": 1}
                actual_champion = clean_string("ארגנטינה 🇦🇷") # קובע שארגנטינה היא האלופה לצורך הטסט

            # 2. עיבוד טבלאות בתים רשמיות לזיהוי מקום 1
            actual_group_winners = {}
            current_standings = all_wc_standings if all_wc_standings else [
                {"group": "GROUP_A", "table": [{"position": 1, "team": {"name": "Mexico"}}]},
                {"group": "GROUP_B", "table": [{"position": 1, "team": {"name": "Canada"}}]}
            ]
                
            for group_data in current_standings:
                g_name = group_data.get("group")
                g_table = group_data.get("table", [])
                if g_table:
                    top_team_en = g_table[0].get("team", {}).get("name")
                    actual_group_winners[g_name] = clean_string(get_team_name_heb(top_team_en))

            # 3. חישוב נקודות משחקים יומיים (חוק הפרש שערים רק בניצחונות!)
            guesses_sheet = sheet.worksheet("DailyGuesses")
            user_guesses = guesses_sheet.get_all_values()
            if len(user_guesses) > 1:
                for row in user_guesses[1:]:
                    if len(row) < 7: continue
                    g_user, g_match_id, g_home, g_away, g_joker = row[1], row[2], int(row[4]), int(row[5]), row[6] == "YES"
                    
                    if g_match_id in actual_results:
                        real = actual_results[g_match_id]
                        match_points = 0
                        
                        # 🏛️ מדרגות הניקוד המתוקנות:
                        if g_home == real["home"] and g_away == real["away"]:
                            match_points = 5 # בול בתוצאה (תופס גם לתיקו וגם לניצחון)
                        elif g_home != g_away and (g_home - g_away) == (real["home"] - real["away"]):
                            match_points = 3 # פגיעה בהפרש שערים - אך ורק אם זה לא תיקו!
                        elif (g_home > g_away and real["home"] > real["away"]) or \
                             (g_home < g_away and real["home"] < real["away"]) or \
                             (g_home == g_away and real["home"] == real["away"]):
                            match_points = 2 # פגיעה רק בכיוון הכללי של המשחק
                            
                        if g_joker: 
                            match_points *= 2
                            
                        if g_user in scores_table: 
                            scores_table[g_user]["משחקים"] += match_points

            # 4. חישוב אוטומטי של בונוס ראשי בתים + בונוס אלופה (10 נקודות!)
            tournament_sheet = sheet.worksheet("TournamentGuesses")
            t_guesses = tournament_sheet.get_all_values()
            
            group_columns_mapping = [
                ("GROUP_A", 3), ("GROUP_B", 4), ("GROUP_C", 5), ("GROUP_D", 6),
                ("GROUP_E", 7), ("GROUP_F", 8), ("GROUP_G", 9), ("GROUP_H", 10),
                ("GROUP_I", 11), ("GROUP_J", 12), ("GROUP_K", 13), ("GROUP_L", 14)
            ]
            
            if len(t_guesses) > 1:
                for row in t_guesses[1:]:
                    if len(row) < 15: continue
                    t_user = row[1]
                    if t_user in scores_table:
                        bonus_points = 0
                        
                        # א) בדיקת 12 הבתים
                        for group_key, col_idx in group_columns_mapping:
                            if group_key in actual_group_winners:
                                user_pick_clean = clean_string(row[col_idx])
                                if actual_group_winners[group_key] in user_pick_clean:
                                    bonus_points += 3
                                    
                        # ב) בדיקת האלופה הסופית (עמודה אינדקס 2) - מעניקה 10 נקודות בונוס!
                        if actual_champion:
                            user_champ_clean = clean_string(row[2])
                            if actual_champion in user_champ_clean:
                                bonus_points += 10
                                
                        scores_table[t_user]["בונוס טורניר"] += bonus_points

            # 5. סיכום סופי
            for member in scores_table:
                scores_table[member]["סך הכל"] = scores_table[member]["משחקים"] + scores_table[member]["בונוס טורניר"]
                
        except Exception as e:
            st.warning(f"טעינת נקודות: {e}")
            
    formatted_data = [{"משתמש": m, "⚽ נקודות משחקים": d["משחקים"], "🏆 בונוס טורניר": d["בונוס טורניר"], "🔥 סך הכל": d["סך הכל"]} for m, d in scores_table.items()]
    formatted_data = sorted(formatted_data, key=lambda x: x["🔥 סך הכל"], reverse=True)
    st.table(formatted_data)
