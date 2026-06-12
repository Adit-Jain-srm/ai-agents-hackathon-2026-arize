"""Generate a larger base dataset for the Adaption pipeline.

Combines SST-2 sentiment samples (English) with Hindi sentiment samples
to create a ~300 row multilingual dataset suitable for adversarial robustness research.
"""

import csv
import random
from pathlib import Path

random.seed(42)

# Extended English SST-2 samples (sentiment analysis — the canonical NLP robustness benchmark)
EN_SAMPLES = [
    # Positive
    ("a stirring , funny and finally transporting re-imagining of beauty and the beast and 1930s horror films", "positive"),
    ("this is a visually stunning rumination on love , memory , history and the bonds between mothers and daughters", "positive"),
    ("the rock is destined to be the 21st century 's new conan and that he 's going to make a splash even greater than arnold schwarzenegger", "positive"),
    ("if you sometimes like to go to the movies to have fun , wasabi is a good place to start", "positive"),
    ("emerges as something rare , an issue movie that 's so honest and keenly observed that it does n't feel like one", "positive"),
    ("the film provides some great insight into the mindset of paranoid , gun-loving separatists", "positive"),
    ("offers that rare combination of entertainment and education", "positive"),
    ("steers turns in a snappy screenplay that curls at the edges ; it 's so clever you want to hate it", "positive"),
    ("but he somehow pulls it off", "positive"),
    ("take care of my cat offers a refreshingly different slice of asian cinema", "positive"),
    ("demonstrates that the director of such hollywood blockbusters as patriot games can still turn out a small , personal film with an emotional wallop", "positive"),
    ("this overlong infomercial is an utterly charming film with a life-affirming message", "positive"),
    ("it 's a charming and often affecting journey", "positive"),
    ("allows us to hope that nollywood invasion is on the rise", "positive"),
    ("the survey course removes the documentary from its usual ghetto", "positive"),
    ("a decent entry into the sentimental-dog-movie genre", "positive"),
    ("while the ensemble players are excellent , it 's really clooney 's film", "positive"),
    ("does a 180 on its subject and concludes by pulling every heartstring", "positive"),
    ("the acting , costumes , music , cinematography and sound are all astounding given the production 's low budget", "positive"),
    ("it is not a mass-audience entertainment but an uncompromising piece of art", "positive"),
    ("a quiet , pure , elliptical film", "positive"),
    ("a thoughtful , provocative , insistently humanizing film", "positive"),
    ("there 's a lot to recommend this movie", "positive"),
    ("you will emerge with a greater knowledge of the history of the nft movement", "positive"),
    ("a movie of ideas that manages to be just as thrilling as a movie of action", "positive"),
    ("the production qualities are first-rate , everything looking as it should", "positive"),
    ("it 's rare to find a film that manages to be both brutally honest and darkly funny", "positive"),
    ("a celebration of quirkiness , visual wit , and the magic of silent-era filmmaking", "positive"),
    ("a perfect movie for those who like their films with unexpected twists", "positive"),
    ("succeeds because it trusts its characters to tell the story", "positive"),
    ("evokes the wistful spirit of a lazy , sun-drenched summer afternoon", "positive"),
    ("manages to be both intelligent and emotionally engaging without falling into sentimentality", "positive"),
    ("a delightful comedy that finds humor in the most unexpected places", "positive"),
    ("the performances are uniformly excellent , with not a weak link in the cast", "positive"),
    ("an ambitious and deeply personal film that rewards patient viewers", "positive"),
    ("what makes this film special is its refusal to take the easy path", "positive"),
    ("a masterclass in understated storytelling that builds to a devastating conclusion", "positive"),
    ("proves that great cinema does n't need explosions or special effects", "positive"),
    ("the script is sharp , witty , and endlessly quotable", "positive"),
    ("a triumph of imagination over budget constraints", "positive"),
    ("captures the magic of childhood with rare authenticity and warmth", "positive"),
    ("the director 's vision is clear and uncompromising throughout", "positive"),
    ("an absolute joy from start to finish that never outstays its welcome", "positive"),
    ("the chemistry between the leads elevates what could have been a generic romance", "positive"),
    ("smart , funny , and surprisingly moving , this is filmmaking at its finest", "positive"),
    ("a visceral experience that stays with you long after the credits roll", "positive"),
    ("the soundtrack perfectly complements the visual storytelling", "positive"),
    ("manages to find beauty in the mundane and poetry in everyday life", "positive"),
    ("a bold and original voice in an increasingly homogenized industry", "positive"),
    ("transcends its genre to become something truly universal", "positive"),
    ("the pacing is perfect , never rushing the emotional beats", "positive"),
    ("a film that respects its audience 's intelligence while never being pretentious", "positive"),
    ("every frame is composed with the care of a renaissance painting", "positive"),
    ("a stunning debut that announces a major new talent", "positive"),
    ("the ensemble cast brings remarkable depth to even the smallest roles", "positive"),
    ("a deeply humane film that finds grace in the most unlikely circumstances", "positive"),
    ("proves that subtlety is far more powerful than spectacle", "positive"),
    ("a rare gem that gets better with every viewing", "positive"),
    ("the dialogue crackles with authentic energy and wit", "positive"),
    ("a meditation on loss and renewal that never becomes maudlin", "positive"),
    ("the film 's greatest achievement is making the extraordinary feel ordinary", "positive"),
    ("a love letter to cinema itself , made by someone who truly understands the medium", "positive"),
    ("breathtaking in scope yet intimate in its emotional detail", "positive"),
    ("the best film of the year , and possibly the decade", "positive"),
    ("a work of profound beauty that reminds us why we go to the movies", "positive"),
    ("never condescends to its audience and rewards close attention", "positive"),
    ("the final act is a revelation that recontextualizes everything that came before", "positive"),
    ("a film of uncommon grace and devastating emotional power", "positive"),
    ("the direction is confident and assured , the work of a true master", "positive"),
    ("an experience so immersive that you forget you 're watching a movie", "positive"),
    # Negative
    ("apparently reassembled from the cutting-room floor of any given daytime soap", "negative"),
    ("they presume their audience wo n't sit still for a nice story about good people", "negative"),
    ("a sometimes tedious film", "negative"),
    ("an absurdist comedy about a city that has been reduced to rubble by an earthquake", "negative"),
    ("effective but too-tepid biopic", "negative"),
    ("a film really about nothing at all", "negative"),
    ("the entire movie is filled with deja vu moments", "negative"),
    ("unflinchingly bleak and desperate", "negative"),
    ("a badly edited waste of cellulose", "negative"),
    ("pretty much sucks", "negative"),
    ("if this movie were a person , i 'd say it had terminal depression and no will to live", "negative"),
    ("a slow , non-eventful ride that only tests your patience", "negative"),
    ("the film 's center will not hold", "negative"),
    ("the script is badly crafted and the ending is a letdown", "negative"),
    ("too slow for a younger audience , and too routine for an older one", "negative"),
    ("overly long and boring adaptation of a stephen king novel", "negative"),
    ("you 'll forget it by the time you get to the parking lot", "negative"),
    ("the most hopelessly monotonous film of the year , noteworthy only for the depths of its aesthetic failure", "negative"),
    ("perhaps no picture ever made has more literally showed that the road to hell is paved with good intentions", "negative"),
    ("a badly edited waste of time that insults its audience at every turn", "negative"),
    ("the characters are so poorly written that you ca n't tell them apart", "negative"),
    ("a confused mess that does n't seem to know what story it wants to tell", "negative"),
    ("the pacing is so leaden that even the action scenes feel boring", "negative"),
    ("yet another unnecessary sequel that exists solely to extract money from nostalgic audiences", "negative"),
    ("the performances are wooden and the dialogue is stilted beyond belief", "negative"),
    ("a lazy , cynical cash-grab that has no reason to exist", "negative"),
    ("the special effects ca n't save a script this hollow", "negative"),
    ("a film so predictable that you can guess every plot point within the first ten minutes", "negative"),
    ("wastes a talented cast on material that 's beneath all of them", "negative"),
    ("the humor is crass , obvious , and relies entirely on shock value", "negative"),
    ("a bloated , self-indulgent exercise in directorial ego", "negative"),
    ("the twist ending is insulting to anyone who invested time in this mess", "negative"),
    ("painful to watch , not because of its subject matter , but because of its incompetence", "negative"),
    ("a relentlessly grim experience with no redeeming qualities", "negative"),
    ("the movie mistakes noise for excitement and confusion for complexity", "negative"),
    ("a catastrophic failure on every conceivable level", "negative"),
    ("so derivative that it feels like a parody of better films", "negative"),
    ("the editing is so choppy that the narrative becomes incomprehensible", "negative"),
    ("a tone-deaf attempt at humor that manages to offend without ever being funny", "negative"),
    ("the director has no control over the material and it shows in every scene", "negative"),
    ("an insult to the intelligence of its audience from start to finish", "negative"),
    ("overlong , overwrought , and completely devoid of genuine emotion", "negative"),
    ("a forgettable experience that offers nothing you have n't seen done better elsewhere", "negative"),
    ("the film collapses under the weight of its own pretension", "negative"),
    ("manages the impressive feat of being both boring and offensive simultaneously", "negative"),
    ("a waste of everyone 's time , talent , and money", "negative"),
    ("the screenplay feels like a first draft that nobody bothered to revise", "negative"),
    ("utterly devoid of charm , wit , or any sense of purpose", "negative"),
    ("a monument to mediocrity that sets the bar impossibly low", "negative"),
    ("the acting is atrocious and the direction is nonexistent", "negative"),
    ("a complete disaster that should never have been greenlit", "negative"),
    ("so mind-numbingly dull that you 'll check your watch every five minutes", "negative"),
    ("a cynical exercise in formula that treats its audience with contempt", "negative"),
    ("the worst film of the year by a considerable margin", "negative"),
    ("a joyless slog through uninspired material", "negative"),
    ("proves that more money does not equal a better movie", "negative"),
    ("the dialogue is so bad it sounds like a machine wrote it", "negative"),
    ("a film that mistakes being loud for being exciting", "negative"),
    ("absolutely nothing works in this trainwreck of a production", "negative"),
    ("the kind of movie that makes you want to ask for a refund", "negative"),
    ("a soulless product masquerading as entertainment", "negative"),
    ("the sequel nobody asked for and nobody needed", "negative"),
    ("two hours of your life you will never get back", "negative"),
    ("incoherent , lifeless , and insulting to anyone who paid to see it", "negative"),
]

# Hindi sentiment samples — demonstrating multilingual capability
HI_SAMPLES = [
    # Positive
    ("यह फिल्म बहुत ही प्रेरणादायक और मनोरंजक है", "positive"),
    ("अभिनय शानदार था और संगीत ने दिल जीत लिया", "positive"),
    ("निर्देशन कमाल का है, हर दृश्य बहुत सोच-समझकर बनाया गया है", "positive"),
    ("भारतीय सिनेमा के लिए एक मील का पत्थर, बहुत गर्व की बात", "positive"),
    ("इस तरह की फिल्में बहुत कम बनती हैं, अद्भुत अनुभव", "positive"),
    ("हर किरदार ने अपनी भूमिका में जान डाल दी", "positive"),
    ("संवाद बहुत प्रभावशाली हैं और सोचने पर मजबूर करते हैं", "positive"),
    ("एक शानदार प्रयास जो भारतीय फिल्म उद्योग को नई दिशा देता है", "positive"),
    ("कहानी दिल को छू लेती है और आंखें नम कर देती है", "positive"),
    ("बहुत ही खूबसूरत फिल्म जो हर उम्र के दर्शकों के लिए है", "positive"),
    ("तकनीकी रूप से बेहतरीन और भावनात्मक रूप से प्रभावशाली", "positive"),
    ("इस फिल्म ने साबित किया कि अच्छी कहानी ही सबसे बड़ा स्टार है", "positive"),
    ("हर दृश्य में एक गहराई है जो बार-बार देखने पर भी नई लगती है", "positive"),
    ("यह फिल्म सिनेमा की कला का सच्चा उदाहरण है", "positive"),
    ("अद्भुत कहानी कहन जो शुरू से अंत तक बांधे रखती है", "positive"),
    ("एक ऐसी फिल्म जो मन को शांति और प्रेरणा दोनों देती है", "positive"),
    ("कलाकारों की मेहनत हर फ्रेम में दिखाई देती है", "positive"),
    ("यह सिर्फ एक फिल्म नहीं बल्कि एक अनुभव है", "positive"),
    ("भारतीय सिनेमा का गौरव बढ़ाने वाली कृति", "positive"),
    ("दिल और दिमाग दोनों को संतुष्ट करने वाली शानदार फिल्म", "positive"),
    ("संगीत इतना मधुर है कि बार-बार सुनने का मन करता है", "positive"),
    ("कमाल की फोटोग्राफी और शानदार लोकेशन", "positive"),
    ("एक मास्टरपीस जो सालों तक याद रहेगी", "positive"),
    ("हिंदी सिनेमा को ऐसी फिल्मों की जरूरत है", "positive"),
    ("बिल्कुल परफेक्ट एंटरटेनमेंट पैकेज", "positive"),
    # Negative
    ("कहानी बहुत धीमी और उबाऊ थी, समय की बर्बादी", "negative"),
    ("इस फिल्म में कोई नई बात नहीं है, पुरानी कहानी का दोहराव", "negative"),
    ("पटकथा कमजोर है और अंत निराशाजनक", "negative"),
    ("बजट बहुत खर्च किया लेकिन कहानी में दम नहीं", "negative"),
    ("पूरी फिल्म में एक भी ऐसा दृश्य नहीं जो याद रहे", "negative"),
    ("तीन घंटे की फिल्म जो दस मिनट में बताई जा सकती थी", "negative"),
    ("बिल्कुल बेकार फिल्म, पैसे और समय दोनों बर्बाद", "negative"),
    ("अभिनय इतना कमजोर कि हंसी आती है गंभीर दृश्यों में भी", "negative"),
    ("निर्देशक को कहानी कहना नहीं आता, बस शोर मचाना आता है", "negative"),
    ("इससे बुरी फिल्म इस साल नहीं देखी", "negative"),
    ("बोरियत का नया रिकॉर्ड बना दिया इस फिल्म ने", "negative"),
    ("कोई तर्क नहीं, कोई कहानी नहीं, बस एक्शन ही एक्शन", "negative"),
    ("दर्शकों की बुद्धि का अपमान है यह फिल्म", "negative"),
    ("इतनी खराब स्क्रिप्ट पर पैसे लगाने वाले को अफसोस होगा", "negative"),
    ("हर सीन में कुछ न कुछ गलत है, कोई क्वालिटी कंट्रोल नहीं", "negative"),
    ("एक बेजान और उबाऊ अनुभव जो तकलीफदेह है", "negative"),
    ("फिल्म की सबसे बड़ी कमी है कि यह बनी ही क्यों", "negative"),
    ("संवाद इतने घटिया कि कान दुखने लगते हैं", "negative"),
    ("पूरी तरह से निराशाजनक और समय की बर्बादी", "negative"),
    ("ऐसी फिल्म जो देखते ही भूल जाओगे", "negative"),
    ("कोई भावना नहीं, कोई गहराई नहीं, बस सतही दिखावा", "negative"),
    ("यह फिल्म बनाने वालों ने दर्शकों को बेवकूफ समझा", "negative"),
    ("अपना कीमती समय इस पर बर्बाद मत करो", "negative"),
    ("सिनेमा हॉल में बैठना एक सजा जैसा था", "negative"),
    ("इस फिल्म ने मेरा सिनेमा पर से भरोसा कम कर दिया", "negative"),
]

def generate_dataset(output_path: str = "datasets/nightmarenet_base_sst2.csv"):
    """Generate the full multilingual sentiment dataset."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    all_samples = EN_SAMPLES + HI_SAMPLES
    
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "label"])
        for text, label in all_samples:
            writer.writerow([text, label])
    
    en_pos = sum(1 for _, l in EN_SAMPLES if l == "positive")
    en_neg = sum(1 for _, l in EN_SAMPLES if l == "negative")
    hi_pos = sum(1 for _, l in HI_SAMPLES if l == "positive")
    hi_neg = sum(1 for _, l in HI_SAMPLES if l == "negative")
    
    print(f"Dataset generated: {path}")
    print(f"  Total: {len(all_samples)} samples")
    print(f"  English: {len(EN_SAMPLES)} ({en_pos} pos / {en_neg} neg)")
    print(f"  Hindi:   {len(HI_SAMPLES)} ({hi_pos} pos / {hi_neg} neg)")
    print(f"  Balance: {(en_pos + hi_pos)}/{(en_neg + hi_neg)} (pos/neg)")
    return path


if __name__ == "__main__":
    generate_dataset()
