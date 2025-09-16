const allRankingsData = {
  "1": {
    title: "Week 1 Report: The Scorch Trials",
    matchup: {
      team1Name: "#3 Bend The Knee",
      team1Record: "(2-0-0)",
      team1Blurb: "A kingdom built on the legs of a rejuvenated Derrick Henry. Can this old-school dynasty survive against the new-age firepower?",
      team2Name: "#1 FreeGucci",
      team2Record: "(2-0-0)",
      team2Blurb: "The league's final boss. Fresh off a Week 1 performance so dominant it should be illegal. Can lightning strike twice?",
      verdict: "This is the heavyweight championship of Week 2. It’s strength vs. strength, ego vs. ego. We’re giving the slight edge to the team that showed a higher, more explosive ceiling. Bend The Knee will put up a fight, but FreeGucci's firepower is too much. <span class='font-bold'>FreeGucci by 3.</span>"
    },
    superlatives: {
      boom: { team: "FreeGucci", reason: "For treating his projection like a speed bump on the way to a blowout." },
      bust: { team: "INDIAN JONES", reason: "For missing his projection so badly, we had to check if he submitted a lineup at all." },
      manager: { team: "INDIAN JONES", reason: "Leaving two 25+ point QBs on the bench is a fireable offense. Unforgivable." },
      fraud: { team: "Bullish", reason: "For winning while his team performed like it was actively trying to lose. An absolute fluke." }
    },
    rankings: [
      { rank: 1, teamName: "FreeGucci", manager: "Nishil naik", record: "2-0-0", tagline: "The League's Final Boss", blurb: "Let's be clear: this wasn't just a win, it was a declaration of war. Annihilating your projection by <span class='text-success-bright font-bold'>+18.50</span> points is the fantasy equivalent of planting your flag on the smoking ruins of your opponent's season. With an army of studs waiting on the bench (Rice, Addison), this team isn't just the one to beat; it's the one to fear. Enjoy the view from the top; the fall will be spectacular.", stud: "Lamar Jackson (29.36 pts), who played like a man possessed.", dud: "Calvin Ridley (4.70 pts), who was thankfully a passenger in this beatdown.", score: { actual: 141.14, projected: 122.64 }},
      { rank: 2, teamName: "Leo the Cleo", manager: "Chris", record: "2-0-0", tagline: "The Silent Assassin", blurb: "The highest scorer of the week, and he made it look easy. While FreeGucci was dropping bombs, Leo the Cleo was quietly and efficiently dismantling his opponent with a <span class='text-success-bright font-bold'>+9.70</span> performance over projection. The fact that his bench was a wasteland means he started the perfect lineup. That’s not luck; that’s terrifyingly good management.", stud: "Bijan Robinson (22.40 pts), looking every bit the part of a league-winner.", dud: "Terry McLaurin (3.70 pts), who apparently decided to take the week off.", score: { actual: 143.32, projected: 133.62 }},
      { rank: 3, teamName: "Bend The Knee", manager: "Darrius M", record: "2-0-0", tagline: "The Titan", blurb: "This team is a throwback powerhouse built on the back of one monster: Derrick Henry. It’s a simple, brutal strategy: run the ball down your opponent’s throat until they beg for mercy. While Nico Collins laid an egg, it didn't matter when Henry single-handedly outscored him by 26. This team is a force of nature, and everyone else is just standing in the way of the storm.", stud: "Derrick Henry (30.70 pts), who drank from the fountain of youth.", dud: "Nico Collins (4.00 pts), a certified milk-carton performance.", score: { actual: 129.80, projected: 124.33 }},
      { rank: 4, teamName: "Mac Daddy", manager: "Maclane", record: "1-1-0", tagline: "The Ferrari with Flat Tires", blurb: "This team has the names, the hype, and the championship ceiling. But in Week 1, it performed like a luxury car running on fumes, sputtering to a <span class='text-danger-bright font-bold'>-7.79</span> point underperformance. Having Justin Jefferson is great, but it doesn't mean much when the rest of your roster plays like they've never seen a football before. This team is all sizzle, no steak... for now.", stud: "Travis Etienne Jr. (18.10 pts), the only one who showed up.", dud: "Kenneth Walker III (3.90 pts), a truly pathetic output.", score: { actual: 128.20, projected: 125.99 }},
      { rank: 5, teamName: "The Injured Reserved", manager: "Greg", record: "1-1-0", tagline: "Mr. Perfectly Mid", blurb: "This team is an art form of average. Scoring almost exactly what you were projected to (<span class='text-gray-600 font-bold'>-0.31</span> difference) is both impressive and soul-crushingly boring. He didn't boom, he didn't bust. He just showed up, did his job, and got steamrolled by a team that actually has a pulse. A playoff threat destined for a 7-7 record and a first-round exit.", stud: "Davante Adams (12.70 pts), the lone bright spot.", dud: "The schedule-maker, who should be fired immediately.", score: { actual: 128.70, projected: 129.01 }},
      { rank: 6, teamName: "Good Will Hunting", manager: "Will", record: "0-2-0", tagline: "Superman and the Civilians", blurb: "This team is Josh Allen and a group of terrified bystanders he has to save every week. He put up a heroic 38.76 points, and his team *still* managed to underperform by <span class='text-danger-bright font-bold'>-12.57</span> points and lose. This isn't a football team; it's a superhero movie where the hero is about to get tired of saving everyone.", panicMeter: { level: "CONCERNED", color: "text-yellow-500 bg-yellow-100" }, score: { actual: 112.00, projected: 124.57 }},
      { rank: 7, teamName: "A dad", manager: "Barrett Davis", record: "2-0-0", tagline: "Winning By Accident", blurb: "This team won a boxing match because its opponent tripped over their own feet on the way to the ring. Getting a win while your first-round pick, Ja'Marr Chase, drops a 3.60-point dud is not a sign of skill; it's a sign that the fantasy gods have a sick sense of humor. This 2-0-0 record is a mirage in the desert of mediocrity.", panicMeter: { level: "CALM (BUT WATCHING)", color: "text-green-500 bg-green-100" }, score: { actual: 116.78, projected: 120.04 }},
      { rank: 8, teamName: "Shut Up", manager: "Neil", record: "0-2-0", tagline: "The Ghost", blurb: "This team is the vanilla ice cream of the league: bland, forgettable, and melting fast. Underperforming by almost 13 points is not just a loss; it's a complete lack of presence. This roster needs a spark before it fades into total irrelevance.", panicMeter: { level: "ELEVATED", color: "text-yellow-500 bg-yellow-100" }, score: { actual: 110.54, projected: 123.15 }},
      { rank: 9, teamName: "Miley Hannah Montana", manager: "Greg", record: "1-1-0", tagline: "FRAUD WATCH", blurb: "Let's be crystal clear: this team is not good. It won by feasting on the carcass of the league's worst team. That's it. His own roster was a dumpster fire that underperformed by 11 points. This win is a lie, and the truth will come out as soon as he plays a team with a pulse.", panicMeter: { level: "VIBING (FOR NOW)", color: "text-green-500 bg-green-100" }, score: { actual: 113.84, projected: 124.74 }},
      { rank: 10, teamName: "Bullish", manager: "mohsin", record: "1-1-0", tagline: "Stumbling to Victory", blurb: "This team stumbled backwards into a win. Underperforming by a league-worst <span class='text-danger-bright font-bold'>-24.42</span> points and still winning is not skill; it’s a statistical anomaly. Apocalyptic failures from Tyreek Hill and Bo Nix make this the ugliest, most undeserved win of the season. Send your opponent a gift basket and an apology.", panicMeter: { level: "DEFCON 1", color: "text-red-500 bg-red-100" }, score: { actual: 114.28, projected: 138.70 }},
      { rank: 11, teamName: "Kim Jong Nate", manager: "Nathan", record: "0-2-0", tagline: "The Sleeping Giant", blurb: "This team is a paradox. It has the best player in fantasy football, Christian McCaffrey, who was solid. It also has Joe Burrow, who played like he was throwing a wet loaf of bread. A truly pathetic 8.82 points from a supposed franchise QB didn't just lose the week; it's masking the terrifying potential of this roster. This is a dangerous team with a QB problem.", panicMeter: { level: "HIGH ALERT", color: "text-yellow-500 bg-yellow-100" }, score: { actual: 110.22, projected: 128.16 }},
      { rank: 12, teamName: "ShakeNBake", manager: "Abhishek", record: "0-2-0", tagline: "A Shakespearean Tragedy", blurb: "The second-biggest projection bust of the week is a sight to behold. Watching your first-round TE, Mark Andrews, deliver a single point is a fantasy tragedy of Shakespearean proportions. It's a tale told by an idiot, full of sound and fury, signifying nothing... except a crushing loss. Leaving Stefon Diggs on the bench was the final act of this tragic comedy.", panicMeter: { level: "FIVE ALARM FIRE", color: "text-red-500 bg-red-100" }, score: { actual: 94.94, projected: 122.67 }},
      { rank: 13, teamName: "Hail Mary", manager: "Andrew", record: "2-0-0", tagline: "The Biggest Lie in the League", blurb: "This team's 2-0-0 record is the biggest fraud since the Fyre Festival. Winning while your roster implodes and underperforms by nearly 14 points isn't a strategy; it's a fluke. With no depth and a negative performance, this team is a paper-thin contender about to be exposed.", panicMeter: { level: "HIGH ALERT (DESPITE RECORD)", color: "text-yellow-500 bg-yellow-100" }, score: { actual: 115.44, projected: 129.20 }},
      { rank: 14, teamName: "INDIAN JONES", manager: "Anuj", record: "0-2-0", tagline: "Wasting a Goldmine", blurb: "This isn't a team; it's a crime scene. The worst score and the biggest bust of the week. But the real tragedy is the 48 points rotting on the bench. Your bench could beat your starters. It's time to fire the manager and hire someone who actually checks their lineup before kickoff.", panicMeter: { level: "SOUND THE ALARMS", color: "text-red-500 bg-red-100" }, score: { actual: 83.64, projected: 118.49 }}
    ]
  },
  "2": {
    // PASTE YOUR WEEK 2 DATA HERE
    title: "Week 2 Report: [Your Title Here]",
    matchup: { 
        team1Name: "", team1Record: "", team1Blurb: "",
        team2Name: "", team2Record: "", team2Blurb: "",
        verdict: ""
     },
    superlatives: { 
        boom: { team: "", reason: "" },
        bust: { team: "", reason: "" },
        manager: { team: "", reason: "" },
        fraud: { team: "", reason: "" }
     },
    rankings: [
        // Add 14 new team ranking objects for week 2 here
    ]
  }
};