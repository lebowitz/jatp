"""Episode shot breakdown. Each shot is one Veo clip (<=8s) with a first-frame still
prompt and a motion prompt that includes any spoken dialogue (Veo voices it).
Refs are storybook portrait slugs used as identity anchors.
Extend SHOTS scene by scene through the screenplay."""

SHOTS = [
 # ===== SCENE 1 — INT. MOLINA GARAGE STUDIO - NIGHT (touch -> jolt) =====
 dict(id="s1_01", scene=1, refs=["julie","luke","alex","reggie"],
   still="Interior garage music studio at night, warm fairy lights strung overhead; a teenage girl and a teenage boy frozen in an amazed embrace, two other teenage boys standing close and grinning; instruments around them.",
   motion='Four teenagers in a fairy-lit garage at night. The embracing pair stay still, astonished. A grinning teenage boy in a red plaid shirt teases them and says: "Are you guys gonna stand like that all night, or—" Gentle handheld, warm light.'),
 dict(id="s1_02", scene=1, refs=["julie","luke","alex"],
   still="Close two-shot of a teenage girl and teenage boy almost nose to nose, amazed and emotional, in a warm fairy-lit garage studio at night; an anxious blond teenage boy just beside them.",
   motion='In a warm garage at night, a blond teenage boy whispers in awe: "Reggie. Her hand isn\'t going right through him." The girl gently presses her palm to the boy\'s shoulder, laughs in amazement, and says: "You\'re solid. You\'re really here."'),
 dict(id="s1_03", scene=1, refs=["reggie","julie","luke","alex"],
   still="A teenage boy with dark swept-back hair throwing both arms up in pure joy in a fairy-lit garage at night; a girl and two boys laughing around him.",
   motion='A teenage boy throws both arms up and shouts with joy: "We played the Orpheum!" The others cheer and laugh, exhilarated.'),
 dict(id="s1_04", scene=1, refs=["reggie","alex"],
   still="Two teenage boys in a dim garage at night; one in a red plaid shirt reaching to high-five the other and looking a little sheepish.",
   motion='A teenage boy tries to high-five his friend, but his hand passes straight through him. He shrugs, a little sheepish, and says: "Okay, so it is just Julie. Cool. Cool cool cool."'),
 dict(id="s1_05", scene=1, refs=["julie","luke","alex","reggie"],
   still="A teenage girl stepping back to look at three teenage boys who glow very faintly in a dim garage at night, wonder and worry mixing on her face.",
   motion='A teenage girl steps back, studying the three boys in wonder, and says slowly: "We did not cross over... and you are all still here." One boy answers softly: "Here." Quiet, warm, intimate.'),
 dict(id="s1_06", scene=1, refs=["luke","julie"],
   still="Close on a teenage boy's forearm and hand in a dim garage at night; a jagged blue-white electric light crackles from a mark on his wrist; light bulbs burst in showers of sparks in the background; a girl's hand reaches in from the side. The wrist and the sparks are the subject, not faces.",
   motion='Blue-white electric light crackles violently from the mark on the wrist; the garage bulbs blow out in showers of sparks; hands recoil. A girl\'s voice cries out off-screen: "Luke?!" Chaotic and electric.'),
 dict(id="s1_07", scene=1, refs=["julie","alex","luke","reggie"],
   still="Three teenage boys collapsed and shaking on the floor of a dim garage at night; a teenage girl kneeling among them, hands hovering, frightened but determined.",
   motion='The three boys drop to the floor, shaking, as the lights buzz back dim and wrong. A weak, anxious blond boy says: "That was worse. So much worse." The girl kneels among them and says firmly: "We are going to fix this."'),

 # ===== SCENE 2 — EXT. MOLINA HOUSE FRONT WALK - NIGHT (possession) =====
 dict(id="s2_01", scene=2, refs=["caleb","nick"],
   still="Night exterior sidewalk; an elegant adult man in a sharp vintage suit stands facing the camera under a streetlight, mid-sentence; in the foreground, the back of a young man's head and shoulders, seen from behind. Moody, cinematic.",
   motion='An elegant adult man in a vintage suit steps from the streetlight haze and addresses the young man whose back is to the camera. The man says smoothly: "How sweet. The broken-hearted boy. Fighting for his girl." Slow and ominous.'),
 dict(id="s2_02", scene=2, refs=["caleb","nick"],
   still="Night; an elegant adult man under a streetlight, facing the camera with a faint knowing smile; the other person is a dark over-the-shoulder silhouette in the foreground. Moody.",
   motion='Over the foreground silhouette\'s shoulder, the elegant adult man smiles. A wary voice asks off-camera: "Do I know you?" The man replies smoothly: "You will." Quietly menacing.'),
 dict(id="s2_03", scene=2, refs=["caleb","nick"],
   still="Night; a golden light flares from an elegant man's wrist and streams toward a teenage boy who stiffens upright; eerie, dramatic.",
   motion='A golden mark flares on the man\'s wrist and light pours into the teenage boy, who straightens as his expression turns cold and amused. In a changed, older voice the boy says: "I have a fight too." Eerie and dramatic.'),
 dict(id="s2_04", scene=2, refs=["nick"],
   still="Extreme close-up of a single human eye in night shadow, a faint cold golden light flickering within the iris; the rest of the face lost in darkness. Mysterious.",
   motion='Extreme close-up of an eye in shadow; a cold golden light flickers and grows within it. A calm, changed voice says: "Hi, Nick." Then everything cuts to black. Sinister.'),

 # ===== SCENE 3 — INT. MOLINA KITCHEN - MORNING (Ray/Carlos comedy, Julie) =====
 dict(id="s3_01", scene=3, refs=["ray","carlos"],
   still="A sunny family kitchen in the morning; a cheerful dad flipping an egg in a pan at the stove; a twelve-year-old boy at the counter holding up a homemade gadget made of a smoke detector, a flashlight, and a baby monitor taped together. Warm, bright.",
   motion='A sunlit kitchen. The dad flips an egg and asks, "Carlos. What is that?" The boy holds up his homemade gadget proudly and says, "EMF reader. Paranormal activity in this house is up four hundred percent." Light comedy, warm.'),
 dict(id="s3_02", scene=3, refs=["ray","carlos"],
   still="A sunny kitchen; a dad at the stove giving a dry, unimpressed look; in the foreground a homemade gadget (smoke detector, flashlight, and baby monitor taped together) held up toward a window, beeping. Focus on the dad and the gadget.",
   motion='The dad at the stove says dryly, "Mm. And down four hundred percent in doing the dishes." The gadget, waved toward the window, suddenly shrieks loudly and the dad fumbles his egg in surprise. Comedic, warm.'),
 dict(id="s3_03", scene=3, refs=["ray","carlos"],
   still="A sunny kitchen; a dad crouched on the floor scraping a dropped fried egg off the tile, deadpan; a beeping homemade gadget at the edge of the frame.",
   motion='An excited young voice cries off to the side, "Did you hear that?!" The dad, crouched scraping the dropped egg off the floor, says flatly, "That is the smoke detector, mijo. Because of the eggs." Deadpan comedy.'),
 dict(id="s3_04", scene=3, refs=["julie","ray"],
   still="A tired teenage girl coming into a sunny kitchen and kissing her cheerful dad on the cheek; warm morning light.",
   motion='A tired teenage girl comes in and kisses her dad on the cheek. He beams and says warmly, "There she is. My big hologram star. Your tia thinks it is special effects. I told her my daughter is an artist." Warm.'),
 dict(id="s3_05", scene=3, refs=["ray","julie"],
   still="A warm sunny kitchen, relaxed wide two-shot: a kind dad at the counter turning toward his tired teenage daughter with gentle concern; both fully in frame.",
   motion='The girl gives a faint, tired smile and says, "Thanks, Dad." The dad softens, looking at her warmly, and says gently, "You okay? You have got your mom\'s look — the one she got when a song was not finished yet." A warm, tender beat.'),
 dict(id="s3_06", scene=3, refs=["julie","carlos"],
   still="A sunny kitchen; a teenage girl rushing out the door toward the garage in the background; in the foreground a homemade gadget on the counter lighting up and beeping.",
   motion='The girl grabs a banana and hurries out toward the garage as the homemade gadget on the counter lights up and screams again. A young voice says, vindicated, "Artist. Sure." Comedic button.'),
]
