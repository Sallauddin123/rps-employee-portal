"""Generate demo data for the RPS Employee Portal: 1 Aug 2026 -> 24 Oct 2026 (now 21:20 IST)."""
import json, random, hashlib, os, re
from datetime import date, datetime, timedelta

R = random.Random(20261024)
START, TODAY = date(2026, 8, 1), date(2026, 10, 24)
NOW_MIN = 21 * 60 + 20  # 21:20 IST
HOL = {"2026-08-15", "2026-09-14", "2026-10-02", "2026-10-20"}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seed")

def ds(d): return d.isoformat()
def iso(d, minutes):
    """IST wall-clock minutes on date d -> UTC ISO string."""
    dt = datetime(d.year, d.month, d.day) + timedelta(minutes=minutes) - timedelta(hours=5, minutes=30)
    return dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")
def h(s): return hashlib.sha256(s.encode()).hexdigest()
def is_wd(d): return d.weekday() != 6 and ds(d) not in HOL
def daterange(a, b):
    while a <= b:
        yield a; a += timedelta(days=1)
def add_wd(d, n):
    while n > 0:
        d += timedelta(days=1)
        if is_wd(d): n -= 1
    return d

# id, name, role, dept, joined, gross, persona
P = {  # persona: attend, late, start(min), hours, report, ontime, accept, busy
 "star":    dict(att=.985, late=.03, st=9*60+30, hrs=9.4, rep=.99, on=.93, acc=.98),
 "good":    dict(att=.965, late=.08, st=9*60+45, hrs=8.7, rep=.95, on=.85, acc=.96),
 "avg":     dict(att=.94,  late=.15, st=9*60+55, hrs=8.3, rep=.88, on=.74, acc=.93),
 "late":    dict(att=.95,  late=.62, st=10*60+25, hrs=8.1, rep=.86, on=.70, acc=.92),
 "skipper": dict(att=.95,  late=.10, st=9*60+50, hrs=8.4, rep=.52, on=.82, acc=.95),
 "overdue": dict(att=.93,  late=.20, st=10*60, hrs=8.2, rep=.84, on=.45, acc=.90),
 "weak":    dict(att=.80,  late=.35, st=10*60+10, hrs=7.6, rep=.66, on=.60, acc=.88),
 "awol":    dict(att=.90,  late=.18, st=9*60+55, hrs=8.3, rep=.85, on=.75, acc=.93),
 "new":     dict(att=.97,  late=.06, st=9*60+40, hrs=8.6, rep=.96, on=.82, acc=.97),
}
EMP = [
 ("RPS002","Kavya Reddy","HR & Operations Manager","HR & Admin","2025-01-06",45000,"good"),
 ("RPS003","Arjun Mehta","Performance Marketing Lead","Performance Marketing","2024-09-02",85000,"star"),
 ("RPS004","Sneha Pillai","Performance Marketer","Performance Marketing","2025-06-02",50000,"good"),
 ("RPS005","Divya Nair","Social Media Manager","Social Media","2024-11-04",42000,"star"),
 ("RPS006","Rahul Varma","Social Media Manager","Social Media","2025-03-03",40000,"late"),
 ("RPS007","Ananya Iyer","Social Media Executive","Social Media","2026-09-08",28000,"new"),
 ("RPS008","Karthik Sharma","Script Writer","Content","2025-02-10",38000,"skipper"),
 ("RPS009","Meghana Rao","Script Writer","Content","2025-08-18",36000,"avg"),
 ("RPS010","Vikram Naidu","Senior Video Editor","Post-production","2024-07-15",60000,"star"),
 ("RPS011","Imran Shaikh","Video Editor","Post-production","2025-05-05",40000,"overdue"),
 ("RPS012","Pooja Kulkarni","Video Editor","Post-production","2025-10-06",38000,"avg"),
 ("RPS013","Suresh Babu","Videographer","Production","2024-12-02",42000,"good"),
 ("RPS014","Nikhil Joshi","Cinematographer","Production","2024-08-19",65000,"good"),
 ("RPS015","Farah Siddiqui","Photographer","Production","2025-04-07",38000,"avg"),
 ("RPS016","Ravi Kiran","Videographer","Production","2025-07-14",36000,"awol"),
 ("RPS017","Lakshmi Prasanna","Telepresenter","Media & News","2025-01-20",45000,"good"),
 ("RPS018","Aditya Rao","Telepresenter","Media & News","2025-09-01",42000,"avg"),
 ("RPS019","Harini Venkat","News Reporter","Media & News","2025-02-03",38000,"good"),
 ("RPS020","Sameer Ali","News Reporter","Media & News","2025-06-16",36000,"late"),
 ("RPS021","Prakash Gowda","Real Estate Agent","Real Estate","2025-03-17",25000,"good"),
 ("RPS022","Swathi Reddy","Real Estate Agent","Real Estate","2025-11-03",25000,"avg"),
 ("RPS023","Ramya Shetty","Telecaller","Sales","2025-05-19",18000,"good"),
 ("RPS024","Manoj Patil","Telecaller","Sales","2025-12-01",18000,"weak"),
 ("RPS025","Deepak Chandra","Sales Executive","Sales","2025-04-21",30000,"avg"),
 ("RPS026","Nandini Murthy","Sales Executive","Sales","2025-01-13",32000,"good"),
 ("RPS027","Rohan Desai","Business Development Manager","Business Development","2024-10-07",80000,"star"),
 ("RPS028","Tanvi Bhat","Business Development Executive","Business Development","2026-10-01",35000,"new"),
]
ON_SHIFT_NOW = {"RPS010", "RPS014"}  # still working at 21:20 tonight
BG = ["O+","B+","A+","O+","AB+","B+","O-","A-","B-"]
CLIENTS = ["Jain Marbles","Vibos","Sea Salt","O2 Automotive","Project N","Thermalon","RPS Instagram","Agri Con"]
PROPS = ["Sarjapur 3BHK villa","Whitefield office floor","Hebbal lake-view flat","Yelahanka plots","Koramangala studio","Hennur row houses"]
PROS = ["Brew Theory Cafe","Namma Fitness","Kaveri Silks","UrbanNest Interiors","GreenLeaf Organics","Skyline Builders","Vizag Seafoods","Tiffin Tales"]
STORIES = ["Namma Metro yellow line","Bengaluru Tech Summit","Mysuru Dasara","Lalbagh flower show","Outer Ring Road traffic","Kadalekai Parishe fair","monsoon flooding in Bellandur"]
LEADS = ["Mr. Srinivas","Mrs. Latha","Mr. Faizal","Ms. Preethi","Mr. Gopal","Mrs. Anitha","Mr. Varun"]

emp = {e[0]: dict(id=e[0], name=e[1], role=e[2], dept=e[3], joined=e[4], gross=e[5], p=P[e[6]], kind=e[6]) for e in EMP}
by_dept = {}
for e in emp.values(): by_dept.setdefault(e["dept"], []).append(e["id"])
def pick(dept, when):
    c = [i for i in by_dept.get(dept, []) if emp[i]["joined"] <= ds(when)]
    return R.choice(c) if c else None
def role_ids(word, when):
    c = [i for i in emp if word in emp[i]["role"] and emp[i]["joined"] <= ds(when)]
    return R.choice(c) if c else None

# ---------- leaves (planned) ----------
leaves = {i: [] for i in emp}
def add_leave(i, t, a, b, r): leaves[i].append(dict(t=t, f=a, to=b, r=r))
add_leave("RPS012","Sick","2026-09-15","2026-09-19","Viral fever, doctor advised rest")
add_leave("RPS003","Earned","2026-08-24","2026-08-26","Family function in Hyderabad")
add_leave("RPS005","Personal","2026-10-09","2026-10-10","Sister's engagement")
add_leave("RPS014","Earned","2026-09-28","2026-09-30","Trip to Coorg (planned)")
add_leave("RPS024","Sick","2026-08-11","2026-08-12","Stomach infection")
add_leave("RPS024","Personal","2026-10-13","2026-10-13","Bank and RTO work")
add_leave("RPS019","Sick","2026-10-06","2026-10-06","Migraine")
add_leave("RPS021","Earned","2026-09-07","2026-09-09","Native place visit, Mandya")
add_leave("RPS009","Personal","2026-08-31","2026-08-31","House shifting")
add_leave("RPS017","Sick","2026-09-22","2026-09-23","Throat infection, can't do voice work")
add_leave("RPS025","Earned","2026-10-21","2026-10-23","Diwali shopping trip to Chennai")
add_leave("RPS026","Personal","2026-08-21","2026-08-21","Child's school annual day")
add_leave("RPS002","Earned","2026-09-02","2026-09-03","Personal work")
add_leave("RPS020","Sick","2026-10-15","2026-10-16","Fever")
add_leave("RPS008","Other","2026-08-07","2026-08-07","Writing workshop (company approved)")
leave_days = {i: set() for i in emp}
for i, L in leaves.items():
    for l in L:
        for d in daterange(date.fromisoformat(l["f"]), date.fromisoformat(l["to"])): leave_days[i].add(ds(d))

# ---------- attendance ----------
att = {i: {} for i in emp}
absent_nl = {i: set() for i in emp}
for i, e in emp.items():
    p = e["p"]; jd = date.fromisoformat(e["joined"])
    for d in daterange(max(START, jd), TODAY):
        k = ds(d)
        if not is_wd(d):
            if d.weekday() == 6 and e["dept"] in ("Production","Media & News") and R.random() < .12:
                pass  # occasional Sunday shoot
            else:
                continue
        elif k in leave_days[i]:
            continue
        elif R.random() > p["att"]:
            absent_nl[i].add(k); continue
        sat = d.weekday() == 5
        late = R.random() < p["late"]
        st = p["st"] + (R.randint(25, 70) if late and p["st"] < 615 else R.randint(-15, 20))
        if late: st = max(st, 10*60+17 + R.randint(0, 40))
        else: st = min(st, 10*60+12)
        dur = (p["hrs"] - (1.2 if sat else 0)) * 60 + R.randint(-50, 55)
        if d == TODAY and i in ON_SHIFT_NOW:
            sessions = [{"i": iso(d, st)}]
        else:
            end = st + dur
            if d == TODAY and end > NOW_MIN - 20: end = NOW_MIN - R.randint(25, 140)
            if R.random() < .45:
                b1 = st + R.randint(210, 270); b2 = b1 + R.randint(30, 55)
                sessions = [{"i": iso(d, st), "o": iso(d, b1)}, {"i": iso(d, b2), "o": iso(d, end + (b2 - b1))}]
            else:
                sessions = [{"i": iso(d, st), "o": iso(d, end)}]
        att[i][k] = {"s": sessions}

att["RPS001"] = {}
def present(i, d): return i == "RPS001" and is_wd(d) or ds(d) in att[i]

# ---------- tasks ----------
tasks = []
def T(frm, to, title, proj, created, due_wd, pri="Normal", det=""):
    if not frm or not to or frm == to: return
    tasks.append(dict(frm=frm, to=to, title=title, proj=proj, created=created, due_wd=due_wd, pri=pri, det=det))
TEMPL = [
 ("Social Media", lambda d: [("Script Writer", f"Script for {c} reel", c, "45-60s reel, hook in first 3 seconds, Kannada + English mix.") for c in [R.choice(CLIENTS)]][0], (2,4)),
 ("Social Media", lambda d: [("Editor", f"Edit {c} reel v1", c, "Raw files are in the shared drive folder for this week. Add captions and the brand end card.") for c in [R.choice(CLIENTS)]][0], (2,4)),
 ("Social Media", lambda d: [("Photographer", f"Product shots for {c}", c, "Flat-lays + 5 lifestyle frames for the carousel.") for c in [R.choice(["Sea Salt","Project N","Jain Marbles","Vibos"])]][0], (3,5)),
 ("Social Media", lambda d: [("Script Writer", f"Captions for {c} carousel", c, "8 slides, keep each caption under 20 words.") for c in [R.choice(CLIENTS)]][0], (1,2)),
 ("Performance Marketing", lambda d: [("Social Media Manager", f"Ad creatives for {c} campaign", c, "3 static + 2 story formats for the next Meta flight.") for c in [R.choice(["Jain Marbles","Sea Salt","O2 Automotive","Vibos"])]][0], (2,4)),
 ("Performance Marketing", lambda d: [("Editor", f"15s cut-down for {c} ads", c, "Vertical 9:16 and square 1:1 versions, no music licensing issues.") for c in [R.choice(["Jain Marbles","O2 Automotive","Sea Salt"])]][0], (2,3)),
 ("Content", lambda d: [("Cinematographer", f"Shot list review for {c}", c, "Check if the lighting plan works for the indoor scenes.") for c in [R.choice(CLIENTS)]][0], (1,3)),
 ("Content", lambda d: [("Videographer", f"Re-shoot B-roll for {c}", c, "Need 6-8 extra B-roll shots of the space in daylight.") for c in [R.choice(["Vibos","Jain Marbles","Sea Salt"])]][0], (2,4)),
 ("Post-production", lambda d: [("Script Writer", f"Final VO script for {c}", c, "Voice-over needs to fit 52 seconds exactly.") for c in [R.choice(CLIENTS)]][0], (1,2)),
 ("Post-production", lambda d: [("Videographer", f"Extra footage for {c} edit", c, "Missing wide shots for the opening sequence.") for c in [R.choice(CLIENTS)]][0], (2,3)),
 ("Media & News", lambda d: [("Cinematographer", f"Cover {s}", "News desk", "Two-camera setup, interviews with 3 people on the spot.") for s in [R.choice(STORIES)]][0], (1,2)),
 ("Media & News", lambda d: [("Editor", f"Package edit: {s}", "News desk", "2-minute package with lower thirds and anchor intro.") for s in [R.choice(STORIES)]][0], (1,2)),
 ("Media & News", lambda d: [("Script Writer", f"Anchor script: {s}", "News desk", "Telepresenter intro + outro, conversational tone.") for s in [R.choice(STORIES)]][0], (1,2)),
 ("Real Estate", lambda d: [("Videographer", f"Walkthrough video – {p}", "Real estate listings", "Gimbal walkthrough, 2 minutes, morning light.") for p in [R.choice(PROPS)]][0], (2,4)),
 ("Real Estate", lambda d: [("Photographer", f"Listing photos – {p}", "Real estate listings", "15 photos including exterior and amenities.") for p in [R.choice(PROPS)]][0], (2,3)),
 ("Sales", lambda d: [("Real Estate Agent", f"Site visit for {l} – {p}", "Real estate listings", "Lead came from the Instagram ad, budget fits.") for l, p in [(R.choice(LEADS), R.choice(PROPS))]][0], (1,3)),
 ("Sales", lambda d: [("Sales Executive", f"Follow up warm lead – {c}", "New business", "Called twice, interested in a 3-month social media package.") for c in [R.choice(PROS)]][0], (1,3)),
 ("Sales", lambda d: [("Business Development", f"Proposal for {c}", "New business", "Social media + website package, they asked for pricing by Friday.") for c in [R.choice(PROS)]][0], (2,4)),
 ("Business Development", lambda d: [("Performance Marketing Lead", f"Media plan for {c} pitch", "New business", "Monthly ad budget around ₹1.5 lakh, Bengaluru-only targeting.") for c in [R.choice(PROS)]][0], (2,4)),
 ("Business Development", lambda d: [("Social Media Manager", f"Sample content calendar for {c}", "New business", "2-week sample calendar to attach with the proposal.") for c in [R.choice(PROS)]][0], (2,3)),
 ("Business Development", lambda d: [("Telecaller", f"Call list: {n} event leads", "Agri Con leads", "Call everyone from the visiting cards sheet and mark interest level.") for n in [R.choice(["Agri Con","BHIVE","Tech Summit"])]][0], (2,4)),
 ("HR & Admin", lambda d: [("*", R.choice(["Submit documents for group insurance","Update emergency contact details","Sign the revised leave policy","Complete POSH awareness module"]), "HR", "Please finish this by the due date.")][0], (3,6)),
]
def resolve(word, when, frm):
    if word == "*": c = [i for i in emp if emp[i]["joined"] <= ds(when) and i != frm]; return R.choice(c) if c else None
    if word == "Business Development": return pick("Business Development", when)
    return role_ids(word, when)

for d in daterange(START, TODAY):
    if not is_wd(d): continue
    n = R.randint(3, 6) if d.weekday() < 5 else R.randint(1, 3)
    for _ in range(n):
        dept, f, rng = R.choice(TEMPL)
        frm = pick(dept, d)
        if not frm or not present(frm, d): continue
        role, title, proj, det = f(d)
        to = resolve(role, d, frm)
        pri = R.choices(["Normal","High","Urgent","Low"], [70, 18, 6, 6])[0]
        T(frm, to, title, proj, d, R.randint(*rng), pri, det)
# founder asks the leads for a few things
for d, to, title in [(date(2026,8,3),"RPS003","Q3 ad spend review deck"),(date(2026,8,10),"RPS027","Pitch for Skyline Builders"),(date(2026,9,1),"RPS005","RPS Instagram growth plan for Q4"),
                     (date(2026,9,21),"RPS010","Showreel 2026 cut"),(date(2026,10,5),"RPS002","Diwali bonus list"),(date(2026,10,19),"RPS027","Thermalon South India pitch follow-up"),(date(2026,10,22),"RPS011","Vibos office reel final export")]:
    T("RPS001", to, title, "Founder's desk", d, 3, "High", "Need this before our Monday review.")

def first_in_min(i, d):
    r = att[i].get(ds(d))
    if not r: return None
    t = datetime.strptime(r["s"][0]["i"], "%Y-%m-%dT%H:%M:%S.000Z") + timedelta(hours=5, minutes=30)
    return t.hour*60 + t.minute
def next_present(i, d, limit=12):
    for _ in range(limit):
        if present(i, d): return d
        d += timedelta(days=1)
    return None
def at_on(i, d, lo=0, hi=None):
    """a time on day d when person i is at work."""
    s = first_in_min(i, d) or 10*60
    hi = hi or s + 7*60
    return iso(d, R.randint(s + 20 + lo, max(s + 30 + lo, hi)))

NOTES_UPD = ["First draft is ready, sharing for a quick look.","Halfway done, waiting on the client's logo files.","Rough cut done, colour grading pending.","Shot 60% of the list, rest tomorrow morning.","Called the client, they want a warmer tone.","Uploaded v1 to the shared folder.","Blocked on approvals from the client side."]
NOTES_DONE = ["Delivered, files are in the shared folder.","Done and sent for client approval.","Final version uploaded with both aspect ratios.","Completed, client approved on the first round.","Done. Added two extra options as alternates.",""]
NOTES_FU = ["Any update on this? Client is asking.","Reminder: this is due today.","Need this by EOD please, the post is scheduled.","Can you prioritise this? It's blocking the campaign."]
NOTES_DEC = ["I'm fully booked on the Jain Marbles shoot this week.","Not my area, please check with the editor.","On leave on the due date.","Already covered in the last batch."]

out_tasks = []
for n, t in enumerate(tasks):
    frm, to = t["frm"], t["to"]; c = t["created"]; ep = emp.get(to, {"p": P["good"]})["p"]
    cmin = (first_in_min(frm, c) or 10*60) + R.randint(15, 300)
    created_at = iso(c, min(cmin, 19*60))
    due = add_wd(c, t["due_wd"])
    tid = "d" + format(int(datetime(c.year, c.month, c.day).timestamp()) // 60 + n, "x") + format(n, "03x")
    log = [dict(by=frm, at=created_at, a="Requested", t="")]
    st = "requested"; up = created_at
    acc_day = next_present(to, c if R.random() < .6 else c + timedelta(days=1))
    if acc_day and acc_day <= TODAY and not (c >= TODAY - timedelta(days=1) and R.random() < .55):
        a_at = at_on(to, acc_day)
        if a_at < created_at: a_at = created_at[:-5] + "999Z"
        if R.random() > ep["acc"]:
            st = "declined"; log.append(dict(by=to, at=a_at, a="Declined", t=R.choice(NOTES_DEC))); up = a_at
        else:
            st = "accepted"; log.append(dict(by=to, at=a_at, a="Accepted", t="")); up = a_at
            if R.random() < .55:
                s_day = next_present(to, acc_day) or acc_day
                if s_day <= TODAY:
                    log.append(dict(by=to, at=max(a_at, at_on(to, s_day, 10)), a="Started work", t="")); st = "progress"
            ontime = R.random() < ep["on"]
            span = max(0, (due - acc_day).days)
            dd = acc_day + timedelta(days=R.randint(0, span)) if ontime else due + timedelta(days=R.randint(1, 5))
            dd = next_present(to, dd) or dd
            if (c >= TODAY - timedelta(days=9) and R.random() < .45) or (emp.get(to, {}).get("kind") == "overdue" and R.random() < .18) or (emp.get(to, {}).get("kind") == "weak" and R.random() < .12):
                dd = TODAY + timedelta(days=3)  # still being worked on
            if R.random() < .35:
                mid = acc_day + timedelta(days=max(0, (dd - acc_day).days // 2))
                if next_present(to, mid) and next_present(to, mid) <= min(dd, TODAY):
                    m2 = next_present(to, mid); log.append(dict(by=to, at=at_on(to, m2, 60), a="Update", t=R.choice(NOTES_UPD)))
            if not ontime:
                fu = due if due <= TODAY else None
                if fu and present(frm, fu): log.append(dict(by=frm, at=at_on(frm, fu, 120), a="Follow-up", t=R.choice(NOTES_FU)))
            if dd <= TODAY and (dd < TODAY or R.random() < .5) and present(to, dd):
                log.append(dict(by=to, at=at_on(to, dd, 90), a="Marked done", t=R.choice(NOTES_DONE))); st = "done"
            if st != "done" and R.random() < .03 and due < TODAY:
                log.append(dict(by=frm, at=at_on(frm, next_present(frm, due) or due, 30) if next_present(frm, due) else iso(due, 16*60), a="Withdrawn", t="Client dropped this, no longer needed.")); st = "withdrawn"
    log.sort(key=lambda x: x["at"])
    log = [l for l in log if l["at"] <= iso(TODAY, NOW_MIN)]
    up = log[-1]["at"]
    out_tasks.append(dict(id=tid, **{"from": frm}, to=to, title=t["title"], det=t["det"], proj=t["proj"], due=ds(due), pri=t["pri"], st=st, at=created_at, up=up, log=log, demo=True))

# ---------- work reports ----------
OPEN = ["Today was focused on {focus}.","Started the day with {focus}.","Main work today: {focus}.","Spent most of the day on {focus}."]
FOCUS = {
 "HR & Admin": ["payroll inputs and attendance checks","onboarding paperwork for new joiners","group insurance enrolment","leave records and policy updates"],
 "Performance Marketing": ["Meta and Google ad performance","campaign optimisation and budget pacing","audience testing for new creatives","weekly ROAS reporting"],
 "Social Media": ["content calendars and posting","community replies and stories","creative briefs for the design team","reel planning and trend research"],
 "Content": ["scripts and voice-over drafts","caption writing","hooks and storyboard notes","rewrites based on client feedback"],
 "Post-production": ["editing reels and colour correction","sound design and subtitles","exports in multiple aspect ratios","revisions from client feedback"],
 "Production": ["shoots and equipment prep","lighting setup and shot lists","backing up footage and logging cards","location recce and planning"],
 "Media & News": ["news coverage and interviews","anchor links and piece-to-camera","story research and fact checks","studio recording"],
 "Real Estate": ["site visits with leads","listing updates and photos coordination","follow-up calls with buyers","negotiations and documentation"],
 "Sales": ["calling leads and qualifying interest","follow-ups on warm leads","updating the sales tracker","demo calls and proposals"],
 "Business Development": ["pitches and proposal drafts","partner meetings","pipeline review","event follow-ups"],
}
MID = {
 "HR & Admin": ["Cross-checked punch-in data against the leave sheet and fixed two mismatches.","Followed up with the insurer about pending e-cards for new members.","Prepared the joining kit and ID details for the next joiner."],
 "Performance Marketing": ["Paused two ad sets with high CPL and moved budget to the best performing creative.","CTR improved after switching to the new hook; cost per lead dropped by about 12 percent.","Set up a lookalike audience from last month's converters."],
 "Social Media": ["Scheduled posts for the next three days and replied to all DMs and comments.","Briefed the editor on the trending audio format we want to try.","Reviewed analytics; reels are getting almost twice the reach of carousels this week."],
 "Content": ["Wrote two script options with different hooks so the client can choose.","Tightened the voice-over to fit the timing the editor shared.","Researched references and shared a mood board with the team."],
 "Post-production": ["Finished the rough cut, added subtitles and synced the voice-over.","Colour graded the indoor shots to match the brand palette.","Exported vertical and square versions and uploaded them to the shared drive."],
 "Production": ["Checked batteries, cards and lenses before the shoot and logged all footage after.","Shot the B-roll list and a few extra angles for the edit.","Did a short recce of the location and noted power points and light direction."],
 "Media & News": ["Recorded two interviews and the piece-to-camera for the story.","Verified the facts with two sources before sending the script to the desk.","Recorded anchor links in the studio, three takes each."],
 "Real Estate": ["Took two families around the property and shared the price sheet.","Updated the listing with new photos and the revised price.","Coordinated with the owner on the possession date."],
 "Sales": ["Made around 60 calls, 9 were interested and 3 asked for a callback.","Sent proposals to two warm leads and logged everything in the tracker.","Followed up on last week's leads; one asked for a meeting next week."],
 "Business Development": ["Met the prospect's marketing head and walked them through our case studies.","Drafted the proposal with pricing for the three-month package.","Reviewed the pipeline and prioritised the five hottest deals."],
}
END = ["Pending: {pend}. Plan for tomorrow is to close it out.","Still pending: {pend}. Will pick it up first thing tomorrow.","Tomorrow I will continue with {pend} and share an update by noon.","No blockers right now. Next up is {pend}."]
def report(i, d, tday):
    e = emp[i]; dep = e["dept"]
    acts = [l for t in out_tasks for l in t["log"] if l["by"] == i and l["at"][:10] == ds(d) and l["a"] in ("Marked done","Accepted","Update","Started work")]
    tnames = {}
    for t in out_tasks:
        for l in t["log"]:
            if l["by"] == i and l["at"][:10] == ds(d): tnames[t["title"]] = l["a"]
    parts = [R.choice(OPEN).format(focus=R.choice(FOCUS[dep]))]
    for tt, a in list(tnames.items())[:3]:
        parts.append({"Marked done":f"Completed \"{tt}\" and shared it with the team.","Accepted":f"Accepted the request for \"{tt}\" and planned the work.","Update":f"Made progress on \"{tt}\" and posted an update.","Started work":f"Started working on \"{tt}\".","Requested":f"Asked a colleague for help on \"{tt}\"."}.get(a, f"Worked on \"{tt}\"."))
    mids = R.sample(MID[dep], 2)
    parts += mids
    open_t = [t["title"] for t in out_tasks if t["to"] == i and t["st"] in ("accepted","progress") and t["at"][:10] <= ds(d)]
    parts.append(R.choice(END).format(pend=("\"" + R.choice(open_t) + "\"") if open_t else R.choice(FOCUS[dep])))
    txt = " ".join(parts)
    GEN = ["Attended the morning stand-up and aligned on priorities with the team.","Cleared pending emails and WhatsApp messages from clients.","Updated the shared tracker so everyone can see where things stand.","Had a quick sync with my reporting manager about this week's deadlines.","Organised files in the shared drive with proper names and dates."]
    pool = [x for x in MID[dep] + GEN if x not in txt]; R.shuffle(pool)
    while len(re.findall(r"\S+", txt)) < 55 and pool: txt += " " + pool.pop()
    return txt

data = {}
for i, e in emp.items():
    p = e["p"]; A = att[i]; rep = {}
    for k in sorted(A):
        d = date.fromisoformat(k); s = A[k]["s"]
        if "o" not in s[-1]: continue  # still on shift
        if R.random() > p["rep"]: continue
        txt = report(i, d, k)
        out_t = datetime.strptime(s[-1]["o"], "%Y-%m-%dT%H:%M:%S.000Z") - timedelta(minutes=R.randint(1, 6))
        rep[k] = dict(t=txt, w=len([w for w in re.findall(r"\S+", txt) if re.search(r"[A-Za-z0-9]", w)]), at=out_t.strftime("%Y-%m-%dT%H:%M:%S.000Z"), n=1)
    cur = ds(TODAY) if ds(TODAY) in A and "o" not in A[ds(TODAY)]["s"][-1] else None
    last = None
    for k in sorted(A, reverse=True):
        ss = [x for x in A[k]["s"] if "o" in x]
        if ss: last = dict(i=ss[-1]["i"], o=ss[-1]["o"]); break
    D = dict(att=A, leaves=sorted(leaves[i], key=lambda l: l["f"], reverse=True), ins={}, rep=rep)
    if cur: D["cur"] = cur
    if last: D["last"] = last
    data[i] = D

# ---------- payslips (Aug, Sep) ----------
def month_wd(y, m):
    d = date(y, m, 1); n = 0
    while d.month == m:
        if d.weekday() != 6: n += 1
        d += timedelta(days=1)
    return n
pays = {}
for i, e in emp.items():
    P_ = {}
    for (y, m, gen) in [(2026, 8, "02 Sep 2026"), (2026, 9, "01 Oct 2026")]:
        first = date(y, m, 1)
        if date.fromisoformat(e["joined"]) > date(y, m, 28): continue
        wd = month_wd(y, m)
        jd = date.fromisoformat(e["joined"])
        notyet = 0
        if jd > first:
            d = first
            while d < jd:
                if d.weekday() != 6: notyet += 1
                d += timedelta(days=1)
        lop_days = notyet + len([k for k in absent_nl[i] if k.startswith(f"{y}-{m:02d}")])
        g = e["gross"]; b = round(g * .5); hra = round(b * .4)
        bonus = 0
        if e["dept"] in ("Real Estate", "Sales"): bonus = R.choice([0, 2500, 4000, 6000, 8500])
        if e["kind"] == "star": bonus = max(bonus, R.choice([3000, 5000]))
        s = dict(basic=b, hra=hra, allow=g - b - hra, bonus=bonus, pf=min(1800, round(b * .12)), pt=200 if g >= 25000 else 0,
                 tds=3500 if g >= 80000 else 1200 if g >= 60000 else 0, oth=0, wd=wd, pd=wd - lop_days, gen=gen)
        fix = b + hra + (g - b - hra); s["lop"] = round(fix / wd * lop_days) if wd else 0
        P_[f"{y}-{m:02d}"] = s
    if P_: pays[i] = P_

# ---------- accounts ----------
NOM = [("Spouse",), ("Mother",), ("Father",)]
users = {"RPS001": dict(name="Bruce", role="Founder & CEO", dept="Leadership", company="Rock Papers Scissors", phone="", email="info@rockpapersscissors.in",
          bg="", addr="Rock Papers Scissors, Bengaluru", ins={}, joined="2024-06-01T00:00:00", pw=h(os.environ["FOUNDER_PASSWORD"]), owner=True,
          hist=[dict(at="2026-10-24T15:55:00.000Z", a="Founder account created")])}
for n, (i, e) in enumerate(emp.items()):
    first = e["name"].split()[0].lower(); last = e["name"].split()[-1].lower()
    ins = {} if i == "RPS028" else dict(prov="Group health insurer (demo)", no=f"GHP-2026-{4100+n:05d}", type="Family floater" if n % 3 == 0 else "Group health",
           sum="500000" if n % 3 == 0 else "300000", **{"from": "2026-04-01"}, till="2027-03-31", nom=R.choice(["Spouse","Mother","Father"]), rel="", mem="Self + spouse + 2 children" if n % 3 == 0 else "Self",
           help="HR desk · ext 204")
    if ins: ins["nom"], ins["rel"] = f"{R.choice(['Suma','Ravi','Meena','Prasad','Lakshmi','Anil'])} {e['name'].split()[-1]}", ins["nom"]
    users[i] = dict(name=e["name"], role=e["role"], dept=e["dept"], company="Rock Papers Scissors", phone=f"+91 90000 {1000+n*37:05d}"[:16],
                    email=f"{first}.{last}@example.com", bg=BG[n % len(BG)], addr=R.choice(["Indiranagar","HSR Layout","Jayanagar","Whitefield","Marathahalli","BTM Layout","Malleshwaram","Electronic City"]) + ", Bengaluru",
                    ins=ins, joined=e["joined"] + "T00:00:00", pw=h("rps12345"), demo=True,
                    hist=[dict(at="2026-10-24T15:55:00.000Z", a="Demo account created for testing")])

# ---------- write ----------
def did(k): return re.sub(r"[^A-Za-z0-9_\-.:@+]", lambda m: "~%04x" % ord(m.group(0)), k)
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT): os.remove(os.path.join(OUT, f))
writes = []
def doc(col, docid, body):
    fn = os.path.join(OUT, f"{col}__{docid}.json"); json.dump(body, open(fn, "w"), ensure_ascii=False)
    writes.append(dict(op="set", collection=col, doc_id=docid, file_path=fn))
for i, u in users.items(): doc("accounts", "u_" + did(i), dict(k="user", id=i, v=u))
for i, D in data.items(): doc("portal", "k_" + did("ems_d_" + i), dict(k="ems_d_" + i, v=D))
for i, Pp in pays.items(): doc("hr", "k_" + did("ems_pay_" + i), dict(k="ems_pay_" + i, v=Pp))
for t in out_tasks: doc("portal", "k_" + did("ems_t_" + t["id"]), dict(k="ems_t_" + t["id"], v=t))
json.dump(writes, open(os.path.join(OUT, "_writes.json"), "w"))
# local test seed (localStorage keys)
ls = {"ems_users": users}
for i, D in data.items(): ls["ems_d_" + i] = D
for i, Pp in pays.items(): ls["ems_pay_" + i] = Pp
for t in out_tasks: ls["ems_t_" + t["id"]] = t
json.dump(ls, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "seed_local.json"), "w"), ensure_ascii=False)
from collections import Counter
print("employees", len(emp), "tasks", len(out_tasks), Counter(t["st"] for t in out_tasks))
print("reports", sum(len(d["rep"]) for d in data.values()), "att days", sum(len(d["att"]) for d in data.values()))
print("docs", len(writes), "max doc KB", max(os.path.getsize(w["file_path"]) for w in writes) // 1024)
print("on shift", [i for i, d in data.items() if d.get("cur")], "absent w/o leave", {i: len(v) for i, v in absent_nl.items() if v})
