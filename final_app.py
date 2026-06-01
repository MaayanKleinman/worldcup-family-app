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

def safe_update(worksheet, range_name, values):
    try:
        worksheet.update(values=values, range_name=range_name)
    except:
        try:
            worksheet.update(range_name, values)
        except Exception as e:
            st.error(f"❌ שגיאה בעדכון השורה בשיטס: {e}")

# 👥 שמות המשתתפים המעודכנים והמצחיקים שלכם!
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

# 🌍 מילון תרגום מתוקן הרמטית לפי הנתונים הגולמיים של ה-API
TEAM_TRANSLATION = {
    # בית א'
    "Mexico": "מקסיקו 🇲🇽",
    "South Africa": "דרום אפריקה 🇿🇦",
    "South Korea": "קוריאה הדרומית 🇰🇷", "Korea Republic": "קוריאה הדרומית 🇰🇷", "Korea": "קוריאה הדרומית 🇰🇷",
    "Czech Republic": "צ'כיה 🇨🇿", "Czechia": "צ'כיה 🇨🇿",
    # בית ב'
    "Canada": "קנדה 🇨🇦",
    "Bosnia and Herzegovina": "בוסניה והרצגובינה 🇧🇦", "Bosnia": "בוסניה והרצגובינה 🇧🇦", "Bosnia-Herzegovina": "בוסניה והרצגובינה 🇧🇦",
    "Qatar": "קטאר 🇶🇦",
    "Switzerland": "שווייץ 🇨🇭",
    # בית ג'
    "Brazil": "ברזיל 🇧🇷",
    "Morocco": "מרוקו 🇲🇦",
    "Haiti": "האיטי 🇭🇹",
    "Scotland": "סקוטלנד 🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    # בית ד'
    "USA": "ארצות הברית 🇺🇸", "United States": "ארצות הברית 🇺🇸", "United States of America": "ארצות הברית 🇺🇸",
    "Paraguay": "פרגוואי 🇵🇾",
    "Australia": "אוסטרליה 🇦🇺",
    "Turkey": "טורקיה 🇹🇷", "Türkiye": "טורקיה 🇹🇷",
    # בית ה'
    "Germany": "גרמניה 🇩🇪",
    "Curaçao": "קוראסאו 🇨🇼", "Curacao": "קוראסאו 🇨🇼",
    "Ivory Coast": "חוף השנהב 🇨🇮", "Côte d'Ivoire": "חוף השנהב 🇨🇮", "Cote d'Ivoire": "חוף השנהב 🇨🇮",
    "Ecuador": "אקוודור 🇪🇨",
    # בית ו'
    "Netherlands": "הולנד 🇳🇱",
    "Japan": "יפן 🇯🇵",
    "Sweden": "שוודיה 🇸🇪",
    "Tunisia": "טוניסיה 🇹🇳",
    # בית ז'
    "Belgium": "בלגיה 🇧🇪",
    "Egypt": "מצרים 🇪🇬",
    "Iran": "איראן 🇮🇷", "IR Iran": "איראן 🇮🇷",
    "New Zealand": "ניו זילנד 🇳🇿",
    # בית ח'
    "Spain": "ספרד 🇪🇸",
    "Cape Verde": "כף ורדה 🇨🇻", "Cabo Verde": "כף ורדה 🇨🇻", "Cape Verde Islands": "כף ורדה 🇨🇻",
    "Saudi Arabia": "ערב הסעודית 🇸🇦",
    "Uruguay": "אורוגוואי 🇺🇾",
    # בית ט'
    "France": "צרפת 🇫🇷",
    "Senegal": "סנגל 🇸🇳",
    "Iraq": "עיראק 🇮🇶",
    "Norway": "נורווגיה 🇳🇴",
    # בית י'
    "Argentina": "ארגנטינה 🇦🇷",
    "Algeria": "אלג'יריה 🇩🇿",
    "Austria": "אוסטריה 🇦🇹",
    "Jordan": "ירדן 🇯🇴",
    # בית י"א
    "Portugal": "פורטוגל 🇵🇹",
    "DR Congo": "קונגו הדמוקרטית 🇨🇩", "Congo DR": "קונגו הדמוקרטית 🇨🇩", "Democratic Republic of the Congo": "קונגו הדמוקרטית 🇨🇩",
    "Uzbekistan": "אוזבקיסטן 🇺🇿",
    "Colombia": "קולומביה 🇨🇴",
    # בית י"ב
    "England": "אנגליה 🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "Croatia": "קרואטיה 🇭🇷",
    "Ghana": "גאנה 🇬🇭",
    "Panama": "פנמה 🇵🇦"
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

TOURNAMENT_START_TIME = datetime(2026, 6, 11, 22, 0, tzinfo=IL_TZ)
is_tournament_started = now_il >= TOURNAMENT_START_TIME

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
teams_b = ["קנדה 🇨🇦", "בוסניה והרצגובינה 🇧🇦", "קטאר 🇶🇦", "שווייץ 🇨חש"]
teams_c = ["ברזיל 🇧🇷", "מרוקו 🇲🇦", "האיטי 🇭🇹", "סקוטלנד 🏴󠁧󠁢󠁳󠁣󠁴󠁿"]
teams_d = ["ארצות הברית 🇺🇸", "פרגוואי 🇵🇾", "אוסטרליה 🇦🇺", "טורקיה 🇹🇷"]
teams_e = ["גרמניה 🇩🇪", "קוראסאו 🇨🇼", "חוף השנהב 🇨🇮", "אקוודור 🇪🇨"]
teams_f = ["הולנד 🇳🇱", "יפן 🇯🇵", "שוודיה 🇸🇪", "טוניסיה 🇹🇳"]
teams_g = ["בלגיה 🇧🇪", "מצרים 🇪🇬", "איראן 🇮🇷", "ניו זילנד 🇳🇿"]
teams_h = ["ספרד 🇪🇸", "כף ורדה 🇨🇻", "ערב הסעודית 🇸🇦", "אורוגוואי 🇺🇾"]
teams_i = ["צרפת 🇫🇷", "סנגל 🇸🇳", "עיראק 🇮🇶", "נורווגיה 🇳🇴"]
teams_j = ["ארגנטינה 🇦🇷", "אלג'יריה 🇩🇿", "אוסטריה 🇦🇹", "ירדן 🇯🇴"]
teams_k = ["פורטוגל 🇵🇹", "קונגו הדמוקרטית 🇨🇩", "אוזבקיסטן 🇺🇿", "קולומביה 🇨🇴"]
teams_l = ["אנגליה 🏴󠁧󠁢󠁥󠁮󠁧󠁿", "קרואטיה 🇭🇷", "גאנה 🇬🇭", "פנמה פנמה 🇵🇦"]

ALL_48_TEAMS = sorted(list(set(teams_a + teams_b + teams_c + teams_d + teams_e + teams_f + teams_g + teams_h + teams_i + teams_j + teams_k + teams_l)))

tab1, tab2, tab3 = st.tabs(["⚽ ניחושים יומיים", "🏆 ניחוש האלופה", "📊 טבלת המובילים"])

with tab1:
    st.markdown("<div style='background-color: #ffe6e6; padding: 10px; border-radius: 5px; border-right: 5px solid #e61d25; color: #b30000; font-weight: bold;'>⚠️ שימו לב: הניחוש תקף ל-90 דקות משחק בלבד! (כולל תוספת זמן פציעות, לא כולל הארכות ופנדלים)</div>", unsafe_allow_html=True)
    st.write("")
    
    guess_inputs = {}
    has_open_matches = False
    
    for i in range(3):
        current_loop_date_str = (now_il + timedelta(days=i)).strftime("%Y-%m-%d")
        date_label = "היום" if i == 0 else "מחר" if i == 1 else "מחרתיים"
        
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
                        "name": f"{home_en} vs {away_en}", "total_games_day": total_games_today, "date": current_loop_date_str
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
                        
                        u_idx = 1 
                        m_idx = 2 
                            
                        for m_id, data in guess_inputs.items():
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
                                
                        st.success(f"🎉 כל הכבוד {username}! הניחושים שלך עודכנו בהצלחה בטבלה!")
                    except Exception as e:
                        st.error(f"❌ שגיאה בשמירה: {e}")
    else:
        st.info("אין משחקים פתוחים לניחוש כרגע בטווח הימים הקרוב.")

with tab2:
    st.markdown("### 🏆 הניחוש המוקדם שלך לטורניר")
    
    if is_tournament_started:
        st.error("🔒 הטורניר החל רשמית! חלק זה נעול לחלוטין ולא ניתן לשנות ניחושים יותר.")
    else:
        st.info("⏰ חלק זה יינעל אוטומטית ב-11 ליוני 2026 בשעה 22:00 עם שריקת הפתיחה של המונדיאל!")
    
    champ = st.selectbox("🥇 מי תהיה האלופה ותניף את הגביע בסוף הטורניר?", ALL_48_TEAMS, disabled=is_tournament_started)
    st.write("---")
    st.markdown("#### ⚽ מי יסיימו בראשות הבתים? (3 נק' לכל תשובה נכונה)")
    
    col1, col2 = st.columns(2)
    with col1:
        group_a = st.selectbox("ראשות בית א'", teams_a, disabled=is_tournament_started)
        group_b = st.selectbox("ראשות בית ב'", teams_b, disabled=is_tournament_started)
        group_c = st.selectbox("ראשות בית ג'", teams_c, disabled=is_tournament_started)
        group_d = st.selectbox("ראשות בית ד'", teams_d, disabled=is_tournament_started)
        group_e = st.selectbox("ראשות בית ה'", teams_e, disabled=is_tournament_started)
        group_f = st.selectbox("ראשות בית ו'", teams_f, disabled=is_tournament_started)
    with col2:
        group_g = st.selectbox("ראשות בית ז'", teams_g, disabled=is_tournament_started)
        group_h = st.selectbox("ראשות בית ח'", teams_h, disabled=is_tournament_started)
        group_i = st.selectbox("ראשות בית ט'", teams_i, disabled=is_tournament_started)
        group_j = st.selectbox("ראשות בית י'", teams_j, disabled=is_tournament_started)
        group_k = st.selectbox("ראשות בית י\"א", teams_k, disabled=is_tournament_started)
        group_l = st.selectbox("ראשות בית י\"ב", teams_l, disabled=is_tournament_started)

    st.write("---")
    if st.button("💾 שמור ניחושי טורניר ארוכי טווח", disabled=is_tournament_started):
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
                    if len(row) > 1 and row[1].strip() == username.strip():
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
            
            actual_group_winners = {}
            for group_data in all_wc_standings:
                g_name = group_data.get("group")
                g_table = group_data.get("table", [])
                if g_table:
                    top_team_en = g_table[0].get("team", {}).get("name")
                    actual_group_winners[g_name] = clean_string(get_team_name_heb(top_team_en))

            guesses_sheet = sheet.worksheet("DailyGuesses")
            user_guesses = guesses_sheet.get_all_values()
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
                            match_points = 5 
                        elif g_home != g_away and (g_home - g_away) == (real["home"] - real["away"]):
                            match_points = 3 
                        elif (g_home > g_away and real["home"] > real["away"]) or \
                             (g_home < g_away and real["home"] < real["away"]) or \
                             (g_home == g_away and real["home"] == real["away"]):
                            match_points = 2 
                            
                        if g_joker: 
                            match_points *= 2
                            
                        if g_user in scores_table: 
                            scores_table[g_user]["משחקים"] += match_points

            tournament_sheet = sheet.worksheet("TournamentGuesses")
            t_guesses = tournament_sheet.get_all_values()
            
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
                            if group_key in actual_group_winners and len(row) > col_idx:
                                user_pick_clean = clean_string(row[col_idx])
                                if actual_group_winners[group_key] in user_pick_clean:
                                    bonus_points += 3
                                    
                        if actual_champion and len(row) > 2:
                            user_champ_clean = clean_string(row[2])
                            if actual_champion in user_champ_clean:
                                bonus_points += 10
                                
                        scores_table[t_user]["בונוס טורניר"] += bonus_points

            for member in scores_table:
                scores_table[member]["סך הכל"] = scores_table[member]["משחקים"] + scores_table[member]["בונוס טורניר"]
                
        except Exception as e:
            st.warning(f"טעינת נקודות: {e}")
            
    formatted_data = [{"משתמש": m, "⚽ נקודות משחקים": d["משחקים"], "🏆 בונוס טורניר": d["בונוס טורניר"], "🔥 סך הכל": d["סך הכל"]} for m, d in scores_table.items()]
    formatted_data = sorted(formatted_data, key=lambda x: x["🔥 סך הכל"], reverse=True)
    st.table(formatted_data)
