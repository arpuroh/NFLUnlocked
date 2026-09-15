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

NOTES = {
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
           "by 24. That is what happens when the man across from you pays $63 for a "
           "receiver who catches two balls for 12 yards. Will's starting lineup "
           "featured $84 of wideout producing 4.6 points while a $1 rookie put up "
           "12.9 on his bench. Zero all-play wins. Zero.",
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
         "line": "Beat Good Will Hunting by 23.70 and missed the median by 1.11. "
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
