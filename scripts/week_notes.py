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
        5: "Tom played a perfect lineup for the second week running, scored 168.68, the high of "
           "the week, and needed every point of it. Greg (IR) scored 166.30, the highest losing "
           "score of the season by 19.02, and went 12-1 in all-play: he beat every team in the "
           "league except the one he was playing. Emanuel Wilson scored 26.5 at Tom's flex. Tom "
           "paid $7 for him. Last week Nishil paid $9 for the same man and got 1.4 on the bench. "
           "Greg's fix was sitting right there: Roman Wilson, a $0 waiver claim, 15.9 on the "
           "bench, over Juwan Johnson's 8.9 at flex. That is 7.00 points in a game decided by "
           "2.38. For three weeks Greg beat every opponent and lost to the median. This week he "
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
        5: "Perfect lineup for the second straight week, 168.68, 13-0 in all-play. Bought Emanuel "
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
            "2.38-point loss. 26 moves, Tyler Goodson twice.",
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

WEEK5 = {
    "headline": "They Finally Started Brian Robinson. He Scored 4.04.",
    "video": {
        "src": "video/2026-wk05.mp4",
        "poster": "video/2026-wk05.jpg",
        "seconds": 44,
        "title": "Week 5 in 44 seconds",
        "blurb": "All fourteen teams, the $15 quarterback on the bench, the perfect lineup made "
                 "of byes and a 10-0 team nobody can touch. Sound on.",
    },
    "kicker": "(week 5: 5.66, 7.70, 13.16, 25.20 on the bench, 4.04 in the lineup)",
    "lede": (
        "For four weeks Brian Robinson improved on Barrett's bench: 5.66, 7.70, 13.16, 25.20. "
        "This week Barrett finally started him. He scored 4.04. Barrett also started Oronde "
        "Gadsden at flex, a free agent picked up at 1:34 on Sunday afternoon, who scored 0.00, "
        "the second straight week a Barrett flex has scored nothing. He went 2-0 anyway and is "
        "9-1, because Barrett always gets away with it. The median hit 138.60, the highest line of "
        "the season for the second week running. Tom cleared it by 42 cents and Will, the man he "
        "was playing, missed it by 42 cents. Will paid $15 for Matthew Stafford at 3:19 on Sunday morning, benched "
        "him, and lost by 0.84 while Stafford threw for 383 yards. Anuj won his first game of "
        "the season, against a number. Greg (Miley) played a perfect lineup because his entire "
        "bench was on bye. Leo the Cleo is 10-0."
    ),

    "games": {
        5: "Will paid $15 for Matthew Stafford on waivers, processed at 3:19 on Sunday morning, "
           "then benched him for Joe Burrow. Stafford threw for 383 yards and three touchdowns, "
           "27.32 points, on the bench. Burrow scored 24.60. In Week 3 Greg (Miley) benched "
           "Stafford's 390 yards. Two managers, two benchings, 773 yards nobody started. The "
           "quarterback was not even the worst of it: Denzel Boston caught a touchdown for 12.62 "
           "on the bench and Terry McLaurin scored 10.2 there, while KC Concepcion (1.0) and "
           "Romeo Doubs (2.1) started. Boston for Concepcion alone wins this game. Will's best "
           "lineup scores 160.62 and wins by 21.60. Stafford for Burrow alone wins it. Instead he lost "
           "by 0.84, missed the median by 0.42 and went 0-2. Tom paid $9 for Jacoby Brissett with Patrick Mahomes on bye, got "
           "25.78, cleared the median by 0.42 and is 9-1. Tom's waiver receipts this season: $7 "
           "for Emanuel Wilson, $9 for Brissett, both started, both paid.",
        8: "Maclane spent $66 of FAAB in one waiver run on Wednesday morning: $41 on Keon "
           "Coleman, $21 on Dohnte Meyers and $4 on Aaron Rodgers. The $4 quarterback threw three "
           "touchdowns for 22.00. The $41 receiver scored 7.2. The $21 receiver sat on the bench "
           "and scored 7.36. Maclane has $16 left. He scored 113.38, the fourth-lowest score of "
           "the week, missed the median by 25.22, and still won his game, because he drew Jon. "
           "Jon started Bo Nix (7.92) over Sam Darnold (10.30) for the second straight week, the "
           "$20 quarterback he bought to bench. Kendrick Bourne, a Wednesday free agent, scored "
           "9.5 on the bench and Rashod Bateman 8.7, while David Montgomery ($23) scored 1.1 and "
           "Brian Thomas Jr. scored 1.0, all of it from one solo tackle. T.J. Watt scored zero. "
           "Jon's best lineup scores 124.00 and wins by 10.62. Jaylen Warren scored 34.8 and it "
           "was nowhere near enough.",
        2: "Four weeks of Brian Robinson on the bench: 5.66, 7.70, 13.16, 25.20. Week 5, Barrett "
           "finally started him: 4.04, on sixteen rushing yards. The bench was the only thing "
           "holding him together. Barrett also picked up Oronde Gadsden on Sunday afternoon and "
           "started him at flex for 0.00, the second week in a row a Barrett flex has scored zero "
           "(Ladd McConkey, who did it last week, scored 0.00 again from the bench). Kendre Miller "
           "scored 9.0 on the bench. Barrett won by 8.10 and cleared the median by 0.92, after "
           "clearing it by 0.26 and then 0.56. He is 9-1 and nobody can explain it. Nishil got "
           "39.46 out of Drake Maye, the best start of the week, and lost both games anyway. He "
           "started the Commanders, a Wednesday free agent, for 9.86 while the Seahawks scored "
           "14.52 on his bench. He paid $21 for Will Shipley (7.8). Chase Brown ($44) scored 5.5. "
           "Nishil is 1-9 and 0-5 against the median.",
        10: "Chris is 10-0, went 13-0 in all-play and posted the high score of the week, 156.98. "
            "Jahmyr Gibbs scored 37.2 and Josh Allen ran for 121 yards. Chris has spent $5 of "
            "FAAB all season and claimed two more players this week for $0. Anuj scored 146.36, "
            "the fourth-highest score of the week, went 10-3 in all-play, and lost to the one "
            "team that mattered. He still won his first game of the season, against the median, "
            "by 7.76. Puka Nacua caught 17 balls. Anuj also picked up Jauan Jennings at 12:06 on "
            "Sunday and started him at flex: 0.00. His best lineup scores 149.76 and still loses. "
            "1-9. The milk has turned into something that resembles a team, a week too late to "
            "matter against this opponent.",
        1: "Andrew started the right quarterback for the second week running: Dak Prescott 14.64, "
           "Jalen Hurts 13.00 on the bench. This time it paid. Bucky Irving scored 32.5, "
           "Christian Watson 30.3, and Andrew went 2-0 for the first time since Week 3. He found "
           "new places to hide points instead: J.K. Dobbins 14.4 and Kyle Pitts 12.7 on the bench, "
           "Jeremiyah Love 2.2 at flex and Harold Fannin 0.9 at tight end. 24.00 points of regret, "
           "the most in the league, in a 12.52-point win. Darrius missed the median by 0.58 and "
           "went 0-2. His best lineup clears it: Keenan Allen's 7.0 on the bench for DK Metcalf's "
           "3.8, Jaylen Wright's 3.22 for RJ Harvey's 0.7. Darrius has scored 691.40 points, the "
           "second most in the league, and is 4-6. His best-lineup record is 8-2. He has the "
           "worst luck in the league, and this week he helped it.",
        12: "Greg (Miley) played a perfect lineup: 100.0 percent efficiency, every call correct. "
            "That is because his entire bench was on bye. Tetairoa McMillan, Rashee Rice, Brycen "
            "Tremayne, Bryce Young and Jalen Coker scored zero between them and could not have "
            "been started if he tried. He even started the right quarterback, Jared Goff 28.94, "
            "because Bryce Young was not playing. Remove Greg's choices and he gets every one "
            "right. He scored 108.10 and lost by 37.20. Abhishek snapped a run of three straight "
            "0-2 weeks behind Isaiah Likely, 11 catches and two touchdowns for 26.9, and Mike "
            "Evans' 23.8. He still found a way: Carnell Tate, 8.8 on his bench in Week 3, started "
            "at flex this week and scored 1.1, with Josh Cameron's 7.52 on the bench. Dameon "
            "Pierce, a Saturday free agent, started and scored 3.16.",
        4: "The biggest margin of the week. Jayden Daniels ran for two touchdowns and 33.26 and "
           "Nathan played a 99.3 percent lineup, with CeeDee Lamb's 1.9 the only stain. Kenyon "
           "Sadiq, the $18 tight end who scored 0.00 as a starter last week, scored -0.70 on the "
           "bench this week. Benching him was the best call Nathan made. 9-1, 5-0 head to head, "
           "$7 of FAAB, none of it spent. Greg (IR) went from 12-1 in all-play last week to 0-13 "
           "this week, the league low at 104.30. He started Roman Wilson, the receiver whose 15.9 "
           "on the bench cost him last week, and Roman Wilson scored 0.00. He paid $8 for Blake "
           "Corum and benched him for 14.7. He paid another $8 for Adonai Mitchell, the player "
           "Jon started in Week 3 for exactly zero, and Mitchell scored zero again. Greg is on 32 "
           "moves. His best lineup scores 122.90 and still goes 0-2.",
    },

    "sections": {
        "awards": "Fourteen citations, one per team. Leo the Cleo's is a formality.",
        "power": "Season to date: record, points, all-play and this week's form, weighted, with "
                 "movement from last week. Best lineup is the record each team would own if it "
                 "had started its best legal lineup every week, everyone else exactly as they "
                 "played. The tax is the difference: wins left on your own bench.",
        "median": "Week 5's line was 138.60, the highest of the season for the second straight "
                  "week. Tom made it by 0.42. Will, his opponent, missed it by 0.42. Anuj lost his game and "
                  "won his first game of the year here; Maclane won his game and lost here by "
                  "25.22. Right of the line is a win.",
        "standings": "Week 5 scoring, both results, and how much of your own roster you managed "
                     "to start. Efficiency is what you scored over what your best legal lineup "
                     "would have scored. Injured reserve does not count against you. Neither, "
                     "it turns out, does a bench full of byes.",
        "bench": "129.24 points of lineup regret this week, down from 192.64. The cleanest week "
                 "of the season, and it still included a 383-yard quarterback on a bench.",
        "faab": "Every dollar of Week 5, audited. Maclane spent $66 of it in one run. Will spent "
                "$15 on a quarterback to bench. Greg (IR) made six adds. This is a receipt, not a "
                "shopping list.",
        "money": "Auction dollars against everything each player has scored so far, started or "
                 "not. A.J. Brown: $45, 4.1 points, still $10.98 a point.",
        "studs": "The best and worst starts of Week 5, measured against what Yahoo thought they "
                 "would do. CeeDee Lamb cost $52 and caught two balls for nine yards.",
        "games": "The long version, closest game first.",
    },

    "blurbs": {
        10: "10-0, 13-0 in all-play, the high score of the week and $95 of FAAB still unspent. "
            "Nobody in this league has figured out how to make Chris spend money or lose a game.",
        5: "9-1. Paid $9 for Jacoby Brissett with Mahomes on bye and got 25.78. Cleared the median "
           "by 0.42. Tom's waiver receipts: $7 Emanuel Wilson, $9 Brissett, both starters, both hits.",
        2: "9-1. Finally started Brian Robinson: 4.04. Started a Sunday free agent at flex: 0.00. "
           "Cleared the median by 0.92. Barrett does everything wrong in the most profitable way "
           "available.",
        4: "9-1, 5-0 head to head, $7 of FAAB and no plans for it. Benched Kenyon Sadiq for -0.70, "
           "the best $18 decision of his season.",
        1: "Right quarterback two weeks running, 2-0, up three spots. Also 24.00 points of bench "
           "regret, the most in the league. Andrew plugged one leak and drilled two more.",
        6: "691.40 points, second most in the league, 4-6. Missed the median by 0.58 with Keenan "
           "Allen on the bench again. Best-lineup record 8-2. The best team nobody is scared of.",
        8: "$66 of FAAB in one night, 113.38 points, and a win, because the schedule handed him "
           "Jon. 1-1 on the week, $16 left, down two spots.",
        12: "First 2-0 since Week 1, behind Isaiah Likely's 26.9. Still started Carnell Tate for "
            "1.1. Up three spots. The man who runs this website is 4-6 and has started calling it "
            "a run.",
        14: "12-1 in all-play last week, 0-13 this week, league low. Started Roman Wilson after "
            "benching his 15.9 and got 0.00. 32 moves. $8 on Adonai Mitchell, the league's "
            "most reliable zero.",
        9: "First win of the season, against the median, by 7.76. Scored 146.36 and lost the "
           "game anyway. Jauan Jennings, Sunday pickup, started at flex: 0.00. 1-9.",
        3: "Paid $15 for Matthew Stafford, benched 383 yards, lost by 0.84. Boston and McLaurin on "
           "the bench too. Best-lineup record 7-3, real record 2-8. Will has built a good team "
           "and refuses to play it.",
        11: "Perfect lineup, 100.0 percent, because the whole bench was on bye. Scored 108.10 and "
            "lost by 37.20. Take away Greg's choices and he gets every one right. Still 2-8.",
        13: "Benched Sam Darnold for Bo Nix again, wrong again, by 2.38 this time. T.J. Watt "
            "scored zero. 1-12 in all-play. The preseason number one is now 13th.",
        7: "Drake Maye, 39.46, best start of the week. 0-2 anyway. Seahawks 14.52 on the bench. "
           "1-9 and 0-5 against the median. Nishil finally has a quarterback and nothing to "
           "put around him.",
    },

    "awards": [
        {"title": "Bench Graduate",
         "winner": "A dad",
         "line": "Brian Robinson on the bench: 5.66, 7.70, 13.16, 25.20. Brian Robinson in the "
                 "lineup: 4.04. Barrett finally listened and got charged for it. Still 2-0."},
        {"title": "Stafford, Benched Again",
         "winner": "Good Will Hunting",
         "line": "$15 on waivers at 3:19 on Sunday morning, benched by kickoff: 383 yards, three "
                 "touchdowns, 27.32. Lost by 0.84. Greg (Miley) benched Stafford's 390 yards in "
                 "Week 3. Will has now matched him."},
        {"title": "Perfect, Technically",
         "winner": "Miley 💨LEO 5K Speedo Fan Club",
         "line": "100.0 percent efficiency. Every bench player on bye, so every decision made "
                 "itself. 108.10 points and a 37.20-point loss."},
        {"title": "Fifty-Eight Cents",
         "winner": "Bend The Knee 🐲🔥",
         "line": "Missed the median by 0.58 with Keenan Allen's 7.0 on the bench. Second-most "
                 "points in the league. 4-6."},
        {"title": "Forty-Two Cents",
         "winner": "The Asshouse Always Wins",
         "line": "Cleared the median by 0.42 and won by 0.84, with Deebo Samuel's 3.5 at flex and "
                 "Khalil Shakir's 9.5 on the bench. The house got away with one."},
        {"title": "Sixty-Six Dollars, One Night",
         "winner": "Mac Daddy",
         "line": "$41 Keon Coleman (7.2), $21 Dohnte Meyers (7.36, benched), $4 Aaron Rodgers "
                 "(22.00). The cheapest one worked. $16 left for twelve weeks."},
        {"title": "Twelve And One, Then Zero And Thirteen",
         "winner": "The Injured Reserved",
         "line": "Last week he beat every team but one. This week he beat nobody. Started Roman "
                 "Wilson for 0.00 a week after benching his 15.9, and paid $8 for Adonai Mitchell "
                 "to score zero for a second franchise."},
        {"title": "First Win, Technically",
         "winner": "Whole Milk 🥛",
         "line": "Lost to the undefeated team by 10.62, beat the median by 7.76. A win is a win. "
                 "The first one took five weeks."},
        {"title": "Five Touchdowns, Zero Wins",
         "winner": "FreeGucci",
         "line": "Drake Maye: 374 yards, five total touchdowns, 39.46, the best start in the "
                 "league. FreeGucci went 0-2."},
        {"title": "Darnold Over Nix, The Sequel",
         "winner": "Fwamming Gwaggon",
         "line": "Benched the $20 quarterback for Bo Nix again. Darnold outscored him again, by "
                 "2.38. Best lineup wins by 10.62. Lost by 7.86."},
        {"title": "Right Quarterback, Wrong Everything Else",
         "winner": "Hail Mary",
         "line": "Dak over Hurts, correct for the second week running. Then 27.1 points of "
                 "Dobbins and Pitts on the bench while Love and Fannin started for 3.1."},
        {"title": "Snapped It",
         "winner": "ShakeNBake",
         "line": "Three straight 0-2 weeks, then a 2-0 by 37.20. Isaiah Likely, 26.9. Carnell "
                 "Tate, 8.8 on the bench in Week 3, started this week for 1.1."},
        {"title": "Ten And Oh",
         "winner": "Leo the Cleo",
         "line": "13-0 in all-play, the high score, $0 spent this week. Same award as last week, "
                 "two more wins."},
        {"title": "Best Bench Decision Of The Week",
         "winner": "Kim Jong Nate",
         "line": "Kenyon Sadiq, $18: 0.00 as a starter in Week 4, -0.70 on the bench in Week 5. "
                 "Nathan learns. Slowly, and only about tight ends."},
    ],

    "waiver_note": (
        "Week 6 waivers process Tuesday night. Maclane has $16, Nathan has $7, Chris has $95 and "
        "no reason to touch it. None of this is advice. Start Matthew Stafford, Will. Or don't. "
        "Somebody in this league will bench him either way."
    ),
}

WEEK6 = {
    "headline": "Kim Jong Nate Played A Perfect Lineup. It Scored 81.54.",
    "video": {
        "src": "video/2026-wk06.mp4",
        "poster": "video/2026-wk06.jpg",
        "seconds": 42,
        "title": "Week 6 in 42 seconds",
        "blurb": "All fourteen teams, a perfect lineup that lost, an empty roster spot, a 26.96 "
                 "quarterback on the bench of a 12-0 team. Sound on.",
    },
    "kicker": "(100.0 percent efficiency, 2-11 in all-play, 0-2. Four of his bench players did not play.)",
    "lede": (
        "Nathan made every correct decision available to him and scored 81.54, because the "
        "decisions available to him were Austin Ekeler, Trevor Etienne and Brian Thomas Jr., "
        "all three picked up this week, all three started, 4.96 points between them. His bench "
        "was four players who did not play and an empty slot. First 0-2 week of his season. The median fell to "
        "113.97, the lowest line of the year, 24.63 below last week's. Greg (Miley) cleared it "
        "by 2.35 and Andrew missed it by 2.35, with Caleb Williams' 16.5 on his bench. Nishil "
        "made nine adds and still left his IDP slot empty. Jon finally started the right "
        "quarterback and scored the league low anyway. Chris benched a 26.96 quarterback and "
        "is 12-0. Barrett scored 170.18 and is 11-1. Abhishek played a perfect lineup too, and "
        "his was worth 164.80."
    ),

    "games": {
        5: "The closest game of the week, and nobody in it played well. Nathan scored 81.54 with "
           "a perfect lineup: Judkins, Tyler Warren, Ollie Gordon and Justin Jefferson, none "
           "of whom played, and one roster spot empty. So he started what he bought. Austin Ekeler, a Saturday "
           "free agent, 1.7. Trevor Etienne, a Sunday free agent, 3.26. Brian Thomas Jr., "
           "claimed for $0 after Jon cut him, 0.00 at flex, a week after scoring 1.0 for Jon "
           "from one solo tackle. Brandon Aubrey kicked one extra point: 1.0. Kenyon Sadiq "
           "started again: 1.7. Tom scored 95.16 and won by 13.62 with Derrick Henry ($45) at "
           "4.5 and Tyler Higbee, a Sunday pickup, at 2.2 in the flex. Tom missed the median by "
           "18.81, 3-10 in all-play, and is 10-2 on a five-game head-to-head streak. The house "
           "does not need to be good. It needs you to be worse.",
        8: "Maclane's $41 receiver finally paid: Keon Coleman, 13.9 and a touchdown. Then he "
           "started KaVontae Turpin at flex for 1.0, the same Turpin who sat on ShakeNBake's "
           "bench in Week 1 and returned 194 yards against him in Week 4. Rico Dowdle scored "
           "6.4 on the bench. Cameron Dicker made 53 yards of field goals for 5.3. None of it "
           "mattered, because Will is 2-10. Will finally started Matthew Stafford, after "
           "benching his 383 yards last week: 16.88. Then he did the receiver thing in reverse. "
           "Week 5: Romeo Doubs started for 2.1, Terry McLaurin (10.2) and Denzel Boston "
           "(12.62) on the bench. Week 6: McLaurin started for 3.2, Boston for 2.0, Doubs on "
           "the bench for 10.7. Will is not unlucky. He is perfectly wrong, on a one-week "
           "delay. 0-2, four straight losses, best-lineup record 7-5.",
        6: "Darrius went 2-0 and still left 39.5 points on his bench: Alvin Kamara 13.9, Stefon "
           "Diggs 13.4, Keenan Allen 12.2, while Michael Wilson (5.2) and Parker Washington "
           "(8.68) started. Keenan Allen has now been benched for 7.0 and 12.2 in back-to-back "
           "weeks. Darrius has the third-most points in the league, a 10-2 best-lineup record, a "
           "6-6 real one and the worst luck index in the league at -1.92. Anuj got 24.2 from Tre "
           "Tucker and 13.8 from Hunter Henry, a Thursday free agent, and lost by 32.10 anyway. "
           "He started Emmett Johnson at flex (5.4) with Jerry Jeudy (8.9) on the bench. Six "
           "straight head-to-head losses. 0-6 against actual teams, 1-5 against a number. 1-11.",
        2: "Barrett scored 170.18, the high score of the week, 13-0 in all-play, 98.7 percent "
           "efficient. Brian Robinson went back to the bench and scored 2.56 there, the first "
           "correct Brian Robinson decision of the season. Kenneth Walker 27.9. Chiefs, $4 on "
           "waivers, 15.74. He also paid $3 for Michael Pittman and sent him straight to IR, and "
           "$12 for Kimani Vidal to bench him. 11-1, 6-0 against the median, best-lineup record "
           "12-0. Greg (IR) lost by 45.80 and still went 1-1, because 124.38 was 10.41 above "
           "the lowest median of the season. Germie Bernard, $21 on waivers, started and scored "
           "20.2: the best FAAB dollar of the week. Blake Corum scored 13.0 on his bench, a week "
           "after scoring 14.7 on his bench. Juwan Johnson started at tight end for 0.00. 33 moves.",
        11: "Greg (Miley) played a perfect lineup for the second straight week. Last week it was "
            "because his whole bench was on bye. This week Cam Skattebo ($21) scored 0.00 at "
            "running back and the lineup was still perfect, because nobody on the bench could "
            "have replaced him. Trey Smack, picked up at 12:21 on Sunday, kicked for 11.8. "
            "Travis Hunter scored 19.9 in the IDP slot by catching a touchdown. 116.32, cleared "
            "the median by 2.35. Jon started Deshaun Watson, a Wednesday free agent, over Bo Nix: "
            "9.46 to 4.48. After two straight weeks of benching the wrong quarterback, Jon got one right. He scored "
            "68.94, the league low, 0-13 in all-play. Bijan Robinson ($69) scored 6.3 with "
            "minus eight receiving yards. Michael Mayer scored 14.0 on the bench while Rashod "
            "Bateman started at flex for 0.00. Chris Godwin, $21 on waivers, benched, 5.7. "
            "T.J. Watt scored 1.0, an improvement on last week.",
        10: "Chris benched Tyler Shough, who threw three touchdowns and ran one in for 26.96, and "
            "started Josh Allen, 18.30. Wrong by 8.66. He also had Jahmyr Gibbs on bye. He won "
            "by 50.12. Malik Nabers 25.5, the Saints, a Wednesday free agent, 17.62. 12-0, six "
            "straight, $95 of FAAB untouched. Nishil scored 75.04, 1-12 in all-play. He made "
            "nine adds this week and did not put anybody in his IDP slot. It sat empty all "
            "Sunday. He picked up Najee Harris at 9:11 on Sunday morning and started him: 0.20, "
            "on two rushing yards. Roschon Johnson, picked up Wednesday, scored 13.5 on the "
            "bench. Nishil is "
            "1-11, 0-6 against the median, and has made 30 moves to get there.",
        12: "Abhishek played a perfect lineup: 164.80, 100.0 percent, 12-1 in all-play, beaten "
            "only by Barrett. Trevor Lawrence threw four touchdowns for 28.34, the best start of "
            "the week. Jaylin Noel, projected for 5.99, scored 22.38 at flex. Carnell Tate, 1.1 "
            "at flex last week, scored 16.0. The 49ers and Evan Williams, both Wednesday free "
            "agents, both started. He also picked up Jordan Addison at 9:15 on Sunday morning, "
            "with the Vikings on bye. Andrew missed the median by 2.35 and Caleb Williams scored "
            "16.5 on his bench while Dak Prescott started for 13.02. The quarterback alone clears "
            "the median. Kyle Pitts caught two touchdowns on the bench for 20.5 while Harold "
            "Fannin started at tight end for 1.4. Last week: Pitts 12.7 on the bench, Fannin 0.9 "
            "starting. 24.68 points of regret, the most in the league for the second straight week.",
    },

    "sections": {
        "awards": "Fourteen citations. Three perfect lineups this week, and they finished 2-0, "
                  "2-0 and 0-2.",
        "power": "Season to date: record, points, all-play and this week's form, weighted, with "
                 "movement from last week. Best lineup is the record each team would own if it "
                 "had started its best legal lineup every week, everyone else exactly as they "
                 "played. The tax is the difference: wins left on your own bench.",
        "median": "Week 6's line was 113.97, the lowest of the season, a week after the highest. "
                  "Greg (Miley) made it by 2.35. Andrew missed it by 2.35 with a better "
                  "quarterback on his bench. Greg (IR) lost his game by 45.80 and got a win here "
                  "anyway; Tom won his game with 95.16 and lost here by 18.81. Right of the line "
                  "is a win.",
        "standings": "Week 6 scoring, both results, and how much of your own roster you managed "
                     "to start. Efficiency is what you scored over what your best legal lineup "
                     "would have scored. Injured reserve does not count against you. Players who "
                     "did not play do not either, which is how 81.54 rates as perfect.",
        "bench": "126.46 points of lineup regret this week, down from 129.24. Andrew and Nishil "
                 "account for 43.68 of it. Leo the Cleo benched the best quarterback on his own "
                 "roster and nobody could punish him for it.",
        "faab": "Every dollar of Week 6, audited. $70 spent, 40 adds. Germie Bernard ($21) "
                "returned 20.2. Chris Godwin ($21) returned 5.7 from the bench. Michael Pittman "
                "($3) went straight to IR. Nishil made nine of the 40 adds.",
        "money": "Auction dollars against everything each player has scored so far, started or "
                 "not. A.J. Brown: $45, 8.3 points in six weeks, 4.2 of them this week from IR.",
        "studs": "The best and worst starts of Week 6, measured against what Yahoo thought they "
                 "would do. Bijan Robinson cost $69 and finished with minus eight receiving yards.",
        "games": "The long version, closest game first.",
    },

    "blurbs": {
        10: "12-0, six straight. Benched Tyler Shough's 26.96 for Josh Allen's 18.30 and won by "
            "50.12. $95 of FAAB, still in the wrapper.",
        2: "170.18, the high score, 13-0 in all-play. Benched Brian Robinson at the right time "
           "for once. 11-1, 6-0 against the median, best-lineup record 12-0.",
        5: "Scored 95.16, 3-10 in all-play, missed the median by 18.81, and won anyway because "
           "Nathan scored 81.54. 10-2. Five straight head-to-head wins, at least one of them earned.",
        6: "2-0 with 39.5 points on the bench, Keenan Allen's 12.2 among them. Third-most points "
           "in the league, 6-6, best-lineup record 10-2, worst luck in the league.",
        12: "Perfect lineup, 164.80, 12-1 in all-play. Second straight 2-0. Also picked up a "
            "Viking on Sunday morning during the Vikings' bye. Up three spots.",
        8: "Keon Coleman finally earned some of his $41. KaVontae Turpin, at flex: 1.0. 2-0, four "
           "straight, 8-4 on $16 of FAAB.",
        4: "Perfect lineup, 81.54, 0-2. Started three players he picked up this week for 4.96 "
           "combined. First 0-2 of the season and a three-spot fall.",
        1: "Missed the median by 2.35 with Caleb Williams' 16.5 on the bench. Kyle Pitts' 20.5 "
           "too, again. Most bench regret in the league two weeks running. Down three.",
        14: "Lost by 45.80, beat the median by 10.41. Germie Bernard ($21) delivered 20.2. Blake "
            "Corum delivered 13.0 to the bench, again. 33 moves.",
        11: "Perfect lineup two weeks running, and this time it counted: 2-0. Cam Skattebo "
            "scored zero and it was still the best lineup available. Up two spots.",
        9: "Six straight head-to-head losses. Tre Tucker 24.2, Hunter Henry 13.8, Jeudy 8.9 on "
           "the bench. 1-11, and the milk is past its date.",
        3: "Started Stafford this week, benched Doubs this week, and Doubs scored the touchdown. "
           "Will makes every right decision exactly one week late. 2-10, four straight losses.",
        13: "Finally started the right quarterback, scored 68.94, 0-13 in "
            "all-play. Bijan ($69): 6.3. Mayer 14.0 on the bench, Bateman 0.00 at flex.",
        7: "Nine adds, 30 moves, an empty IDP slot. Started a Sunday-morning Najee Harris for "
           "0.20. 1-11, 0-6 against the median. Busiest manager in the league, least to show.",
    },

    "awards": [
        {"title": "Perfect, And Still 0-2",
         "winner": "Kim Jong Nate",
         "line": "100.0 percent efficiency, 81.54 points, 2-11 in all-play. Four bench players who "
                 "did not play, one empty slot, three new pickups started for 4.96 combined."},
        {"title": "Perfect, And Actually Good",
         "winner": "ShakeNBake",
         "line": "100.0 percent, 164.80, 12-1 in all-play. Jaylin Noel, projected for 5.99, at "
                 "flex for 22.38. The other perfect lineup this week lost by 13.62."},
        {"title": "Perfect, Again",
         "winner": "Miley 💨LEO 5K Speedo Fan Club",
         "line": "Second straight 100.0 percent week. Cam Skattebo scored zero in it. Cleared the "
                 "median by 2.35, which is the part that mattered."},
        {"title": "Benched The Wrong Quarterback, Won By Fifty",
         "winner": "Leo the Cleo",
         "line": "Tyler Shough 26.96 on the bench, Josh Allen 18.30 starting, Gibbs on bye. Won "
                 "by 50.12. 12-0. The rest of the league cannot even capitalize on his mistakes."},
        {"title": "The Quarterback Was On The Bench",
         "winner": "Hail Mary",
         "line": "Caleb Williams 16.5 on the bench, Dak Prescott 13.02 starting, median missed by "
                 "2.35. The swap alone clears it. Plus Kyle Pitts' two touchdowns, benched."},
        {"title": "Nobody At Linebacker",
         "winner": "FreeGucci",
         "line": "Nine adds in one week. The IDP slot stayed empty. Najee Harris, added at 9:11 "
                 "on Sunday and started: 0.20."},
        {"title": "One Week Late, Every Week",
         "winner": "Good Will Hunting",
         "line": "Benched Stafford's 27.32 last week, started his 16.88 this week. Started Doubs "
                 "for 2.1 last week, benched his 10.7 this week. 2-10."},
        {"title": "High Score, No Notes",
         "winner": "A dad",
         "line": "170.18, 13-0 in all-play, 98.7 percent. Benched Brian Robinson the one week he "
                 "deserved it. Best-lineup record 12-0."},
        {"title": "Right Quarterback, Wrong Everything",
         "winner": "Fwamming Gwaggon",
         "line": "Deshaun Watson over Bo Nix, correct by 4.98, after two weeks of Nix over the "
                 "better quarterback. League low 68.94. 0-13 in all-play."},
        {"title": "The Third Option",
         "winner": "Bend The Knee 🐲🔥",
         "line": "Kamara 13.9, Diggs 13.4 and Keenan Allen 12.2 on the bench. Won both games "
                 "anyway. Best-lineup record 10-2, real record 6-6."},
        {"title": "Twenty-One Dollars Well Spent",
         "winner": "The Injured Reserved",
         "line": "Germie Bernard, $21 on waivers, started, 20.2. Lost by 45.80 and won the median "
                 "by 10.41. Corum on the bench for 13.0, again."},
        {"title": "Won With 95",
         "winner": "The Asshouse Always Wins",
         "line": "95.16 points, 3-10 in all-play, a 13.62-point win. Derrick Henry ($45), 4.5. "
                 "Ten wins, and the schedule is starting to look like a co-manager."},
        {"title": "Former Employee Of The Week",
         "winner": "Mac Daddy",
         "line": "KaVontae Turpin, cut by ShakeNBake, started at flex: 1.0. Keon Coleman, $41, "
                 "finally scored a touchdown. 2-0 on four straight wins."},
        {"title": "0-6",
         "winner": "Whole Milk 🥛",
         "line": "Six head-to-head games, six losses. Tre Tucker caught two touchdowns this week. "
                 "Lost by 32.10."},
    ],

    "waiver_note": (
        "Week 7 waivers process Tuesday night. Chris has $95 and a 12-0 record, so he will "
        "probably not bid. Nathan has $7 and a bench that did not play a down in Week 6. Nishil has $65 and, as of Sunday, an open IDP slot. None of this is advice."
    ),
}

WEEK7 = {
    "headline": "Whole Milk Won A Game. It Was Against The Guy Who Runs This Website.",
    "video": {
        "src": "video/2026-wk07.mp4",
        "poster": "video/2026-wk07.jpg",
        "seconds": 43,
        "title": "Week 7 in 43 seconds",
        "blurb": "All fourteen teams, two perfect lineups playing each other, a tie to the hundredth, "
                 "a receiver added on his own bye week twice, and the first Whole Milk win. Sound on.",
    },
    "kicker": "(85.48, league low, 0-13 in all-play. Anuj still went 1-1: the median sunk him by 1.41.)",
    "lede": (
        "Anuj lost his first six head-to-head games. In Week 7 he drew Abhishek, who scored 85.48, "
        "the league low, with Trevor Lawrence on bye, a quarterback picked up at 6:26 on Tuesday "
        "morning and 34.86 points of running backs on his bench. Anuj won by 35.66, then missed "
        "the median by 1.41 and went 1-1 anyway. Barrett cleared it by 1.41 and is 7-0 against it. "
        "Will played a perfect lineup and lost by 1.62 to Nathan, who also played a perfect lineup. "
        "Greg (Miley) played his third perfect lineup in a row. Andrew scored 169.12 and benched "
        "the better quarterback for the second straight week, the other one this time. Maclane "
        "and Jon scored exactly 118.08 each. Chris is 14-0."
    ),

    "games": {
        4: "Two perfect lineups, one game. Nathan picked up Kirk Cousins on Thursday afternoon with "
           "Jayden Daniels on bye and got 20.4. Quinshon Judkins, who did not play a down for him "
           "last week, scored 22.9. CeeDee Lamb, two catches for nine yards in Week 5, caught two "
           "touchdowns. Wan'Dale Robinson ($0) scored 2.7 at flex and Pat Freiermuth, a Saturday "
           "pickup, 3.0 at tight end, and both were still the best available, because four of "
           "Nathan's five bench players scored zero. 136.72, 100.0 percent. Will matched him "
           "decision for decision: Joe Burrow started for 28.88 with Matthew Stafford's 18.5 on "
           "the bench, the first time Will has had two quarterbacks playing and started the "
           "better one. He paid $40 for DeMario Douglas, the biggest bid of the week, and benched him "
           "correctly for 3.8. KC Concepcion, 1.0 in Week 5, scored 20.2. The Jets defense, "
           "projected for 13.61, scored 3.7. 135.10, 100.0 percent, lost by 1.62. Will is finally "
           "on time and it did not help. The median saved him by 12.55. Five straight head-to-head "
           "losses, $10 of FAAB left.",
        10: "Chris had Josh Allen on bye, so Tyler Shough started and scored 14.82. Tony Pollard "
            "scored three touchdowns at flex, 36.00 on a 13.37 projection, the best start of the "
            "week. Chris picked up Colby Parkinson at 11:22 on Saturday, benched him for 8.3 and "
            "started Jake Ferguson at tight end for 0.00. Xavier Hutchinson scored 13.36 on the "
            "bench. 86.6 percent, cleared the median by 1.95, 14-0, seven straight. Greg (IR) "
            "picked up Jacoby Brissett at 3:58 on Saturday afternoon, benched him for 16.48 and "
            "started Brock Purdy, who threw two interceptions for 14.02. Adonai Mitchell started at "
            "flex and scored 0.00, the league's most reliable zero, still reliable. Jalen Coker "
            "scored 1.4 at the other flex, with Dylan Sampson (9.2) and Jonah Coleman ($3, 7.9) on "
            "the bench. Greg's best lineup scores 135.52 and wins by 11.02. Blake Corum finally "
            "started and scored 16.6. Four straight losses, 37 moves.",
        7: "Nishil filled his IDP slot this week. Alex Singleton, a $0 claim, scored 17.5 in it. "
           "Omar Cooper ($16) scored 21.0, Drake Maye 28.44, and Nishil won his first game against "
           "the median all season, by 7.93. Then the bench: Caleb Douglas, a Tuesday free agent, "
           "two catches, two touchdowns, 20.0, benched. Makai Lemon, picked up at 7:50 on Monday "
           "morning, benched, 16.2 that night. Roschon Johnson, who scored 13.5 on the bench last "
           "week, started this week and scored 1.3. 28.10 points of regret, the most in the "
           "league. Darrius played a 98.7 percent lineup and lost both games. Keenan Allen, benched "
           "for 7.0 and then 12.2, started at flex this week and scored 5.6. The Ravens allowed 35 "
           "and scored 3.18. Darrius has the third-most points in the league, a 6-8 record and "
           "the worst luck index in the league at -2.00.",
        11: "Greg (Miley) played his third straight perfect lineup. Cam Skattebo went from 0.00 "
            "last week to 19.6. Javonte Williams ran for 155 yards, Trey McBride scored 23.1 and "
            "Nick Bolton, a Saturday pickup, 8.5 in the IDP slot. 137.06, 12-1 in all-play. Greg's "
            "best-lineup record is 11-3 and his real one is 6-8, because the first four weeks still "
            "count. Maclane scored 118.08. So did Jon, to the hundredth, in a different game. Both "
            "went 0-2 and both missed the median by 4.47. Maclane started Eddy Pineiro, a Friday "
            "pickup, with Cameron Dicker on bye: 3.0. He started the Colts (11.8) over the Vikings "
            "(12.16). Garrett Wilson scored 3.6. Tee Higgins scored 24.8 and it was nowhere near "
            "enough. The four-game winning streak is over.",
        2: "Barrett cleared the median by 1.41, the smallest margin of the week, and is 7-0 against "
           "it. Kenneth Walker ($43) scored 7.7, Xavier Worthy 2.6 and Matthew Golden 6.9, while "
           "Devaughn Vele scored 13.9 on the bench. Braelon Allen, $1 in the auction, scored 17.4. "
           "123.96 was enough because Tom scored 96.08, 1-12 in all-play, and missed the median by "
           "26.47. Derrick Henry ($45) ran for 45 yards. Tom paid $11 for Kyler Murray and started "
           "him over Patrick Mahomes, correct by 6.90, and it did not matter. The house went 0-2 for "
           "the first time all season and its five-game head-to-head streak is over. Barrett is "
           "13-1 and his best-lineup record is 14-0.",
        9: "Six head-to-head games, six losses. Then Anuj drew Abhishek. Geno Smith scored 24.48, "
           "Rhamondre Stevenson 20.0, Tre Tucker 19.8, and Whole Milk won its first real game of "
           "the season by 35.66. Then it missed the median by 1.41 and went 1-1. Emmett Johnson: "
           "started for 5.4 last week with Jerry Jeudy's 8.9 on the bench, benched this week for "
           "6.94 while MarShawn Lloyd started for 4.5. That swap alone clears the median. Abhishek "
           "scored 85.48, the league low, 0-13 in all-play, a week after a perfect 164.80. Trevor "
           "Lawrence was on bye, so Abhishek picked up Tanner McKee at 5:39 on Tuesday morning and "
           "J.J. McCarthy at 6:26, and McCarthy scored 10.18. Nico Collins ($43) caught two balls "
           "for six yards. Jaylin Noel, 22.38 last week, scored 1.98 at flex. Isaiah Likely 2.2. "
           "Dameon Pierce (12.78), Kaelon Black (11.76) and Tyrone Tracy (10.32) were all on the "
           "bench. Even the best lineup loses by 12.44.",
        1: "Andrew scored 169.12, the high score of the week, 13-0 in all-play, and won by 51.04, "
           "the biggest margin of the week. He also benched the better quarterback for the second "
           "straight week. Week 6: Dak Prescott started for 13.02, Caleb Williams 16.5 on the "
           "bench. Week 7: Caleb started for 22.12, Dak 23.28 on the bench. Kyle Pitts scored 10.7 "
           "on the bench, his third straight week there: 12.7, 20.5, 10.7. On Saturday Andrew "
           "added Antonio Williams at 9:28, Makai Lemon at 12:26 and Antonio Williams again at "
           "6:24. Antonio Williams plays for Washington, who were on bye. Lemon was gone by "
           "Monday morning and scored 16.2 that night on Nishil's bench. Jon started Bo Nix over "
           "Deshaun Watson, 26.28 to 19.22, the right quarterback two weeks running, and lost by "
           "51.04. Dontayvion Wicks started at flex for 0.00. A.J. Brown ($45) scored 6.3 and has "
           "14.6 points in seven weeks. 3-11, three straight losses, last in the power rankings.",
    },

    "sections": {
        "awards": "Fourteen citations. Three more perfect lineups, and two of them played each "
                  "other.",
        "power": "Season to date: record, points, all-play and this week's form, weighted, with "
                 "movement from last week. Best lineup is the record each team would own if it "
                 "had started its best legal lineup every week, everyone else exactly as they "
                 "played. The tax is the difference: wins left on your own bench.",
        "median": "Week 7's line was 122.55. Barrett made it by 1.41. Anuj missed it by 1.41, in "
                  "the week he finally won a game. Will lost his game by 1.62 and got a win here "
                  "anyway; Anuj won his and lost here. Maclane and Jon missed it by the same 4.47. "
                  "Right of the line is a win.",
        "standings": "Week 7 scoring, both results, and how much of your own roster you managed "
                     "to start. Efficiency is what you scored over what your best legal lineup "
                     "would have scored. Injured reserve does not count against you. Three teams "
                     "hit 100.0 percent and went 2-0, 2-0 and 1-1.",
        "bench": "125.46 points of lineup regret this week, down from 126.46. One point of "
                 "progress, league-wide, in a week. Nishil and Abhishek account for 51.32 of it.",
        "faab": "Every dollar of Week 7, audited. $81 spent, 41 adds. Will spent $40 of it on a "
                "receiver he benched for 3.8. Nishil spent $16 on one who scored 21.0. Andrew "
                "added a Commanders receiver during the Commanders' bye. Twice.",
        "money": "Auction dollars against everything each player has scored so far, started or "
                 "not. A.J. Brown: $45, 14.6 points in seven weeks.",
        "studs": "The best and worst starts of Week 7, measured against what Yahoo thought they "
                 "would do. Nico Collins cost $43 and caught two balls for six yards.",
        "games": "The long version, closest game first.",
    },

    "blurbs": {
        10: "14-0, seven straight. Started Jake Ferguson for 0.00 the day after picking up a tight "
            "end, and still cleared the median. $95 of FAAB, now a museum piece.",
        2: "13-1, 7-0 against the median, cleared it by 1.41 this week. Best-lineup record 14-0. "
           "Barrett no longer needs to be good, just slightly above the middle.",
        1: "169.12, 13-0 in all-play, up five. Benched the wrong quarterback again, the other one "
           "this time. Added a receiver on his own bye week. Twice.",
        4: "Perfect lineup, beat another perfect lineup by 1.62. 11-3 and the best luck in the "
           "league. Up three.",
        5: "96.08, 1-12 in all-play, five-game streak over. Derrick Henry ($45): 5.4. Down two. "
           "First week all year the house had to pay out.",
        6: "98.7 percent, 0-2. Started Keenan Allen the one week he scored 5.6. Third-most points, "
           "6-8, worst luck in the league.",
        8: "118.08, the same score as Jon to the hundredth. 0-2, streak over. Started a Friday "
           "kicker for 3.0.",
        11: "Third straight perfect lineup, 137.06, 12-1 in all-play. Skattebo from 0.00 to 19.6. "
            "Up two.",
        14: "Benched a 16.48 quarterback he picked up Saturday, started Purdy's two picks. Adonai "
            "Mitchell at flex: 0.00. Four straight losses, 37 moves.",
        12: "85.48, league low, 0-13, lost to the 1-11 team. Down five. The man who runs this "
            "website has stopped calling it a run.",
        3: "Perfect lineup, right quarterback, correct $40 benching. Lost by 1.62. Five straight "
           "head-to-head losses. Will is finally on time and it does not help.",
        9: "First head-to-head win of the season, by 35.66. Missed the median by 1.41, so 1-1. "
           "Benched Emmett Johnson the week he outscored his starter. 2-12.",
        7: "2-0, first median win all year, IDP slot occupied. Also 28.10 points on the bench, "
           "most in the league. 3-11, 36 moves.",
        13: "Right quarterback two weeks running, lost by 51.04. Tied Maclane at 118.08 for the "
            "league's most average failure. 3-11, last.",
    },

    "awards": [
        {"title": "Perfect Beats Perfect",
         "winner": "Kim Jong Nate",
         "line": "100.0 percent against Will's 100.0 percent. Kirk Cousins, a Thursday free agent, "
                 "20.4. Won by 1.62. Last week his perfect lineup scored 81.54. This one counted."},
        {"title": "Perfect, And Still Lost",
         "winner": "Good Will Hunting",
         "line": "Burrow 28.88 started, Stafford 18.5 benched, the $40 receiver benched for 3.8. "
                 "Every call right. Lost by 1.62. Saved by the median."},
        {"title": "Perfect, Three Straight",
         "winner": "Miley 💨LEO 5K Speedo Fan Club",
         "line": "Third 100.0 percent week in a row. Cam Skattebo went from 0.00 to 19.6. Best-lineup "
                 "record 11-3, real record 6-8."},
        {"title": "First Blood",
         "winner": "Whole Milk 🥛",
         "line": "0-6 head to head, then a 35.66-point win. Then missed the median by 1.41. Seven "
                 "weeks, one real win, and the median took half of it back."},
        {"title": "Lost To The Milk",
         "winner": "ShakeNBake",
         "line": "85.48, league low, 0-13 in all-play. Two quarterbacks added 47 minutes apart on "
                 "Tuesday morning; J.J. McCarthy scored 10.18. 34.86 points of running backs on "
                 "the bench."},
        {"title": "Wrong Quarterback, Both Directions",
         "winner": "Hail Mary",
         "line": "Week 6: Dak started, Caleb benched, wrong. Week 7: Caleb started, Dak benched for "
                 "23.28, wrong by 1.16. Won by 51.04 anyway."},
        {"title": "Monday Morning Receiver",
         "winner": "FreeGucci",
         "line": "Makai Lemon, added at 7:50 on Monday morning, benched, 16.2 that night. Caleb "
                 "Douglas 20.0 on the bench. 28.10 points of regret. Still 2-0."},
        {"title": "Tied To The Hundredth",
         "winner": "Mac Daddy",
         "line": "118.08. Jon scored 118.08. Both 0-2, both missed the median by 4.47. Eddy Pineiro, "
                 "a Friday pickup, kicked for 3.0."},
        {"title": "Right Quarterback, Lost By Fifty-One",
         "winner": "Fwamming Gwaggon",
         "line": "Bo Nix 26.28 over Deshaun Watson 19.22, correct two weeks running. Dontayvion Wicks "
                 "at flex: 0.00. Lost by 51.04. Last in the power rankings."},
        {"title": "Fourteen And Oh",
         "winner": "Leo the Cleo",
         "line": "Started Jake Ferguson at tight end for 0.00 with a Saturday pickup on the bench. "
                 "Tony Pollard, 36.00 at flex. Nothing he does is punished."},
        {"title": "Closest Call, Still A Win",
         "winner": "A dad",
         "line": "Cleared the median by 1.41, the smallest margin of the week. 7-0 against it. Even "
                 "Barrett's close calls go his way."},
        {"title": "The Keenan Allen Experience",
         "winner": "Bend The Knee 🐲🔥",
         "line": "On the bench: 7.0, 12.2. In the lineup: 5.6. 98.7 percent efficient, 0-2, worst "
                 "luck in the league at -2.00."},
        {"title": "Brissett, Benched",
         "winner": "The Injured Reserved",
         "line": "Added Jacoby Brissett at 3:58 on Saturday, benched his 16.48 for Purdy's two "
                 "picks. Adonai Mitchell at flex: 0.00. Best lineup wins by 11.02."},
        {"title": "The House Paid Out",
         "winner": "The Asshouse Always Wins",
         "line": "96.08, 1-12 in all-play, missed the median by 26.47. Derrick Henry ($45), 5.4. "
                 "First 0-2 of the season."},
    ],

    "waiver_note": (
        "Week 8 waivers process Tuesday night. Chris has $95 and a 14-0 record. Will has $10 "
        "left after a $40 bench piece. Nathan has $7. None of this is advice. Andrew, check the "
        "bye weeks before you add a receiver. Twice."
    ),
}

NOTES = {1: WEEK1, 2: WEEK2, 3: WEEK3, 4: WEEK4, 5: WEEK5, 6: WEEK6, 7: WEEK7}
