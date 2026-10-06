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
        "at this. This week it averaged 114.81 and the invoice arrived. Hail Mary went from "
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
           "not need a quarterback, and neither does Barrett. Greg (Miley) lost this by 19.78 "
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


WEEK3 = {
    "headline": "The Median Was Decided By Fifty-Two Cents. Everything Else Was Worse.",
    "kicker": "(week 3, corrected: it was two cents until Yahoo took half a tackle off Fred Warner)",
    "lede": (
        "The median this week was 120.70. Barrett (A dad) scored 120.96 and Nathan (Kim Jong Nate) "
        "scored 120.44, so one of them cleared it by 26 cents and the other missed it by 26 cents, "
        "and that quarter is the only reason Kim Jong Nate is no longer undefeated. This page used "
        "to say a penny; then Yahoo reviewed the tape and took half a tackle off Fred Warner. "
        "Barrett needed his quarter because he left 37.16 points on his own bench and lost his actual game by 0.46. "
        "Leo the Cleo is the last unbeaten team in the league. Four managers benched a quarterback "
        "who outscored the one they started, and one of them is Andrew, for the third week in a "
        "row. ShakeNBake scored the league low again. Fwamming Gwaggon won a game. Nobody is "
        "sure what to do with that."
    ),

    "games": {
        1: "Andrew has now started the wrong quarterback three weeks running. Week 1 it was Caleb "
           "Williams. Week 2 it was Dak Prescott. Week 3 it was Dak Prescott again: 18.94 on the "
           "bench, Jalen Hurts 13.62 in the lineup. He won anyway, by 0.46, which is smaller than "
           "the quarterback mistake and much smaller than the other guy's mistakes. Barrett "
           "started Pat Freiermuth (4.1) over Brock Bowers (23.6), started Tyler Bass (5.8), a "
           "kicker he picked up off the street on Tuesday, over Chris Boswell (14.3), and left "
           "Brian Robinson's 13.16 on the bench. His best lineup scores 158.12 and wins by 36.70. "
           "He lost by less than half a point, then beat the median by 0.26 and walked away 1-1 "
           "like nothing happened.",
        8: "Maclane scored 146.64, the high score of the week, and still managed to bench the "
           "Vikings defense: 24.76 points, six sacks and a return touchdown, sitting behind a "
           "Chiefs defense that scored 9.30. That is the second week running the Vikings have "
           "outscored his starting defense from the bench. It cost him 15.46 points and he won "
           "by 2.34, so this time it was free. Darrius lost it by the exact width of one swap: "
           "Keenan Allen 15.3 on the bench, Stefon Diggs 5.3 in the lineup, a difference of 10.00 "
           "points in a game decided by 2.34. Cameron Dicker, after two straight weeks of exactly "
           "2.00 points, kicked for 9.50 and nobody said thank you.",
        14: "Greg (IR) is 3-0 against his opponents and 0-3 against the median, which makes him "
            "the only manager in the league who has beaten every person he played and lost to "
            "arithmetic every single week. Brock Purdy threw four touchdowns for 31.28. Trey "
            "Smack, the kicker Greg claimed on waivers for $0, scored exactly 2.00, which means "
            "the Cameron Dicker curse did not end, it was traded. Greg is on 21 roster moves and "
            "has now added Ja'Kobi Lane twice. Will finally started Denzel Boston, the rookie who "
            "scored 30.9 on his bench in the first two weeks, and Boston scored 7.1. Terry "
            "McLaurin scored 16.7 on the same bench. Will's best lineup wins this game by 24.36.",
        10: "Chris is 6-0 and the last undefeated team in the league, and he got there by "
            "benching Tyler Shough's four touchdowns and 24.80 points to start Josh Allen for "
            "18.96. Jahmyr Gibbs scored 37.90 and covered for everything. Greg (Miley) is 0-6. "
            "He benched Matthew Stafford's 390 yards (22.90) to start Jared Goff (19.36), and he "
            "benched Bryce Young (14.64) as well, because Greg has three quarterbacks and a "
            "deep conviction that the one on the field should be the second best. His best "
            "lineup record for the season is 5-1. His real record is 0-6.",
        4: "Nathan played a clean game, beat Whole Milk by 27.28, and lost his undefeated record "
           "anyway, to the median, by 26 cents. The only change his best lineup makes is Chris "
           "Bell (8.7) for Malachi Fields (2.9). That is 5.80 points, and he needed 0.27. Anuj "
           "renamed his team from Talk Darty to Me to Whole Milk, then picked up Geno Smith on "
           "Tuesday and benched him on Sunday. Geno threw three touchdowns for 26.04. Baker "
           "Mayfield started and scored 12.28. The rebrand is 0-6 and already past its date.",
        13: "Jon, whose team the preseason model ranked first, won his first head-to-head game of "
            "the season. He did it while starting Adonai Mitchell at flex, a player Yahoo "
            "projected for zero points, who scored zero points, with Michael Mayer's 10.7 on the "
            "bench. He also spent $30 of FAAB on Rashod Bateman and benched him for 4.7. Bijan "
            "Robinson ran for 194 yards and none of that mattered. Abhishek scored 85.16, the "
            "lowest score in the league for the second week in a row. He is 0-26 in all-play "
            "over the last two weeks, which means that in fourteen days he has not outscored a "
            "single team in this league once. He made four free-agent adds between 8:49 and "
            "9:39 on Sunday morning and started one of them, Terrance Ferguson, at flex, for "
            "1.4, with Carnell Tate's 8.8 on the bench.",
        5: "Tom played a perfect lineup, scored 146.00, and beat FreeGucci by 56.34, the "
           "biggest margin of the week. Drake London caught nine balls for 194 yards. Tom has "
           "made two roster moves all season and is 5-1. Nishil started Drake Maye, who threw "
           "two interceptions and lost a fumble for 6.76, and benched Kalif Raymond (18.6) and "
           "Wan'Dale Robinson (15.2). He paid $9 for Emanuel Wilson on Tuesday and got 1.4 "
           "points on the bench. 1-5, 1-12 in all-play, eleven moves.",
    },

    "sections": {
        "awards": "Ten citations. Two of them are for 26 cents.",
        "power": "Season to date: record, points, all-play and this week's form, weighted, with "
                 "movement from last week. Best lineup is the record each team would own if it "
                 "had started its best legal lineup every week, everyone else exactly as they "
                 "played. The tax is the difference: wins left on your own bench.",
        "median": "Week 3's line was 120.70. A dad made it by 0.26. Kim Jong Nate missed it by "
                  "0.26. The top seven were separated from the bottom seven by 52 cents, and by two "
                  "cents until Yahoo's stat correction. Right of the line is a win.",
        "standings": "Week 3 scoring, both results, and how much of your own roster you managed "
                     "to start. Efficiency is what you scored over what your best legal lineup "
                     "would have scored. Injured reserve does not count against you.",
        "bench": "221.94 points of lineup regret this week, up from 194.22. Four benched "
                 "quarterbacks outscored the quarterback started in front of them. The personal "
                 "growth lasted one week.",
        "faab": "Tuesday's waivers and the week's free agents, audited: every dollar, what it "
                "bought, and what that player did the same Sunday. This is a receipt, not a "
                "shopping list. Nobody here is telling you who to pick up.",
        "money": "Auction dollars against everything each player has scored so far, started or "
                 "not. Three weeks is a sample now. Plan your excuses accordingly.",
        "studs": "The best and worst individual starts of Week 3, measured against what Yahoo "
                 "thought they would do.",
        "games": "The long version, closest game first.",
    },

    "blurbs": {
        10: "6-0 and the last unbeaten team in the league, on a week Chris benched four touchdown "
            "passes. Jahmyr Gibbs scored 37.9. The system still works when your running back is "
            "a cheat code too.",
        5: "Perfect lineup, 146.00, a 56-point win and two roster moves all season. Tom is doing "
           "the thing everybody else claims they are doing.",
        6: "Tied for the best all-play record in the league at 32-7 and lost this week by 2.34 "
           "with Keenan Allen's 15.3 on the bench. The unluckiest good team in the building.",
        2: "Lost by 0.46 with 37.16 points on the bench, the worst lineup efficiency in the "
           "league at 76.5 percent, then beat the median by 26 cents. Barrett is not good at "
           "this. Barrett is lucky at this.",
        4: "Undefeated for three weeks and then undone by 26 cents. The best lineup needed one "
           "swap worth 5.80. Nathan needed 0.27. The accountant finally missed a decimal.",
        1: "Started the wrong quarterback for the third straight week and won anyway, by 0.46. "
           "Three quarterbacks, three weeks, zero correct starts. The commissioner is on a "
           "streak.",
        8: "Scored the most points in the league and benched the defense that outscored his "
           "starting defense for the second week running. Up three spots. The Vikings would "
           "like to be considered.",
        14: "3-0 against his opponents, 0-3 against the median, 21 moves, one kicker who scored "
            "exactly 2.00. Greg has beaten everybody he has played and lost to a number every "
            "single week.",
        13: "Up five spots for his first head-to-head win, earned while starting a player "
            "projected for zero who scored zero. $30 of FAAB on Rashod Bateman, benched. The "
            "preseason number one is now merely below average.",
        3: "Finally started Denzel Boston and got 7.1, while Terry McLaurin scored 16.7 on the "
           "bench. The best lineup wins this game by 24.36. Will has discovered the exact "
           "opposite of timing.",
        11: "0-6. The best-lineup version of this team is 5-1, the biggest lineup tax in the "
            "league. Benched 390 passing yards this week. One roster move all season, and "
            "somehow that is also too many.",
        12: "League low for the second week running, 0-26 in all-play over two weeks, four "
            "Sunday-morning pickups in fifty minutes. The man who runs this website now has "
            "the worst recent form in it.",
        7: "Drake Maye: two interceptions, a lost fumble, 6.76 points. Two receivers on the bench "
           "scored 33.8 between them. 1-12 in all-play and eleven moves to show for it.",
        9: "Renamed from Talk Darty to Me to Whole Milk, then benched Geno Smith's three "
           "touchdowns two days after picking him up. 0-6. The new name has already gone off.",
    },

    "awards": [
        {"title": "Twenty-Six Cents",
         "winner": "Kim Jong Nate",
         "line": "Median: 120.70. Nathan: 120.44. First loss of the season, by a quarter and a "
                 "penny, in a week he won his actual game by 27.28. Chris Bell scored 8.7 on his "
                 "bench."},
        {"title": "Also Twenty-Six Cents",
         "winner": "A dad",
         "line": "Lost the matchup by 0.46 with Brock Bowers' 23.6 on the bench, then cleared "
                 "the median by 0.26 to stay 1-1. The worst lineup in the league bought itself "
                 "a win with loose change."},
        {"title": "Any Quarterback But That One, Part III",
         "winner": "Hail Mary",
         "line": "Caleb Williams in Week 1. Dak Prescott in Week 2. Dak Prescott in Week 3, "
                 "18.94 on the bench while Jalen Hurts scored 13.62. Three weeks, three wrong "
                 "quarterbacks, and somehow a 4-2 record."},
        {"title": "Beat Everyone, Lost To A Number",
         "winner": "The Injured Reserved",
         "line": "3-0 head-to-head. 0-3 against the median. Greg has beaten every manager "
                 "he has faced and lost to the middle of the league every single week."},
        {"title": "Picked Him Up To Bench Him",
         "winner": "Whole Milk 🥛",
         "line": "Geno Smith, added Tuesday, benched Sunday: 321 yards, three touchdowns, 26.04. "
                 "The highest-scoring bench player in the league, on a team that just renamed "
                 "itself after a dairy product."},
        {"title": "Bench Defense Of The Year (So Far)",
         "winner": "Mac Daddy",
         "line": "Vikings on the bench: 24.76, six sacks and a return touchdown. Chiefs in the "
                 "lineup: 9.30. Second week running. Won by 2.34 anyway, which only encourages "
                 "him."},
        {"title": "$30 For The Bench",
         "winner": "Fwamming Gwaggon",
         "line": "The biggest FAAB bid of the week, $30 on Rashod Bateman, who sat on the bench "
                 "and scored 4.7. The flex spot went to Adonai Mitchell: projected zero, scored "
                 "zero, exactly as advertised."},
        {"title": "Zero For Twenty-Six",
         "winner": "ShakeNBake",
         "line": "League low in Week 2, league low in Week 3, and in all-play across both he "
                 "has beaten nobody: 0-26. Four free agents added on Sunday morning. One of them "
                 "started at flex and scored 1.4."},
        {"title": "The Five-Win Bench",
         "winner": "Miley 💨LEO 5K Speedo Fan Club",
         "line": "Best lineup record 5-1. Real record 0-6. This week's bench: Matthew Stafford, "
                 "390 yards. Greg has made one roster move all season and not one correct "
                 "start decision that we can find."},
        {"title": "Nothing To Report",
         "winner": "The Asshouse Always Wins",
         "line": "Perfect lineup. 146.00. A 56.34-point win. Two moves all season. This award "
                 "exists so the rest of you can see what it looks like."},
    ],

    "waiver_note": (
        "Week 4 waivers process Tuesday night. Everything above already happened; none of it is "
        "a recommendation. Figure out your own roster. Start the quarterback who scores more "
        "points. That one is free."
    ),
}

WEEK4 = {
    "headline": "Brian Robinson Has Spent Four Weeks On The Bench And Improved Every Single Week",
    "kicker": "(week 4: 5.66, 7.70, 13.16, 25.20)",
    "lede": (
        "Brian Robinson has been on Barrett's bench for every week of this season, and his score "
        "has gone up every single week: 5.66, 7.70, 13.16, 25.20. This week he ran for three "
        "touchdowns. On the bench. Barrett started Ladd McConkey instead, who scored zero, and "
        "won anyway, because Barrett always wins anyway. The median hit 131.64, the highest line "
        "of the season. A dad cleared it by 56 cents and ShakeNBake missed it by 56 cents with "
        "15.96 points of Jaylin Noel on the bench. Kim Jong Nate spent $93 of FAAB in one night "
        "and has $7 left for the next thirteen weeks. Andrew finally started the right "
        "quarterback and lost by 52 points. Whole Milk played a perfect lineup and is 0-8. "
        "Leo the Cleo is 8-0 and has spent five dollars all year."
    ),

    "games": {
        5: "Tom played a perfect lineup for the second week running, scored 169.68, the high of "
           "the week, and needed every point of it. Greg (IR) scored 166.30, the highest losing "
           "score of the season by 19.02, and went 12-1 in all-play: he beat every team in the "
           "league except the one he was playing. Emanuel Wilson scored 26.5 at Tom's flex. Tom "
           "paid $7 for him. Last week Nishil paid $9 for the same man and got 1.4 on the bench. "
           "Greg's fix was sitting right there: Roman Wilson, a $0 waiver claim, 15.9 on the "
           "bench, over Juwan Johnson's 8.9 at flex. That is 7.00 points in a game decided by "
           "3.38. For three weeks Greg beat every opponent and lost to the median. This week he "
           "beat the median and lost to his opponent. He has also now added Tyler Goodson twice.",
        8: "Abhishek lost this by 6.28 and missed the median by 0.56, and the fix was one swap: "
           "Jaylin Noel, 114 return yards and 15.96 points on the bench, for Makai Lemon, 4.2 at "
           "flex. That is 11.76 points and a 2-0 week, in a league that pays for return yards, "
           "run by the man who keeps telling everyone it pays for return yards. Meanwhile "
           "KaVontae Turpin, who sat on ShakeNBake's bench in Week 1 before being released, "
           "returned 194 yards for Maclane and scored 9.76 in this exact game. Saquon Barkley, "
           "$52 at auction, ran for 8 yards. Maclane started Garrett Wilson (4.2) and a Friday "
           "free agent, DeMario Douglas (2.5), with Tyler Allgeier's 11.9 on the bench, and won "
           "anyway. Cameron Dicker kicked 115 yards of field goals for 13.50. The curse has left "
           "the building.",
        2: "Brian Robinson has been on Barrett's bench every week of the season. 5.66, 7.70, "
           "13.16, 25.20. This week he ran for three touchdowns, from the bench, while Barrett "
           "started Ladd McConkey at flex, who did not record a single stat and scored 0.00. "
           "Barrett won by 11.16 anyway because Kenneth Walker ran for 177 yards, then cleared "
           "the median by 0.56, after clearing it by 0.26 last week. Anuj, meanwhile, played a "
           "perfect lineup. Every start correct, 100.0 percent efficiency, Puka Nacua 24.2. He "
           "lost both games and is 0-8. He also paid $10 for Case Keenum on Wednesday, who is "
           "already off the roster.",
        4: "Nathan spent $93 of FAAB in a single waiver run on Wednesday morning: $75 on Ollie "
           "Gordon II and $18 on Kenyon Sadiq. Gordon scored 18.0 at flex, which is fine. Sadiq "
           "started at the other flex and scored 0.00, which is $18 for nothing. Nathan has $7 "
           "left, it is the first week of October, and there are thirteen weeks to go. He also "
           "left Tyquan Thornton on the bench, a free agent Yahoo projected for zero, who caught "
           "two touchdowns for 26.6. Nathan's best lineup scores 173.00, higher than anybody's "
           "actual score this week. He won by 16.80 anyway, because CeeDee Lamb caught 17 balls. "
           "Nishil got 27.16 out of Drake Maye and 19.4 out of a $3 T.J. Hockenson and still "
           "lost, because his kicker, Chase McLaughlin, scored exactly 2.00, and because after "
           "Kalif Raymond scored 7.7 and then 18.6 on his bench, Nishil finally started him. 2.24.",
        13: "Jon won his matchup and still went 1-1, the only manager this week to beat his "
            "opponent and lose to arithmetic. He paid $20 for Sam Darnold on Wednesday, benched "
            "him for Bo Nix, and Darnold outscored Nix by 0.76. Courtland Sutton caught one ball "
            "for four yards. Will scored 99.52, the lowest score in the league, and went 0-13 in "
            "all-play. Joe Burrow threw for 428 yards and it barely registered, because Ja'Marr "
            "Chase ($63) scored 4.2, Josh Downs 3.1 and Dalton Kincaid 1.2, while Romeo Doubs "
            "caught two touchdowns on the bench for 20.8. Will's best lineup scores 122.32 and "
            "wins this game. His season lineup regret is 86.88 points, the worst in the league.",
        11: "Greg (Miley) went 2-0 for the first time this season, behind Tetairoa McMillan's 14 "
            "catches, 192 yards and 40.2 points, the best start of the week, plus three Javonte "
            "Williams touchdowns. Naturally he still started the wrong quarterback: Bryce Young "
            "21.46, Jared Goff 21.48 on the bench. Two cents. He also started Rashee Rice at flex "
            "for 0.00. Darrius lost by 27.34 and would have won by 0.34 with his own bench: Alvin "
            "Kamara scored 20.3 and DK Metcalf 15.0 there, while Parker Washington (1.62), "
            "Stefon Diggs (6.0) and Travis Kelce (2.5) played. Darrius has the third-most points "
            "in the league and a 4-4 record.",
        10: "Chris is 8-0. Kyren Williams scored 32.7, Malik Nabers 21.2, and the Packers, picked "
            "up as a free agent at 11:19 on Sunday morning, scored 12.42. Chris has spent $5 of "
            "FAAB all season. Andrew, for the first time this year, started the right "
            "quarterback: Dak Prescott 18.10, Jalen Hurts 13.52 on the bench. He was rewarded "
            "with 100.02 points, a 52.42-point loss, the biggest of the week, and an 0-2. He "
            "benched Isaiah Williams' 15.18, a receiver he has now picked up twice, to start "
            "Bucky Irving for 6.1. Jeremiyah Love scored 6.0. The lesson Andrew learned this "
            "week is that doing it right does not help.",
    },

    "sections": {
        "awards": "Thirteen citations, one for every team except Mac Daddy, who is under "
                  "investigation.",
        "power": "Season to date: record, points, all-play and this week's form, weighted, with "
                 "movement from last week. Best lineup is the record each team would own if it "
                 "had started its best legal lineup every week, everyone else exactly as they "
                 "played. The tax is the difference: wins left on your own bench.",
        "median": "Week 4's line was 131.64, the highest of the season. A dad made it by 0.56. "
                  "ShakeNBake missed it by 0.56. Greg (IR) lost his game and finally beat the "
                  "median; Jon won his game and lost to it. Right of the line is a win.",
        "standings": "Week 4 scoring, both results, and how much of your own roster you managed "
                     "to start. Efficiency is what you scored over what your best legal lineup "
                     "would have scored. Injured reserve does not count against you.",
        "bench": "192.64 points of lineup regret this week, down from 221.94. Progress, unless "
                 "you are one of the three managers who started a player who scored zero.",
        "faab": "Every dollar of Week 4, audited. $93 of it was Nathan's. Tom paid $7 for the "
                "player Nishil paid $9 for last week and got 25.1 more points out of him. This is "
                "a receipt, not a shopping list.",
        "money": "Auction dollars against everything each player has scored so far, started or "
                 "not. A.J. Brown is now costing Jon $10.98 a point.",
        "studs": "The best and worst starts of Week 4, measured against what Yahoo thought they "
                 "would do. Three starters scored zero. Two of them cost more than $25.",
        "games": "The long version, closest game first.",
    },

    "blurbs": {
        10: "8-0, a 52.42-point win, and $95 of FAAB still in the drawer. Chris has spent five "
            "dollars all season and has not lost a game. The rest of you are paying retail.",
        5: "Perfect lineup for the second straight week, 169.68, 13-0 in all-play. Bought Emanuel "
           "Wilson for $7, the guy Nishil paid $9 for and benched, and got 26.5. Tom is shopping "
           "at FreeGucci's garage sale.",
        2: "7-1. Cleared the median by 0.26, then by 0.56. Started a receiver who scored zero. "
           "Benched a three-touchdown running back for the fourth straight week. If luck is a "
           "skill, Barrett is a first-ballot Hall of Famer.",
        4: "$93 of FAAB in one night: $75 on Ollie Gordon (18.0), $18 on Kenyon Sadiq (started, "
           "0.00). $7 left in the first week of October. Left 26.6 on the bench and won by 16.80 "
           "anyway. Nathan's budget is gone and so is his margin for error.",
        8: "Up two spots to 5-3. KaVontae Turpin, cut by ShakeNBake, returned 194 yards in a "
           "6.28-point win over ShakeNBake, and Cameron Dicker finally kicked like a person. "
           "Revenge, served by somebody else's former player.",
        6: "Down three spots. Third-most points in the league, 4-4, the worst luck in the "
           "building. This week it was not luck: Kamara 20.3 and Metcalf 15.0 on the bench, "
           "Parker Washington 1.62 in the lineup. The best lineup wins by 0.34.",
        14: "166.30, the highest losing score of the season by 19 points. First median win of the "
            "year, in the first week he lost a matchup. Roman Wilson's 15.9 sat on the bench in a "
            "3.38-point loss. 26 moves, Tyler Goodson twice.",
        1: "Started the right quarterback for the first time all season, scored 100.02 and lost "
           "by 52.42. Andrew finally learned the lesson, and the lesson was a lie.",
        11: "First 2-0 week of the year, behind Tetairoa McMillan's 40.2. Benched Jared Goff "
            "(21.48) to start Bryce Young (21.46). Wrong by two cents, which for Greg counts as a "
            "breakthrough.",
        13: "Won the matchup, lost to the median. Paid $20 for Sam Darnold, benched him, watched "
            "him outscore Bo Nix by 0.76. A.J. Brown, season to date: $45, 4.1 points.",
        12: "Missed the median by 0.56 and lost by 6.28 with Jaylin Noel's 114 return yards on "
            "the bench. Saquon Barkley, $52, scored 1.5. Up a spot only because the people below "
            "him are worse at this.",
        3: "League low, 99.52, 0-13 in all-play. Joe Burrow threw for 428 yards and Ja'Marr Chase "
           "($63) caught three balls for 27. Worst season lineup regret in the league: 86.88.",
        9: "0-8. Played a perfect lineup this week, every call correct, and lost both games. The "
           "lineup was never the problem. $10 on Case Keenum, already gone.",
        7: "14th of 14. Kalif Raymond scored 7.7, then 18.6, on the bench, so Nishil finally "
           "started him: 2.24. Chase McLaughlin kicked exactly 2.00. The curse has a new address.",
    },

    "awards": [
        {"title": "Four Weeks Of Bench Growth",
         "winner": "A dad",
         "line": "Brian Robinson on Barrett's bench: 5.66, 7.70, 13.16, 25.20. Three rushing "
                 "touchdowns this week. Ladd McConkey started instead and scored 0.00. Barrett "
                 "won by 11.16 and will learn nothing."},
        {"title": "Ninety-Three Dollars, One Night",
         "winner": "Kim Jong Nate",
         "line": "$75 on Ollie Gordon II and $18 on Kenyon Sadiq, both processed at 4:19 on "
                 "Wednesday morning. Sadiq started and scored 0.00. $7 left for thirteen weeks."},
        {"title": "Highest-Scoring Loser Of The Season",
         "winner": "The Injured Reserved",
         "line": "166.30 points and 12-1 in all-play. The one team that beat him was the one he "
                 "played. Roman Wilson's 15.9 on the bench was the game."},
        {"title": "The Two-Cent Quarterback",
         "winner": "Miley 💨LEO 5K Speedo Fan Club",
         "line": "Bryce Young 21.46 in the lineup, Jared Goff 21.48 on the bench. Last week Greg "
                 "benched 390 yards. This week he was wrong by two cents. Growth."},
        {"title": "Did Everything Right",
         "winner": "Whole Milk 🥛",
         "line": "Perfect lineup. 100.0 percent efficiency. 0-2 for the week, 0-8 for the season. "
                 "This award is a sympathy card."},
        {"title": "Did Everything Right, Part II",
         "winner": "Hail Mary",
         "line": "Started the right quarterback for the first time in four weeks. Scored 100.02 "
                 "and lost by 52.42, the biggest beating of the week. Back to guessing, Andrew."},
        {"title": "Garage Sale Of The Week",
         "winner": "The Asshouse Always Wins",
         "line": "Emanuel Wilson: $9 and 1.4 points on Nishil's bench in Week 3. $7 and 26.5 "
                 "points in Tom's flex in Week 4. Same player, same price range, different "
                 "manager."},
        {"title": "Return To Sender",
         "winner": "ShakeNBake",
         "line": "Jaylin Noel on the bench: 114 return yards, 15.96 points. Makai Lemon at flex: "
                 "4.2. KaVontae Turpin, his Week 1 bench guy, returned 194 yards against him for "
                 "Mac Daddy. Lost by 6.28, missed the median by 0.56."},
        {"title": "Started Him Too Late",
         "winner": "FreeGucci",
         "line": "Kalif Raymond on the bench: 7.7, then 18.6. Kalif Raymond in the lineup: 2.24. "
                 "Also Chase McLaughlin, 2.00, the kicker curse's new address."},
        {"title": "Bought A Quarterback To Bench Him",
         "winner": "Fwamming Gwaggon",
         "line": "$20 on Sam Darnold, benched for Bo Nix, outscored Bo Nix by 0.76. Won the game, "
                 "lost to the median, finished 1-1 on a coin he paid for."},
        {"title": "Undefeated On Five Dollars",
         "winner": "Leo the Cleo",
         "line": "8-0. $5 of FAAB spent all season. Grabbed the Packers at 11:19 on Sunday "
                 "morning and got 12.42. Some people just get to have nice things."},
        {"title": "Zero And Thirteen",
         "winner": "Good Will Hunting",
         "line": "99.52, the league low, and not one team in the league outscored. Joe Burrow "
                 "threw for 428 yards. Romeo Doubs caught two touchdowns on the bench."},
        {"title": "The Thirty-Four-Cent Bench",
         "winner": "Bend The Knee 🐲🔥",
         "line": "Best lineup beats Miley by 0.34. Actual lineup lost by 27.34. Kamara and "
                 "Metcalf on the bench, Parker Washington's 1.62 on the field."},
    ],

    "waiver_note": (
        "Week 5 waivers process Tuesday night. Nathan has $7. Everybody else, see above. None "
        "of this is advice. Start Brian Robinson, Barrett. Or don't. We will be here either way."
    ),
}

NOTES = {1: WEEK1, 2: WEEK2, 3: WEEK3, 4: WEEK4}
