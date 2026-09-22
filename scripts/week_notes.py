# -*- coding: utf-8 -*-
"""
Every line of prose for the weekly recap. build_week.py does the arithmetic and
imports NOTES; keeping the writing here means a re-scrape never overwrites a joke.

House rule, same as everywhere else on this site: full savage, fantasy decisions
only. Lineups, drafts, waivers, money. Never anybody's real life.

Remember the league plays TWO games a week - the matchup and the league median - so
a weekly record is 2-0, 1-1 or 0-2. Never write "won this week" about a 1-1.

Game notes are keyed by the WINNING team_id:
  1 Hail Mary · 2 A dad · 3 Good Will Hunting · 4 Kim Jong Nate
  5 The Asshouse Always Wins · 6 Bend The Knee · 7 FreeGucci · 8 Mac Daddy
  9 Talk Darty to Me · 10 Leo the Cleo · 11 Miley · 12 ShakeNBake
  13 Fwamming Gwaggon · 14 The Injured Reserved
"""

WEEK1 = {
    "headline": "Fourteen Managers Walked In. Nine Of Them Left Evidence.",
    "kicker": "(week 1, and the benches scored 247 points)",
    "lede": (
        "The model said this league would average 106 points a week. Week 1 came in at "
        "126 and change, which means every single one of you is about to mistake variance "
        "for genius. Two teams cleared 155. One team started a quarterback who threw for "
        "13 yards. Three managers lost a game they had the points to win, sitting on their "
        "own bench, in street clothes, watching. Then the median came for the rest: 117.91, "
        "the second opponent nobody gets to game-plan for. It saved two managers who lost "
        "their matchup and it took a win away from two who won theirs. Five of you are 2-0. "
        "Five of you are 0-2. Nothing you learned this week is real, and all of it is permanent."
    ),

    # one line under each game on the scoreboard
    "games": {
        14: "The two lowest scores of the week found each other, like they were "
            "supposed to. Greg made seven roster moves this week, more than anybody, "
            "and used exactly none of them to notice that Kyle Monangai was about to "
            "go for 20.4 on his bench while Jaylen Waddle caught one pass for two "
            "yards in his starting lineup. He won the matchup and then lost to the "
            "median by 12.37, so the reward for all that activity is 1-1. Anuj drew "
            "the only opponent in the league he could have beaten and still went 0-2.",
        4: "The cleanest win of the week and the dirtiest loss. Nathan is the only "
           "manager in this league who started his best available eleven, full stop, "
           "100 percent of the points he had, and it bought him a 2-0 by exactly 0.53 "
           "points over the median. Greg, the other Greg, started a quarterback for 5.1, "
           "a kicker for 1.0 and a wide receiver in the IDP slot for 2.6. That is 8.7 "
           "points from three roster spots. He lost by 8.68 and went 0-2. "
           "Do the math, it's already done.",
        1: "309 combined points, the best game on the board, and both managers "
           "should feel terrible. Andrew won it 162 to 147 with Caleb Williams and "
           "37.26 points glued to his bench and Kyle Pitts posting a clean zero in "
           "his starting lineup. Tom had the single best roster in the league on "
           "Sunday, 179.18 points of it, and played 147.28. Mahomes and Goedert "
           "watched from the couch. That is the whole game, right there. The only mercy "
           "is that 147.28 cleared the median by 29.37, so Tom banked the half he did "
           "not have to think about and goes to 1-1.",
        7: "Nishil scored 116.80, which is 10 points below league average, and won "
           "by 23. That is what happens when the man across from you pays $63 for a "
           "receiver who catches two balls for 12 yards. Will's starting lineup "
           "featured $84 of wideout producing 4.6 points while a $1 rookie put up "
           "12.9 on his bench. Zero all-play wins, and 0-2. But hold the parade in "
           "Gucci: 116.80 missed the median by 1.11, so winning by 22.70 bought Nishil "
           "a 1-1 anyway. One more catch anywhere on that roster and he is 2-0.",
        12: "Abhishek left 2.18 points on the bench, the best lineup management in "
            "the league that did not go clean, and it did not matter, because "
            "Darrius started Sam Darnold. Thirteen passing yards. 0.52 points. "
            "C.J. Stroud, also one dollar, also on the roster, threw for 274 and "
            "two scores from the bench. The $1 quarterback lottery has a losing "
            "ticket and Bend The Knee bought it. Darrius still cleared the median by "
            "7.67, which is the fantasy equivalent of getting hit by a bus and keeping "
            "your wallet. 1-1.",
        10: "The preseason number one against the preseason number two, and it was "
            "over by the second quarter. Chris got 35.66 from Josh Allen and 33.1 "
            "from Gibbs and never looked back. Jon started a $22 tight end who did "
            "not play a snap, a quarterback who scored 6.44, and benched the guy "
            "who threw for 387. 110 points a week was the projection. This is the "
            "kind of week that makes a projection feel personal.",
        2: "The biggest beating of the week, 52.58, delivered by a man whose "
           "quarterback finished with 0.62 points. Barrett started Kyler Murray, "
           "watched him throw for 18 yards and an interception, and still put up "
           "157.06 because Kenneth Walker went for 34.6 and Chuba Hubbard went for "
           "22.2. Maclane got 24.96 from Lamar Jackson and then the rest of his "
           "roster filed for unemployment, 13 points under the median, 0-2.",
    },

    # section intros
    "sections": {
        "awards": "Ten citations from a single Sunday. Every one of them is a number "
                  "somebody chose on purpose.",
        "games": "Now the long version, closest game first. Scores, lineups, and what "
                 "each manager did to himself.",
        "median": "This league plays two games a week: your matchup, and the league "
                  "median. Week 1's line was 117.91. Seven teams cleared it and seven did "
                  "not, which is what a median is, and it is the one opponent that does not "
                  "care who you were scheduled against. Bars run from the line. Right is a win.",
        "standings": "Week 1 scoring, all-play record, and how much of your own "
                     "roster you actually managed to start, plus both results. Efficiency is what you "
                     "scored over what your best legal lineup would have scored. "
                     "Injured reserve does not count against you. Everything else does.",
        "bench": "247.36 points sat on benches this week. That is nearly two full "
                 "winning scores, in street clothes, doing nothing. Here is where "
                 "they were sitting.",
        "money": "Every dollar from draft night, priced against exactly one Sunday "
                 "of work. It is a sample of one and it is completely unfair, which "
                 "is the entire point of running it.",
        "draftvs": "Preseason projections against what actually happened. The model "
                   "ranked all fourteen of you in September on projected points per "
                   "week. One week is noise. Enjoy the noise.",
        "studs": "The best and worst individual performances of Week 1, measured "
                 "against what Yahoo thought they would do.",
        "waivers": "FAAB and roster moves through the end of Week 1. Waivers run "
                   "Tuesday night, so this board is a snapshot, not a shopping list. "
                   "Nobody here is telling you who to pick up. Half of you would do "
                   "the opposite out of spite anyway.",
    },

    # award, winner team name, and the receipt
    "awards": [
        {"title": "The $34 Per Point Award",
         "winner": "The Injured Reserved",
         "line": "Jaylen Waddle, $24, one reception, two yards, 0.70 points. "
                 "That is $34.29 per fantasy point. He won the game anyway, which "
                 "somehow makes it worse."},
        {"title": "Bench Warrant Issued",
         "winner": "Miley 💨LEO 5K Speedo Fan Club",
         "line": "36.84 points left on the bench, the most in the league, in a game "
                 "lost by 8.68. Jalen Coker cost two dollars and scored 30.8 from the "
                 "sideline. Jared Goff threw for two touchdowns next to him."},
        {"title": "The Perfect Lineup, Entirely Wasted",
         "winner": "Kim Jong Nate",
         "line": "The only 100 percent efficiency in the league. Started his best "
                 "eleven, every slot, no regrets. Finished seventh in scoring. "
                 "Sometimes the best you have is 118.44."},
        {"title": "Least Necessary Flex",
         "winner": "A dad",
         "line": "Won by 52.58 points while his starting quarterback threw for "
                 "18 yards and an interception. Kyler Murray scored 0.62. "
                 "The other ten starters scored 156.44."},
        {"title": "The Ja'Marr Chase Memorial Receipt",
         "winner": "Good Will Hunting",
         "line": "$63 for two catches and 12 yards. Add $21 of Terry McLaurin for "
                 "14 more. That is $84 of wide receiver, 26 yards, 4.6 points, and "
                 "the lowest score in the league."},
        {"title": "Thirteen Yards",
         "winner": "Bend The Knee 🐲🔥",
         "line": "Sam Darnold: 13 passing yards, 0.52 fantasy points, started at "
                 "quarterback on purpose, in a league where C.J. Stroud was on the "
                 "same bench for the same one dollar."},
        {"title": "Rebrand Of The Year",
         "winner": "Talk Darty to Me 🎯",
         "line": "Changed the name from Poop Squad after the draft, then went 1-13 "
                 "in all-play and scored 98.10. Jordan Addison and Davante Adams "
                 "combined for 4.1 points out of the starting lineup. New name, "
                 "same squad."},
        {"title": "Won The Game, Lost The Week",
         "winner": "FreeGucci",
         "line": "Beat Good Will Hunting by 22.70 and missed the median by 1.11. "
                 "A single catch anywhere on the roster is the difference between 2-0 "
                 "and 1-1, and he will think about that until November."},
        {"title": "Half A Point From A Different Season",
         "winner": "Fwamming Gwaggon",
         "line": "117.38 against a median of 117.91. As the 8th-highest score in a "
                 "14-team league he helped set that number, then lost to it by 0.53 "
                 "and left Week 1 at 0-2 as the preseason favourite."},
        {"title": "Paid In Full",
         "winner": "ShakeNBake",
         "line": "Isaiah Likely, three dollars, 23.80 points, the best tight end "
                 "week in the league. Trevor Lawrence, seven dollars, four "
                 "touchdowns. 98.6 percent lineup efficiency. Annoying."},
    ],

    "waiver_note": (
        "Waivers process Tuesday night. This page refreshes Wednesday with what "
        "cleared, what it cost, and which of you spent real FAAB money on a Week 1 "
        "box score. No recommendations here, ever. Figure out your own roster."
    ),
}


WEEK2 = {
    "headline": "Last Week's Geniuses Have Asked Us Not To Bring It Up",
    "kicker": "(week 2, and we are bringing it up)",
    "lede": (
        "Last week this league averaged 126 points and fourteen people decided they were good "
        "at this. This week it averaged 114.88 and the invoice arrived. Hail Mary went from "
        "162.10 to 97.72. ShakeNBake went from 155.60 to 72.04, the lowest score in the league, "
        "days after spending $70 of FAAB. Good Will Hunting went from last place to 2-0. "
        "Bend The Knee, ranked 14th of 14 in the preseason, played a perfect lineup, scored "
        "168.86 and beat the preseason favourite by more than the preseason favourite scored. "
        "Three teams are 4-0. Three teams are 0-4, and one of them is Greg (Miley), whose best "
        "possible lineup would be 4-0. We checked. Twice."
    ),

    "games": {
        5: "Tom finally started Patrick Mahomes, who threw for 382 and three touchdowns, and "
           "finally started Dallas Goedert, who caught one ball for four yards. Last week "
           "Goedert scored 21.7 on the bench. Fantasy football is the only sport where you are "
           "punished for learning. Anuj lost this by 6.52 with Tre Tucker's 21.4 on the bench "
           "and the most on-brand disaster in league history: a team named Talk Darty to Me got "
           "20 passing yards and 0.80 points out of Jaxson Dart. Davante Adams went for 38.5, "
           "which was very kind of him and changed nothing. 0-4.",
        10: "Chris got 40.82 from Josh Allen and is 4-0 despite starting two receivers who "
            "combined for 1.5 points. Maclane's lineup did everything in its power to lose: $18 "
            "of fresh FAAB on Mike Gesicki, started at tight end, zero points, with George "
            "Kittle's 16.0 on the bench next to a Vikings defense that scored 17.06 while the "
            "Chiefs defense he picked up off the street scored 6.5. His best lineup scores "
            "147.98 and wins this game by 11.88. His kicker, Cameron Dicker, has now scored "
            "exactly 2.00 points in back-to-back weeks. The median bailed him out by 0.90 for a "
            "1-1 he did nothing to earn.",
        2: "Barrett is 4-0 with a quarterback room that has produced 6.94 points in two weeks. "
           "Kyler Murray gave him 0.62, so he picked Carson Wentz up off the street, and Wentz "
           "gave him 6.32. Amon-Ra St. Brown went for 31.7 and it turns out this roster does "
           "not need a quarterback, and neither does Barrett. Greg (Miley) lost this by 20.78 "
           "while his bench scored 100.72: Jared Goff 29.78, Bryce Young 24.08 (bought for $10 "
           "on Tuesday, benched on Sunday), Dalton Schultz 21.0 on twelve catches, Jonah Coleman "
           "13.3, Jalen Coker 12.56. His best lineup wins this game. It also would have won last "
           "week's. More on that below, if you can stand it.",
        14: "Greg (IR) is on 15 roster moves in two weeks, more than the six quietest managers "
            "in this league combined, and that includes adding Nate Landman on September 10 "
            "and then adding Nate Landman again on September 20. He won the matchup for the "
            "second week running and lost to the median for the second week running, by 4.16 "
            "this time, so he is 2-0 against his schedule and 0-2 against the league. Nishil got "
            "negative points from DJ Moore: minus one rushing yard, zero catches, minus 0.10. "
            "That is not a bad week. That is a fine for showing up.",
        4: "Nathan played his second perfect lineup in two weeks, has made one roster move all "
           "season, and is 4-0 on scores of 118.44 and 126.46, which is the least exciting way "
           "to be undefeated and he could not care less. CeeDee Lamb went for 33.3 and Brandon "
           "Aubrey kicked 129 yards of field goals. Andrew went from the league's high score to "
           "97.72 by doing exactly what he did last week: benching the right quarterback. Last "
           "week it was Caleb Williams and 37.26. This week it was Dak Prescott, four "
           "touchdowns, 29.76, while Jalen Hurts started and threw two picks.",
        3: "Will's first win of the season, and it came against the man who built this website. "
           "Ja'Marr Chase, the $63 receiver who caught two balls for 12 yards in Week 1, went "
           "for 23.0, and Will's $35 waiver pickup Romeo Doubs added 11.1. Will also benched "
           "Denzel Boston again, and Boston scored 18.0 on the bench again, which puts the $1 "
           "rookie at 30.9 points in two weeks from a bench Will refuses to look at. Abhishek "
           "scored 72.04, the lowest score in the league, zero all-play wins, on a roster he "
           "spent $70 of FAAB rebuilding this week. His lineup was 95.1 percent efficient. "
           "The lineup was fine. The roster is the problem, and the roster is what he paid for.",
        6: "Darrius started Sam Darnold last week for 0.52 points. This week Darnold is on "
           "injured reserve, which is the most useful thing he has done for this roster, and "
           "Darrius put up 168.86, the high score of the week by 32.76, with a perfect lineup. "
           "Jaxon Smith-Njigba 40.0 on three touchdowns, Travis Kelce 21.6, James Cook 21.4, "
           "Stefon Diggs 19.2. The preseason model ranked this team 14th of 14. Jon's team, "
           "which the same model ranked 1st, scored 82.22. The winning margin, 86.64, was bigger "
           "than the losing score. The preseason favourite is 0-4 and his $22 tight end has "
           "0.80 points on the season.",
    },

    "sections": {
        "awards": "Ten citations. Every one of them is a decision somebody made on purpose, on "
                  "a phone, in public.",
        "power": "Season to date: record, points, all-play and this week's form, weighted, with "
                 "movement from last week. Best lineup is the record each team would own if it "
                 "had started its best legal lineup every week, everyone else exactly as they "
                 "played. The tax is the difference: wins left on your own bench.",
        "median": "Week 2's line was 118.02. The two teams either side of it, 7th and 8th, made "
                  "or missed it by 0.90 each, which is becoming a tradition. Right of the line "
                  "is a win.",
        "standings": "Week 2 scoring, both results, and how much of your own roster you managed "
                     "to start. Efficiency is what you scored over what your best legal lineup "
                     "would have scored. Injured reserve does not count against you.",
        "bench": "194.22 points sat on benches this week, down from 247 last week, which is the "
                 "closest thing to personal growth this league has shown.",
        "faab": "Tuesday's waivers and the week's free agents, audited: every dollar, what it "
                "bought, and what that player did the same Sunday. This is a receipt, not a "
                "shopping list. Nobody here is telling you who to pick up.",
        "money": "Auction dollars against everything each player has scored so far, started or "
                 "not. Two weeks is still unfair. It is less unfair than one.",
        "studs": "The best and worst individual starts of Week 2, measured against what Yahoo "
                 "thought they would do.",
        "games": "The long version, closest game first.",
    },

    "blurbs": {
        10: "Josh Allen has 76.48 points in two weeks and Chris started two receivers who "
            "combined for 1.5 this week. Number one anyway. The system works when your "
            "quarterback is a cheat code.",
        2: "Undefeated with 6.94 points of quarterback play across two weeks. Barrett has "
           "invented football without the forward pass and nobody has the heart to tell him.",
        6: "Ranked 14th in the preseason. Now 3rd, with the biggest score of the year and a "
           "perfect lineup. Getting Sam Darnold off the field is the best personnel decision "
           "anyone has made this season.",
        4: "Two perfect lineups, one roster move, zero excitement, 4-0. Nathan plays fantasy "
           "football the way accountants play poker, and he is taking everybody's money.",
        5: "Best-lineup record 4-0, real record 3-1, and the missing win is Mahomes and Goedert "
           "on the Week 1 bench. Tom has since learned to start them. Goedert has since "
           "learned to stop scoring.",
        1: "From 162 to 97. Three quarterbacks, two weeks, and the wrong one started both times. "
           "Andrew is the commissioner, so complaints about this blurb can go to Andrew.",
        3: "Up seven, the biggest climb of the week, because Ja'Marr Chase remembered what he "
           "is paid for. Denzel Boston has 30.9 points and zero starts. Will is saving him for "
           "something.",
        14: "Fifteen moves. Added Nate Landman twice. Undefeated against his opponents, winless "
            "against the median, and the best-lineup version of this team is 4-0. Greg is very "
            "busy doing something.",
        12: "Spent 70 percent of the season's FAAB this week and scored 72.04 on Sunday. The "
            "two biggest bids, $52 between them, sat on the bench for 7.5 points. Saquon Barkley "
            "also cost $52 and scored 2.5. The man who runs this website would like everyone to "
            "stop visiting it.",
        8: "Up two spots on the strength of the median and nothing else. Paid $18 for a tight "
           "end who scored zero while George Kittle sat. The kicker has scored exactly 2.00 in "
           "each of the last two weeks, which at least suggests a process.",
        11: "The best lineup on this roster is 4-0. The lineup Greg started is 0-4. His bench "
            "scored 100.72 on Sunday. The other Greg in this league made fifteen moves; this "
            "one could stand to make a single correct one.",
        7: "DJ Moore scored negative points. Not a low number, a negative one. George Pickens "
           "has 11.3 on the season at $37. The only win so far came against Week 1's lowest score.",
        9: "Named the team after Jaxson Dart, then Jaxson Dart threw for 20 yards. Tre Tucker's "
           "21.4 on the bench would have won both games this week. The rebrand is 0-4 and has "
           "asked for its old name back.",
        13: "Preseason number one. Now 0-4, 14th, 7-19 in all-play, and outscored by 86.64 in a "
            "single game. The model that ranked this team first has been taken out back.",
    },

    "awards": [
        {"title": "The Undefeated Ghost",
         "winner": "Miley 💨LEO 5K Speedo Fan Club",
         "line": "Greg's best possible lineup is 4-0. The lineup Greg actually started is 0-4. "
                 "His bench scored 100.72 on Sunday, including 24.08 from Bryce Young, whom he "
                 "bought for $10 on Tuesday specifically not to play."},
        {"title": "Named After His Quarterback, Unfortunately",
         "winner": "Talk Darty to Me 🎯",
         "line": "Jaxson Dart: 20 passing yards, 0.80 points, started by a team called Talk "
                 "Darty to Me. Baker Mayfield sat on the bench with 13.18. The branding held. "
                 "The quarterback did not."},
        {"title": "The $70 Week",
         "winner": "ShakeNBake",
         "line": "$70 of a $100 season budget in a single week, for 22.2 points. $52 of it went "
                 "to two bench players who scored 7.5, the same $52 he paid for Saquon Barkley, "
                 "who scored 2.5. He also paid $13 to re-sign Kayshon Boutte, a receiver he had "
                 "picked up for free the week before."},
        {"title": "Any Quarterback But That One",
         "winner": "Hail Mary",
         "line": "Week 1: benched Caleb Williams, who outscored the starter by 12.54. Week 2: "
                 "benched Dak Prescott, four touchdowns, who outscored the starter by 11.60. "
                 "Three quarterbacks on the roster and a perfect record of starting the wrong one."},
        {"title": "Finally Started Him",
         "winner": "The Asshouse Always Wins",
         "line": "Dallas Goedert, Week 1, on the bench: 21.7 points. Dallas Goedert, Week 2, in "
                 "the starting lineup: one catch, four yards, 0.90. Tom will never trust anything "
                 "again and he is right not to."},
        {"title": "$18 For A Zero",
         "winner": "Mac Daddy",
         "line": "Mike Gesicki, bought Tuesday, started Sunday at tight end, zero points. George "
                 "Kittle on the bench: 16.0. The Vikings defense on the bench: 17.06. The best "
                 "lineup wins this game by 11.88. The median carried him to 1-1 by 0.90 instead."},
        {"title": "Below Zero",
         "winner": "FreeGucci",
         "line": "DJ Moore: minus one rushing yard, zero catches, minus 0.10 fantasy points. A "
                 "player on bye scores zero, which would have been an upgrade. Nishil started one "
                 "who played."},
        {"title": "The Least Watchable 4-0 On Record",
         "winner": "Kim Jong Nate",
         "line": "Second straight perfect lineup. One roster move all season. Scores of 118.44 "
                 "and 126.46, no bench regret, no drama, no fun. Undefeated."},
        {"title": "Bench Him Again, I Dare You",
         "winner": "Good Will Hunting",
         "line": "Denzel Boston, $1: 12.9 on the bench in Week 1, 18.0 on the bench in Week 2. "
                 "That is 30.9 points and zero starts. Will spent $35 on Romeo Doubs instead, and "
                 "Doubs scored 11.1."},
        {"title": "Doubled",
         "winner": "Bend The Knee 🐲🔥",
         "line": "168.86 against 82.22. The margin, 86.64, was bigger than the losing team's "
                 "entire score. A perfect lineup, one week after starting a quarterback who threw "
                 "for 13 yards."},
    ],

    "waiver_note": (
        "Week 3 waivers process Tuesday night. Everything above already happened; none of it is "
        "a recommendation. Figure out your own roster. Judging by the table up top, some of you "
        "should start soon."
    ),
}

NOTES = {1: WEEK1, 2: WEEK2}
