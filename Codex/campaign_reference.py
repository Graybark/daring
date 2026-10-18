"""Campaign events to add to the OneNote reference, with session provenance.

Each fact describes play recorded in a numbered session. Entries absent from the
OneNote reference become new reference pages in the browser.
"""

from __future__ import annotations

from collections.abc import Iterable


Fact = tuple[str, tuple[int, ...]]


CAMPAIGN: dict[tuple[str, str], list[Fact]] = {
    # Existing character pages: developments after, or clearer in, the session log.
    ("Characters", "Glasstaff"): [
        ("He aided the party against a Death Tyrant in Wave Echo Cave and died during the fight.", (42,)),
    ],
    ("Characters", "Black Spider"): [
        ("He hired the party to defeat a Death Tyrant in Wave Echo Cave and later offered them work in Leilon.", (42, 43)),
        ("Using Yalda's blood, he grew a duplicate body and transferred Zzara'kath's consciousness into it. His research then located the Nightwalker on its plane.", (131, 132)),
    ],
    ("Characters", "Varos"): [
        ("At the Shard of the Moon, he resurrected Klyde after the fight with Vaeril.", (113,)),
    ],
    ("Characters", "Cornelius"): [
        ("He gave up personal memories to the mirror of Shar for power. Fragments of his husband remained.", (70,)),
        ("Selûne's intervention brought him into the battle with Veylar's shadow dragon echo; he later fought Ularan Mortus with Dark Star.", (104, 118)),
    ],
    ("Characters", "Dagult Neverember"): [
        ("Cornelius returned to Lord Neverember after the party learned Veylar was a dragon and was arrested there.", (100,)),
    ],
    ("Characters", "Mariel Thornton"): [
        ("The party gave her credit for saving guests at the Sleeping Giant Inn, then freed her from Veylar's Geas.", (99,)),
    ],
    ("Characters", "Cedric Thornton"): [
        ("He asked the party for evidence of the danger in Neverwinter Wood. After they showed him the fungal threat, he agreed to approach his sister.", (91, 97)),
        ("The party later teleported to him to rest safely after the battle for Waterdeep.", (126,)),
    ],
    ("Characters", "Veylar"): [
        ("He altered Woodruff's memory and secretly controlled Mariel Thornton. The party later learned he was an ancient green dragon infected by an echo from another world.", (90, 99, 100)),
        ("His shadow dragon echo was defeated in the Shadowfell. He was later trapped in the Necrofungal Colossus, and the party used Wish to bring him out.", (104, 105, 128, 129)),
    ],
    ("Characters", "Ogron"): [
        ("A subordinate of Captain Harrows, he quietly contacted the party and shared what he knew about deaths among Neverwinter's soldiers.", (93,)),
    ],
    ("Characters", "Woodruff"): [
        ("The fungal hivemind captured her; Onyx later took her into the Far Realms to fight the spores' influence. Klyde summoned her back during the battle for Waterdeep.", (95, 106, 123)),
        ("After returning, she reached Veylar and heard him say that he forgave her.", (132,)),
    ],
    ("Characters", "Yalda"): [
        ("She learned that the Nightwalker had been her patron. With Talos's help, she renounced that connection and became a level 20 sorcerer.", (132,)),
        ("The Black Spider used her blood to grow a duplicate body for Zzara'kath's consciousness.", (131, 132)),
    ],
    ("Characters", "Swift"): [
        ("When the fungal hivemind subdued much of the party, Swift's attack forced it to release Cornelius, Woodruff, and Yalda.", (95,)),
    ],
    ("Characters", "Klyde"): [
        ("He emerged from Shar's mirror in Waterdeep and joined the party.", (70,)),
        ("He died in the battle with Vaeril and was resurrected by Varos. Later, he summoned Woodruff into the battle for Waterdeep.", (113, 123)),
    ],
    ("Characters", "Green (Bridd~s, Bridds)"): [
        ("Green joined after the Nightwalker encounter in the Mere of Dead Men. In the fungal battle, Bridds was grafted into a hulk; the party preserved a finger.", (64, 96)),
    ],
    ("Characters", "Gundren Rockseeker"): [
        ("The party repeatedly tried to rescue him from Cragmaw Castle but could not find him there.", (7, 9, 12)),
    ],
    ("Characters", "Friyola"): [
        ("She was one of the original companions in Phandalin and distrusted Sildar's promise of payment.", (1, 2)),
    ],
    ("Characters", "Sildar Hallwinter"): [
        ("The party escorted him to Phandalin, where he arranged their reward. He later gave them leads on nearby threats.", (2, 19)),
    ],
    ("Characters", "Halia Thornton"): [
        ("She invited the party to the Miner's Exchange and later gave Dio a task to watch religious cults and gain influence in Leilon.", (13, 30)),
    ],
    ("Characters", "Eed"): [
        ("Eed magically charmed Harbin Wester into paying the party extra, later dealt with Agatha, and eventually wandered off while the party slept.", (6, 22, 49)),
    ],
    ("Characters", "Dio"): [
        ("He performed with Bradwick in Phandalin and died in the Nightwalker encounter in the Mere of Dead Men.", (28, 63)),
    ],
    ("Characters", "Aersius"): [
        ("A Death Tyrant petrified her in Wave Echo Cave. Merrygold restored her, after which she left the party.", (42, 49)),
    ],
    ("Characters", "Bradwick"): [
        ("He helped the party defeat King Grol and later died while they defended travelers at a roadside inn.", (12, 44)),
    ],
    ("Characters", "Hyppolite"): [
        ("He traveled to Phandalin with Keth Thok and later met Cornelius, who joined the party's trip to the Dwarven Excavation Site.", (1, 3)),
    ],
    ("Characters", "Zzara'kath"): [
        ("The illithid consciousness in Yalda's ring was transferred into the duplicate body made from Yalda's blood.", (131, 132)),
    ],
    ("Characters", "Hamun Kost"): [
        ("He identified the Nightwalker's influence on Cornelius and helped him decipher Bowgentle's spell.", (23, 24, 25)),
    ],
    ("Characters", "Thalivar"): [
        ("The party confronted his ghost in the House of Thalivar and freed it from the Material Plane.", (51, 52)),
    ],
    ("Characters", "Druknar Ironmind"): [
        ("He joined the party in the duergar mines and explained the mind flayers' control over his people.", (76,)),
    ],
    ("Characters", "Keth Thok"): [
        ("He helped Hyppolite survive a goblin ambush, then traveled with him to Phandalin while searching for clues about his mother.", (1,)),
    ],
    ("Characters", "Slinn Dancer"): [
        ("Fleeing the Cassalanter family, Slinn joined the party at the Dwarven Excavation Site and nearly died fighting an ochre jelly.", (5, 6)),
    ],
    ("Characters", "Harbin Wester"): [
        ("He paid the party for clearing the Dwarven Excavation Site; Eed charmed him into paying extra. He also offered a task against orcs at Wyvern Tor.", (6, 19)),
    ],
    ("Characters", "Bren"): [
        ("The Session 14 notes say Bren pointed the party toward the Miner's Exchange in Phandalin.", (14,)),
    ],
    ("Characters", "Thunaman"): [
        ("Hamun Kost mentioned Thunaman as an expert tattooist in Thay.", (25,)),
    ],
    ("Characters", "Silla Scalesweep"): [
        ("She and Tarbin Tul traveled with the party after seeking safety from the Hounds of Darkness.", (46,)),
    ],
    ("Characters", "Tarbin Tul"): [
        ("He and Silla Scalesweep shared the party's magical shelter while a dark form searched overhead.", (46,)),
    ],
    ("Characters", "Thalgrim"): [
        ("The duergar shaman promised aid against the Sharrans if the party helped free his people from the mind flayers.", (79,)),
    ],
    ("Characters", "Captain Harrows"): [
        ("His subordinate Ogron quietly met the party with information about deaths among Neverwinter's soldiers.", (93,)),
    ],
    ("Characters", "Elvar Kurn"): [
        ("He approached Yalda at the Sleeping Giant Inn and urged her to follow Talos. He escaped during the battle with the Hounds of Darkness.", (98, 99)),
    ],
    ("Characters", "Onyx"): [
        ("He helped in the battle with the fungal hivemind, absorbed Veylar's defeated shadow dragon echo, and took Woodruff to the Far Realms.", (96, 105, 106)),
    ],
    ("Characters", "Ithrelle"): [
        ("The Raven Queen blessed her and the party before their planned fight with the Nightwalker. Her old wound from fighting undead drew Woodruff's attention.", (132,)),
    ],
    ("Characters", "Veyra Halbrune"): [
        ("As the commander defending Waterdeep, she offered the party two missions: find the source of the undead attack or destroy the vampire nest.", (108,)),
    ],
    ("Characters", "Adria"): [
        ("She lured Yalda from the party, tried to charm her, and revealed herself as a vampire when the spell failed.", (109,)),
    ],
    ("Characters", "Orien"): [
        ("The Pale Child offered to help the party against Ularan Mortus after confronting them about the death of his children.", (111,)),
    ],
    ("Characters", "Ularan Mortus"): [
        ("The party hunted him in the Mere of Dead Men, fought him and his death knights, then destroyed the circle sustaining him and defeated him with Talos cultists' help.", (112, 118, 119, 120)),
    ],
    ("Characters", "Vaeril Quenya Ara"): [
        ("Yalda's father led undead troops as a death knight. The party captured his soul and later learned it was bound to their ship; they persuaded him to release his anger.", (112, 113, 116)),
    ],
    # Existing mythology, factions, places, history, and encounter pages.
    ("Mythology", "Selûne"): [
        ("Her intervention brought Cornelius into the battle with Veylar's echo. A phial blessed by her helped the party confront Ularan Mortus.", (104, 109, 118)),
    ],
    ("Mythology", "Talos"): [
        ("Yalda sought his guidance before the mission against Ularan. He later helped her renounce the Nightwalker's patronage.", (109, 114, 132)),
    ],
    ("Mythology", "Shar"): [
        ("Her mirror in Waterdeep took Cornelius's memories in exchange for power and released Klyde. She later drew the party into a dreamlike battle royale.", (70, 80)),
    ],
    ("Factions", "Neverwinter Council"): [
        ("The party sought council support against the damage in Neverwinter Wood, and Cedric agreed to speak to Mariel after seeing their evidence.", (91, 97)),
    ],
    ("Factions", "Redbrands"): [
        ("They fought the party in Phandalin and at Tresendar Manor before the party reached Glasstaff.", (3, 17)),
    ],
    ("Culture and History", "Highharvestide"): [
        ("The notes describe Phandalin being decorated for the festival; the played portion of the session does not say whether the party joined the celebrations.", (14,)),
    ],
    ("Locations", "Negative Plane"): [
        ("After the Black Spider located the Nightwalker, the party plane-shifted and teleported into a void containing an immense steel sphere.", (132,)),
    ],
    ("Locations", "Shadowfell"): [
        ("The party tracked Veylar's shadow dragon echo there and defeated it.", (103, 104, 105)),
    ],
    ("Locations", "Neverwinter"): [
        ("The party investigated Veylar's influence over its council and later returned there after defeating the Necrofungal Colossus.", (90, 99, 130)),
    ],
    ("Locations", "Mere of Dead Men"): [
        ("The party survived a Nightwalker encounter there and later hunted Ularan Mortus behind enemy lines.", (62, 63, 112)),
    ],
    ("Locations", "Shard of the Moon"): [
        ("Varos resurrected Klyde there. After Ularan's defeat, the party discovered fungal spores had reached it.", (113, 120)),
    ],
    ("Locations", "House of Thalivar"): [
        ("The party confronted Thalivar's ghost in the tower and freed it from the Material Plane.", (50, 51, 52)),
    ],
    ("Locations", "Leilon"): [
        ("The Black Spider hired the party to free it from undead, and the party later fought cultists at the Wayside Inn on the road there.", (43, 55, 56)),
    ],
    ("Locations", "Sleeping Giant Inn"): [
        ("The party met Ogron there, fought the Hounds of Darkness, and later faced a vampire ambush.", (93, 98, 99, 101)),
    ],
    ("Encounters", "Hounds of Darkness"): [
        ("The party fought them repeatedly while the Nightwalker pursued Cornelius and later at the Sleeping Giant Inn.", (39, 46, 58, 98, 99)),
    ],
    ("Encounters", "Echo"): [
        ("The party tracked Veylar's shadow dragon echo in the Shadowfell and defeated it; Onyx absorbed what remained.", (103, 104, 105)),
    ],
    ("Encounters", "Ularan Mortus"): [
        ("The party confronted the lich and his death knights, then returned with Talos cultists to defeat him.", (117, 118, 119)),
    ],
    ("Encounters", "Waterdeep Battle"): [
        ("The undead breached Waterdeep's defenses, but the party helped restore control of the South Gate sector.", (121, 122, 123, 124, 125)),
    ],
    ("Encounters", "Necrofungal Colossus"): [
        ("It held Veylar captive. The party used Wish to draw him out and destroyed the creature, discovering it had formed around Woodruff's dispersed remains.", (128, 129)),
    ],
    # Characters named in played sessions but missing from the OneNote list.
    ("Characters", "Agatha"): [
        ("The witch bargained with Bradwick and Cornelius and stole time from the party when they visited her lair.", (22,)),
    ],
    ("Characters", "Alara"): [
        # Character detail supplied by the player; Session 97 names her but does not describe her role.
        ("Varos's right hand and a priestess of Selûne.", ()),
        ("Named in the Dramatis Personae when the party returned to Neverwinter.", (97,)),
    ],
    ("Characters", "Backes"): [
        ("The party spared this cultist after the fight at the Wayside Inn so they could question him.", (56,)),
    ],
    ("Characters", "Bergamont"): [
        ("An assassin looking for Swift appeared at the Sleeping Giant Inn.", (101,)),
    ],
    ("Characters", "Boy"): [
        ("A young tiefling followed the party through Neverwinter, befriended them, and led them to a magic-item shop.", (130,)),
    ],
    ("Characters", "Candrian of Sigil"): [
        ("His account of surviving the Negative Material Plane appears in the party's preparations for the trip there.", (131,)),
    ],
    ("Characters", "Cryovain"): [
        ("The party slew the dragon when it attacked them at Conyberry.", (20,)),
    ],
    ("Characters", "Ceddi"): [
        ("Cedric Thornton's clone accompanied Veylar to speak with Halia Thornton after the party showed Cedric evidence of the danger in Neverwinter Wood.", (97,)),
    ],
    ("Characters", "Darlan Greaves"): [
        ("The party convinced Neverwinter's guard commander that sending more soldiers into the forest would lead to needless deaths. He agreed to speak with Dagult Neverember.", (97,)),
    ],
    ("Characters", "Fheralai Stormsworn"): [
        ("The party convinced her and her Talos cultist bodyguards to join the fight against Ularan Mortus.", (119,)),
    ],
    ("Characters", "Grol"): [
        ("The goblin king attacked the party at Cragmaw Castle and was defeated with Bradwick's help.", (9, 10, 11, 12)),
    ],
    ("Characters", "Grognor"): [
        ("His betrayal confronted the party during the defense of Leilon.", (48,)),
    ],
    ("Characters", "Hanna"): [
        ("Yalda wrote to her about Cornelius's failure to remember her.", (126,)),
    ],
    ("Characters", "Captain Faras"): [
        ("Named among those involved in the party's voyage and approach to Ularan Mortus's lair.", (116, 117)),
    ],
    ("Characters", "Kerri (Crack)"): [
        ("Crack joined the party after Bradwick's burial. Kerri later investigated the Nightwalker's possible connection to Cornelius's husband and died in the Mere of Dead Men.", (45, 49, 63)),
    ],
    ("Characters", "Koshra"): [
        ("Joined Cornelius and Hyppolite on their journey to the Dwarven Excavation Site.", (4,)),
    ],
    ("Characters", "Merrygold"): [
        ("She asked the party to rescue children and fishermen in Leilon, then restored Aersius after they brought her diamond dust.", (47, 49)),
    ],
    ("Characters", "Qeline Alderleaf"): [
        ("The session notes say she told Bradwick about Reidoth, the druid who knew the region around Thundertree.", (19, 31)),
    ],
    ("Characters", "Reidoth"): [
        ("He offered to guide the party to Wave Echo Cave if they dealt with the green dragon, then accompanied them on the journey.", (35, 36, 39)),
    ],
    ("Characters", "Ser Caldrin Veyr"): [
        ("Named in the session's Dramatis Personae as one of the elite soldiers supplied for the Mere of Dead Men mission.", (109,)),
    ],
    ("Characters", "Nyssa Kael"): [
        ("Named in the session's Dramatis Personae as one of the elite soldiers supplied for the Mere of Dead Men mission.", (109,)),
    ],
    ("Characters", "Orven Dhal"): [
        ("Named in the session's Dramatis Personae as one of the elite soldiers supplied for the Mere of Dead Men mission.", (109,)),
    ],
    ("Characters", "Sister Garaele"): [
        ("The session's leads record her wish that the party ask Agatha about Bowgentle's spellbook, with a silver comb to offer as a gift.", (19,)),
    ],
    ("Characters", "Thestryl Mellardin"): [
        ("She greeted the party when Cornelius teleported them to Waterdeep's City of the Dead.", (66,)),
    ],
    ("Characters", "Thalamun"): [
        ("Bridds learned that the sword he had received from a solar was an ancient sentient weapon named Thalamun.", (97,)),
    ],
    ("Characters", "Udrok Pest-Strangler"): [
        ("The orc leader told the party where to find Cragmaw Castle.", (7,)),
    ],
    ("Characters", "Velleen"): [
        ("She fought the party near Tresendar Manor, was revived by Bradwick, and carried beads like his.", (28, 29)),
    ],
    # Other named reference subjects that emerge in the session history.
    ("Mythology", "The Raven Queen"): [
        ("She blessed Ithrelle and the party before their planned fight with the Nightwalker.", (132,)),
    ],
    ("Mythology", "Myrkul"): [
        ("The Pale Child said Myrkul had placed him under Ularan Mortus's command; Ularan's forces also served the god.", (111, 115)),
    ],
    ("Mythology", "Nightwalker"): [
        ("An avatar attacked the party in the Mere of Dead Men. Yalda later learned the Nightwalker had been her patron; the Black Spider located its plane.", (62, 63, 132)),
    ],
    ("Mythology", "Tymora"): [
        ("Eed prayed to the goddess of luck while seeking clues near Conyberry.", (19,)),
    ],
    ("Factions", "The Daring Dozen"): [
        ("The adventuring party fought threats from Phandalin to Waterdeep and is preparing to confront the Nightwalker.", (1, 125, 132)),
    ],
    ("Factions", "The Harpers"): [
        ("Cornelius used their teleportation circle in Waterdeep's City of the Dead.", (66,)),
    ],
    ("Factions", "Sharran cultists"): [
        ("They emerged through Shar's mirror after Klyde and fought the party in Waterdeep.", (70, 71)),
    ],
    ("Factions", "Talos cultists"): [
        ("They guarded the island leading to Ularan Mortus's lair. The party persuaded their leader Fheralai to turn on the lich.", (115, 117, 119)),
    ],
    ("Factions", "Many-Arrows orcs"): [
        ("The party encountered Udrok's band while traveling through Neverwinter Forest toward Cragmaw Castle.", (7,)),
    ],
    ("Factions", "Cassalanter family"): [
        ("Slinn Dancer was fleeing this family when they joined the party near the Dwarven Excavation Site.", (5,)),
    ],
    ("Factions", "Duergar villagers"): [
        ("The party found the village under mind flayer control. Thalgrim promised its aid against the Sharrans in return for help against the mind flayers.", (78, 79)),
    ],
    ("Factions", "Mind flayers"): [
        ("Their patrols controlled the duergar village. Zzara'kath, whose consciousness later occupied Yalda's ring, was part of this threat.", (76, 78, 79, 131)),
    ],
    ("Factions", "Fungal network"): [
        ("Woodruff briefly entered a symbiosis with a fungus-bound deep dragon; a later malignant network captured her and overtook much of the party.", (78, 95, 96, 98)),
    ],
    ("Culture and History", "Siege of Waterdeep"): [
        ("The undead breached the South Gate defenses. The party fought there until control of the sector was restored.", (121, 122, 123, 124, 125)),
    ],
    ("Locations", "Waterdeep"): [
        ("Cornelius brought the party there through the Harpers' circle. Later, the city endured an undead siege that the party helped repel.", (66, 108, 121, 125)),
    ],
    ("Locations", "Wave Echo Cave"): [
        ("The party met the Black Spider there, fought a Death Tyrant, and later returned for his help locating the Nightwalker.", (42, 43, 131)),
    ],
    ("Locations", "Cragmaw Castle"): [
        ("The party made repeated attempts to rescue Gundren Rockseeker there and defeated King Grol.", (7, 8, 9, 10, 11, 12)),
    ],
    ("Locations", "Cragmaw Hideout"): [
        ("The party freed Sildar Hallwinter there and escorted him back to Phandalin.", (2,)),
    ],
    ("Locations", "Tresendar Manor"): [
        ("The party fought Redbrands, a banshee, and a vampire beneath and around the manor.", (16, 17, 28, 29)),
    ],
    ("Locations", "Thundertree"): [
        ("The party met Reidoth in the ruins and fought the green dragon before he guided them onward.", (34, 35, 36)),
    ],
    ("Locations", "Conyberry"): [
        ("The party slew Cryovain there and later met Hamun Kost nearby.", (20, 23)),
    ],
    ("Locations", "Old Owl Well"): [
        ("Sildar's lead mentions strange activity around Conyberry and Old Owl Well. The recorded meeting with Hamun Kost took place at Conyberry.", (19, 23)),
    ],
    ("Locations", "Wyvern Tor"): [
        ("Harbin Wester offered the party a task to drive away orcs camping and raiding there; the notes call it optional.", (19,)),
    ],
    ("Locations", "Dragon's Barrow"): [
        ("The party stopped there on the way to Reidoth and found dancing lights above the hill.", (30,)),
    ],
    ("Locations", "Neverwinter Wood"): [
        ("The party gathered evidence of the fungal danger there and later found Veylar in trouble before the Necrofungal Colossus fight.", (95, 97, 127)),
    ],
    ("Locations", "City of the Dead"): [
        ("Cornelius brought the party to the Harpers' circle in this Waterdeep cemetery.", (66,)),
    ],
    ("Locations", "Vanrakdoom"): [
        ("Soloj Claddar showed the party an illusion of its temple and described how to reach it through the Underdark.", (73,)),
    ],
    ("Locations", "Dwarven Excavation Site"): [
        ("The early party cleared ochre jellies from the site and claimed Harbin Wester's reward.", (3, 5, 6)),
    ],
    ("Locations", "Stonehill Inn"): [
        ("The party spent a night there after returning Sildar Hallwinter to Phandalin.", (2,)),
    ],
    ("Locations", "Duergar village"): [
        ("The party hid from mind flayer patrols in its mines, met Thalgrim, and negotiated for the villagers' help.", (78, 79)),
    ],
    ("Locations", "Far Realms"): [
        ("Onyx took Woodruff there to fight the fungal spores' influence, before Klyde later summoned her back during the battle for Waterdeep.", (106, 123)),
    ],
    ("Locations", "Agatha's Lair"): [
        ("The party visited Agatha near Conyberry; her bargain with Bradwick and Cornelius cost them time.", (19, 22)),
    ],
}


def facts_for(category: str, title: str) -> Iterable[Fact]:
    return CAMPAIGN.get((category, title), ())


# PRIVATE GM PREPARATION. Roleplay portrayals and ambitions planned for Session 134.
# Do not cite these as events played at the table or disclose them in player recaps.
GM_CHARACTER_NOTES: dict[str, dict[str, str]] = {
    "The Listener": {
        "appearance": "A gaunt lich in dark robes, wearing an eyeless silver mask. Tuning forks protrude from his skeletal fingers and vibrate softly.",
        "voice": "Soft, measured, almost a whisper; clinical, unnervingly calm, and rarely raised.",
        "mannerisms": "Tilts his head as though hearing a distant sound; pauses mid-sentence; taps his forked fingers together for faint metallic chimes; studies others like specimens.",
        "gm_goal": "Wants the party's power to subdue the Nightwalker without destroying the Unmoored Anchor, which he intends to control.",
        "example": "Destroy the Nightwalker? How terribly unimaginative. Imagine what we might learn from it.",
    },
    "Morthakar, the Gilded Horn": {
        "appearance": "A towering undead vampiric minotaur with dark, patchy fur over pale leathery skin, heavy armor, a broken horn repaired with gold, dull crimson eyes, and predatory fangs.",
        "voice": "Deep, hollow, resonant, and authoritative; deliberately slow, never pausing for breath. Becomes quieter when angry.",
        "mannerisms": "Holds perfectly still while listening, never blinks, fixes speakers with an unbroken stare, and taps one heavy finger when impatient.",
        "gm_goal": "Wants the Nightwalker gone so he can restore order and regain full control of Death Heart; unlike the Listener, he has no interest in keeping the Unmoored Anchor.",
        "example": "I have maintained peace among monsters for centuries. I will not allow one more to take my city from me.",
    },
}
