def get_brewing_suggestions(varietal, process):
    """
    Generate expert brewing suggestions based on coffee varietal and processing method.
    Includes advanced parameters and specialized knowledge for coffee enthusiasts.

    Parameters:
    varietal (str): The coffee varietal (e.g., 'Bourbon', 'Gesha', 'Caturra')
    process (str): The processing method (e.g., 'Washed', 'Natural', 'Honey')

    Returns:
    dict: Comprehensive suggestions for brewing parameters
    """
    # Default suggestions - baseline for most coffees
    default_suggestions = {
        "brew_ratio": "1:16",
        "grind_size": "Medium (20-25 on Comandante)",
        "water_temp": "92-94°C (198-201°F)",
        "brew_time": "2:30 - 3:00",
        "technique": "Standard pour-over with 45s bloom, then continuous pour",
        "water_quality": "150 ppm TDS, 50-75 ppm calcium hardness, pH 7.0",
        "optimal_age": "7-14 days off roast",
        "flavor_notes": "Balanced extraction",
        "troubleshooting": "If sour, grind finer or increase temperature. If bitter, grind coarser or decrease temperature.",
        "description": "Standard balanced brewing approach suitable for most coffees.",
    }

    suggestions = default_suggestions.copy()

    # Varietal-based suggestions
    varietal = varietal.lower() if varietal else ""

    # Ethiopian varietals
    if "ethiopian" in varietal or "ethiopia" in varietal:
        if "heirloom" in varietal or "landrace" in varietal:
            suggestions.update(
                {
                    "brew_ratio": "1:16.5",
                    "grind_size": "Medium-fine (18-22 on Comandante)",
                    "water_temp": "90-93°C (194-199°F)",
                    "water_quality": "120-150 ppm TDS, lower mineral content to highlight floral notes",
                    "technique": "45-60s bloom, gentle pulse pouring technique",
                    "optimal_age": "10-21 days off roast",
                    "filter_type": "Paper filter (preferably white, oxygen-bleached)",
                    "flavor_notes": "Bergamot, jasmine, peach, blueberry, tea-like",
                    "troubleshooting": "To emphasize florals, use cooler water. For more fruit sweetness, extend brew time slightly.",
                    "description": "Ethiopian heirloom varieties often have complex floral, fruity, and tea-like characteristics. A gentler approach with cooler water helps highlight these delicate flavors.",
                }
            )
        elif "yirgacheffe" in varietal:
            suggestions.update(
                {
                    "brew_ratio": "1:16.5",
                    "grind_size": "Medium-fine (18-22 on Comandante)",
                    "water_temp": "89-92°C (192-198°F)",
                    "water_quality": "120-140 ppm TDS, softer water preferred",
                    "technique": "60s bloom, very gentle pulse pouring",
                    "optimal_age": "10-21 days off roast",
                    "filter_type": "Paper filter (preferably white, oxygen-bleached)",
                    "flavor_notes": "Citrus, bergamot, floral, lemon, honey",
                    "troubleshooting": "If florals are muted, reduce water temperature by 1-2°C",
                    "description": "Yirgacheffe coffees are prized for their distinctive floral and citrus notes. A very gentle extraction approach preserves these delicate aromatics.",
                }
            )
        elif "sidamo" in varietal:
            suggestions.update(
                {
                    "brew_ratio": "1:16",
                    "grind_size": "Medium (20-24 on Comandante)",
                    "water_temp": "90-93°C (194-199°F)",
                    "water_quality": "130-150 ppm TDS, balanced mineral content",
                    "technique": "45s bloom, gentle continuous pour",
                    "optimal_age": "7-21 days off roast",
                    "filter_type": "Paper filter (preferably white, oxygen-bleached)",
                    "flavor_notes": "Blueberry, chocolate, citrus, wine-like",
                    "troubleshooting": "If acidity is too pronounced, slightly lower water temperature",
                    "description": "Sidamo coffees typically have pronounced berry notes with wine-like acidity. A balanced approach highlights its complex characteristics.",
                }
            )
        elif "guji" in varietal:
            suggestions.update(
                {
                    "brew_ratio": "1:16.5",
                    "grind_size": "Medium-fine (18-22 on Comandante)",
                    "water_temp": "90-92°C (194-198°F)",
                    "water_quality": "120-140 ppm TDS, softer water preferred",
                    "technique": "60s bloom, very gentle pulse pouring",
                    "optimal_age": "10-21 days off roast",
                    "filter_type": "Paper filter (preferably white, oxygen-bleached)",
                    "flavor_notes": "Stone fruit, floral, tea-like, complex berry",
                    "troubleshooting": "For more sweetness, try a 1:16 ratio and extend brew time slightly",
                    "description": "Guji coffees are renowned for their complex stone fruit notes and floral aromatics. A gentle extraction approach highlights these nuanced characteristics.",
                }
            )

    # Gesha/Geisha varietals
    elif "gesha" in varietal or "geisha" in varietal:
        suggestions.update(
            {
                "brew_ratio": "1:17",
                "grind_size": "Medium-fine (18-22 on Comandante)",
                "water_temp": "90-92°C (194-198°F)",
                "water_quality": "100-130 ppm TDS, lower mineral content to highlight florals",
                "technique": "Gentle pour with extended bloom time (45-60s), then slow pulse pours",
                "optimal_age": "10-21 days off roast",
                "filter_type": "Paper filter (preferably white, oxygen-bleached)",
                "flavor_notes": "Jasmine, bergamot, peach, tropical fruit, tea-like",
                "pour_technique": "Extremely gentle, 6-7g of water per second maximum flow rate",
                "troubleshooting": "If tea-like notes are muted, reduce temperature by 2°C. If lacking sweetness, try 1:16.5 ratio.",
                "description": "Gesha/Geisha varietals are known for their delicate floral and tea-like qualities. A gentler extraction with slightly cooler water helps highlight these nuanced flavors. Worth treating with exceptional care.",
            }
        )
        # Specific origin Geshas
        if "panama" in varietal:
            suggestions.update(
                {
                    "water_temp": "89-91°C (192-196°F)",
                    "water_quality": "100-120 ppm TDS, very soft water preferred",
                    "flavor_notes": "Jasmine, bergamot, tropical fruits, honey, exceptional clarity",
                    "description": "Panamanian Gesha is the benchmark for this varietal, with unmatched clarity and floral complexity. Extremely gentle extraction with cooler water preserves its delicate characteristics.",
                }
            )
        elif "colombia" in varietal:
            suggestions.update(
                {
                    "water_temp": "90-93°C (194-199°F)",
                    "flavor_notes": "Jasmine, stone fruit, citrus, maple syrup",
                    "description": "Colombian Gesha typically shows more body and sweetness than Panamanian counterparts, with stone fruit complimenting the floral notes.",
                }
            )
        elif "ethiopia" in varietal:
            suggestions.update(
                {
                    "water_temp": "90-92°C (194-198°F)",
                    "flavor_notes": "Bergamot, complex florals, tropical fruit, honey",
                    "description": "Ethiopian Gesha combines the varietal's floral complexity with Ethiopia's distinctive terroir for an exceptionally aromatic cup.",
                }
            )

    # Bourbon varieties
    elif "bourbon" in varietal:
        # Default Bourbon
        suggestions.update(
            {
                "brew_ratio": "1:15.5",
                "water_temp": "94-96°C (201-205°F)",
                "water_quality": "150-180 ppm TDS, higher mineral content enhances sweetness",
                "technique": "Medium-strong bloom (60s), then two main pours",
                "optimal_age": "7-21 days off roast",
                "filter_type": "Paper filter or metal filter for higher body",
                "flavor_notes": "Caramel, red fruit, balanced acidity, nutty",
                "troubleshooting": "To enhance sweetness, try a stronger 1:15 ratio",
                "description": "Bourbon tends to have good sweetness and balanced acidity. A slightly higher temperature and stronger ratio can help accentuate its inherent sweetness.",
            }
        )

        # Bourbon color mutations
        if "yellow bourbon" in varietal:
            suggestions.update(
                {
                    "brew_ratio": "1:15.5",
                    "grind_size": "Medium (20-24 on Comandante)",
                    "water_temp": "92-94°C (198-201°F)",
                    "flavor_notes": "Honey, caramel, yellow fruits, softer acidity",
                    "description": "Yellow Bourbon combines the sweetness of Bourbon with a softer acidity. Slightly stronger ratio helps develop its full sweetness potential.",
                }
            )
        elif "pink bourbon" in varietal:
            suggestions.update(
                {
                    "brew_ratio": "1:16",
                    "grind_size": "Medium-fine (18-22 on Comandante)",
                    "water_temp": "91-93°C (196-199°F)",
                    "technique": "60s bloom, gentle pulse pouring",
                    "flavor_notes": "Floral, red berries, tropical fruit, wine-like acidity",
                    "description": "Pink Bourbon often presents with floral notes and vibrant acidity. A medium-fine grind with moderate temperature helps highlight its complex flavor profile.",
                }
            )
        elif "orange bourbon" in varietal:
            suggestions.update(
                {
                    "brew_ratio": "1:16",
                    "grind_size": "Medium (20-24 on Comandante)",
                    "water_temp": "93-95°C (199-203°F)",
                    "flavor_notes": "Orange zest, caramel, chocolate, bright acidity",
                    "description": "Orange Bourbon typically has a good balance of sweetness and acidity with distinctive citrus notes. A standard approach with slightly higher temperature helps develop its full flavor profile.",
                }
            )

    # SL varietals (Kenya)
    elif "sl28" in varietal or "sl-28" in varietal:
        suggestions.update(
            {
                "brew_ratio": "1:16",
                "grind_size": "Medium-fine (18-22 on Comandante)",
                "water_temp": "93-95°C (199-203°F)",
                "water_quality": "150-170 ppm TDS, balanced mineral content",
                "technique": "45s bloom, then slow continuous pour",
                "optimal_age": "10-28 days off roast (Kenyan coffees benefit from longer rest)",
                "filter_type": "Paper filter (preferably white, oxygen-bleached)",
                "flavor_notes": "Blackcurrant, tomato, grapefruit, winey, complex acidity",
                "troubleshooting": "For more balanced acidity, try a 1:16.5 ratio",
                "description": "SL28 is known for its vibrant blackcurrant notes and complex acidity. A medium-fine grind and slightly higher temperature helps extract its distinctive berry and citrus notes.",
            }
        )
    elif "sl34" in varietal or "sl-34" in varietal:
        suggestions.update(
            {
                "brew_ratio": "1:16",
                "grind_size": "Medium (20-25 on Comandante)",
                "water_temp": "92-94°C (198-201°F)",
                "water_quality": "150-180 ppm TDS",
                "technique": "40s bloom, then two medium pours",
                "optimal_age": "10-28 days off roast",
                "filter_type": "Paper filter",
                "flavor_notes": "Blackberry, chocolate, fuller body than SL28, citrus",
                "description": "SL34 typically has good body with chocolate notes complementing the berry acidity. A standard approach works well to balance its body and sweetness.",
            }
        )
    elif "kenyan" in varietal and not (
        "sl28" in varietal
        or "sl34" in varietal
        or "sl-28" in varietal
        or "sl-34" in varietal
    ):
        suggestions.update(
            {
                "brew_ratio": "1:16",
                "grind_size": "Medium-fine (18-22 on Comandante)",
                "water_temp": "93-95°C (199-203°F)",
                "water_quality": "150-170 ppm TDS",
                "technique": "45s bloom, then slow continuous pour",
                "optimal_age": "10-28 days off roast",
                "filter_type": "Paper filter",
                "flavor_notes": "Blackcurrant, grapefruit, tomato, complex acidity",
                "description": "Kenyan coffees typically have distinctive blackcurrant notes with vibrant, juicy acidity. A medium-fine grind with slightly higher temperature helps extract these characteristics.",
            }
        )

    # Pacamara
    elif "pacamara" in varietal:
        suggestions.update(
            {
                "brew_ratio": "1:15",
                "grind_size": "Medium-coarse (24-28 on Comandante)",
                "water_temp": "94-96°C (201-205°F)",
                "water_quality": "150-180 ppm TDS",
                "technique": "Extended bloom (60s), then pulse pouring technique",
                "optimal_age": "7-21 days off roast",
                "filter_type": "Paper filter or metal filter for higher body",
                "flavor_notes": "Stone fruit, maple syrup, complex acidity, full body",
                "troubleshooting": "Due to bean size, may require coarser grind than expected. If astringent, go coarser.",
                "description": "Pacamara can have complex acidity and flavor with large bean size. A coarser grind with hotter water helps balance the extraction of this distinctive varietal.",
            }
        )

    # Typica
    elif "typica" in varietal:
        suggestions.update(
            {
                "brew_ratio": "1:16",
                "water_temp": "92-94°C (198-201°F)",
                "water_quality": "150 ppm TDS",
                "technique": "Gentle continuous pour after 45s bloom",
                "optimal_age": "7-14 days off roast",
                "filter_type": "Paper filter",
                "flavor_notes": "Clean, sweet, mild acidity, chocolate, nutty",
                "description": "Typica often has clean, sweet characteristics. A balanced approach helps showcase its traditional flavors.",
            }
        )

    # Caturra
    elif "caturra" in varietal:
        suggestions.update(
            {
                "brew_ratio": "1:16.5",
                "grind_size": "Medium (20-25 on Comandante)",
                "water_quality": "140-160 ppm TDS",
                "technique": "Standard pour-over with 30s bloom, then continuous pour",
                "optimal_age": "7-14 days off roast",
                "filter_type": "Paper filter",
                "flavor_notes": "Bright acidity, medium body, citrus, apple",
                "description": "Caturra often has bright acidity and medium body. A standard approach works well, but a slightly more dilute ratio can help highlight its clarity.",
            }
        )

    # Catuai
    elif "catuai" in varietal:
        suggestions.update(
            {
                "brew_ratio": "1:15.5",
                "grind_size": "Medium (20-24 on Comandante)",
                "water_temp": "93-95°C (199-203°F)",
                "water_quality": "150-180 ppm TDS",
                "technique": "30s bloom, then continuous pour",
                "optimal_age": "7-14 days off roast",
                "filter_type": "Paper filter",
                "flavor_notes": "Chocolate, nutty, medium acidity, caramel",
                "description": "Catuai often presents with good sweetness and medium acidity. A slightly stronger ratio and higher temperature helps develop its full flavor potential.",
            }
        )
        if "yellow catuai" in varietal:
            suggestions.update(
                {
                    "flavor_notes": "Caramel, yellow fruits, milder acidity, nutty",
                    "description": "Yellow Catuai typically has milder acidity with pronounced sweetness. A slightly stronger ratio enhances its caramel-like sweetness.",
                }
            )
        elif "red catuai" in varietal:
            suggestions.update(
                {
                    "flavor_notes": "Red apple, chocolate, medium acidity, fuller body",
                    "description": "Red Catuai generally has more pronounced acidity than Yellow Catuai with red fruit notes. A balanced approach works well.",
                }
            )

    # Mundo Novo
    elif "mundo novo" in varietal:
        suggestions.update(
            {
                "brew_ratio": "1:15",
                "grind_size": "Medium (20-25 on Comandante)",
                "water_temp": "94-96°C (201-205°F)",
                "water_quality": "170-200 ppm TDS, higher mineral content",
                "technique": "30s bloom, followed by two main pours",
                "optimal_age": "7-14 days off roast",
                "filter_type": "Paper or metal filter",
                "flavor_notes": "Chocolate, nutty, low acidity, full body",
                "description": "Mundo Novo typically has good body and chocolatey notes. A stronger ratio with higher temperature enhances its body and sweetness.",
            }
        )

    # Maragogipe
    elif "maragogipe" in varietal or "maragogype" in varietal:
        suggestions.update(
            {
                "brew_ratio": "1:16.5",
                "grind_size": "Medium-coarse (24-28 on Comandante)",
                "water_temp": "92-94°C (198-201°F)",
                "water_quality": "150 ppm TDS",
                "technique": "60s bloom, gentle pulse pours",
                "optimal_age": "7-14 days off roast",
                "filter_type": "Paper filter",
                "flavor_notes": "Mild acidity, floral notes, tea-like, delicate",
                "troubleshooting": "Due to large bean size, requires coarser grind. If thin-tasting, use slightly hotter water.",
                "description": "Maragogipe beans are large 'elephant beans' with unique characteristics. Their size requires a coarser grind, and gentle extraction helps highlight their distinct flavor profile.",
            }
        )

    # Villa Sarchi
    elif "villa sarchi" in varietal:
        suggestions.update(
            {
                "brew_ratio": "1:16",
                "grind_size": "Medium-fine (18-22 on Comandante)",
                "water_temp": "91-93°C (196-199°F)",
                "water_quality": "130-150 ppm TDS",
                "technique": "45s bloom, slow continuous pour",
                "optimal_age": "7-14 days off roast",
                "filter_type": "Paper filter",
                "flavor_notes": "Bright acidity, honey sweetness, citrus, light body",
                "description": "Villa Sarchi often has bright acidity with delicate sweetness. A finer grind helps extract its complexity while moderate temperature preserves its delicate notes.",
            }
        )

    # Catimor
    elif "catimor" in varietal:
        suggestions.update(
            {
                "brew_ratio": "1:15",
                "grind_size": "Medium (20-25 on Comandante)",
                "water_temp": "94-96°C (201-205°F)",
                "water_quality": "170-200 ppm TDS",
                "technique": "30s bloom, then two strong pours",
                "optimal_age": "7-14 days off roast",
                "filter_type": "Paper filter",
                "flavor_notes": "Cedar, earthy, herbal, medium-high body",
                "troubleshooting": "To reduce potential astringency, use slightly cooler water",
                "description": "Catimor typically has robust flavors and good body. A stronger ratio and higher temperature helps balance its sometimes astringent characteristics.",
            }
        )

    # Java
    elif "java" in varietal:
        suggestions.update(
            {
                "brew_ratio": "1:15.5",
                "grind_size": "Medium (20-24 on Comandante)",
                "water_temp": "93-95°C (199-203°F)",
                "water_quality": "150-170 ppm TDS",
                "technique": "40s bloom, consistent medium flow",
                "optimal_age": "7-14 days off roast",
                "filter_type": "Paper filter",
                "flavor_notes": "Herbal, spicy, medium body, clean finish",
                "description": "Java varietals typically offer herbal notes with good body. A slightly stronger ratio helps accentuate its distinctive characteristics.",
            }
        )

    # Tabi
    elif "tabi" in varietal:
        suggestions.update(
            {
                "brew_ratio": "1:16",
                "grind_size": "Medium (20-24 on Comandante)",
                "water_temp": "92-94°C (198-201°F)",
                "water_quality": "140-160 ppm TDS",
                "technique": "45s bloom, two main pours",
                "optimal_age": "7-14 days off roast",
                "filter_type": "Paper filter",
                "flavor_notes": "Red fruit, chocolate, balanced acidity, good body",
                "description": "Tabi often has a balanced profile with good sweetness. A standard approach works well to highlight its balanced characteristics.",
            }
        )

    # Maracaturra
    elif "maracaturra" in varietal:
        suggestions.update(
            {
                "brew_ratio": "1:15.5",
                "grind_size": "Medium-coarse (24-28 on Comandante)",
                "water_temp": "94-96°C (201-205°F)",
                "water_quality": "150-170 ppm TDS",
                "technique": "60s bloom, then pulse pouring",
                "optimal_age": "7-14 days off roast",
                "filter_type": "Paper filter",
                "flavor_notes": "Fruity, full body, chocolate, moderate acidity",
                "troubleshooting": "Due to large bean size, requires coarser grind. If sour, use slightly higher temperature.",
                "description": "Maracaturra is a cross between Maragogipe and Caturra with large beans. A coarser grind with higher temperature helps balance its unique flavor profile.",
            }
        )

    # Icatu
    elif "icatu" in varietal:
        suggestions.update(
            {
                "brew_ratio": "1:15.5",
                "grind_size": "Medium (20-25 on Comandante)",
                "water_temp": "94-96°C (201-205°F)",
                "water_quality": "150-180 ppm TDS",
                "technique": "30s bloom, then continuous pour",
                "optimal_age": "7-14 days off roast",
                "filter_type": "Paper filter",
                "flavor_notes": "Chocolate, nutty, low-medium acidity, full body",
                "description": "Icatu typically has good body and sweetness. A slightly stronger ratio with higher temperature enhances its chocolatey notes.",
            }
        )

    # Process-based suggestions
    process = process.lower() if process else ""

    # Natural/Dry process
    if "natural" in process or "dry" in process:
        suggestions.update(
            {
                "brew_ratio": "1:16.5 to 1:17",
                "grind_size": "Medium-coarse (24-28 on Comandante)",
                "water_temp": "88-92°C (190-198°F)",
                "water_quality": "120-150 ppm TDS, softer water preferred",
                "technique": "Longer bloom (45-60s), gentle pulse pouring",
                "optimal_age": "14-28 days off roast (naturals benefit from longer rest)",
                "filter_type": "Paper filter (preferably white, oxygen-bleached)",
                "flavor_notes": "Berries, tropical fruit, fermented notes, wine-like",
                "troubleshooting": "If ferment flavors are too intense, use cooler water and more dilute ratio (1:17-1:18)",
                "description": "Natural processed coffees have pronounced fruit notes and sweetness. A slightly coarser grind and cooler water can help control ferment notes while highlighting the fruity character.",
            }
        )

    # Washed/Wet process
    elif "washed" in process or "wet" in process:
        suggestions.update(
            {
                "brew_ratio": "1:15.5 to 1:16",
                "grind_size": "Medium (20-25 on Comandante)",
                "water_temp": "92-96°C (198-205°F)",
                "water_quality": "150-180 ppm TDS",
                "technique": "Standard 30-45s bloom, then continuous pour",
                "optimal_age": "7-21 days off roast",
                "filter_type": "Paper filter or metal filter depending on desired clarity",
                "flavor_notes": "Clean, bright acidity, transparent, defined sweetness",
                "description": "Washed coffees typically have a cleaner profile with defined acidity. A standard approach with slightly higher temperature can highlight these characteristics.",
            }
        )

        # Double washed variation
        if "double washed" in process or "double soaked" in process:
            suggestions.update(
                {
                    "brew_ratio": "1:16",
                    "grind_size": "Medium-fine (18-22 on Comandante)",
                    "water_temp": "92-94°C (198-201°F)",
                    "water_quality": "130-150 ppm TDS",
                    "technique": "30s bloom, then continuous measured pour",
                    "flavor_notes": "Exceptional clarity, vibrant acidity, clean finish",
                    "description": "Double washed coffees have exceptional clarity and defined acidity. A medium-fine grind helps highlight their clean profile and vibrant characteristics.",
                }
            )

    # Honey/Pulped Natural process
    elif "honey" in process or "pulped" in process:
        # Default honey process
        honey_suggestions = {
            "brew_ratio": "1:16",
            "grind_size": "Medium (20-24 on Comandante)",
            "water_temp": "90-94°C (194-201°F)",
            "water_quality": "140-160 ppm TDS",
            "technique": "45s bloom, then two main gentle pours",
            "optimal_age": "10-21 days off roast",
            "filter_type": "Paper filter",
            "flavor_notes": "Balanced sweetness and acidity, stone fruit, honey",
            "description": "Honey/pulped natural coffees balance the fruity sweetness of naturals with some clarity of washed coffees. A moderate approach helps balance these characteristics.",
        }
        suggestions.update(honey_suggestions)

        # Specific honey process variations
        if "black honey" in process:
            suggestions.update(
                {
                    "brew_ratio": "1:16",
                    "water_temp": "90-92°C (194-198°F)",
                    "water_quality": "130-150 ppm TDS",
                    "flavor_notes": "Intense sweetness, dried fruit, full body, wine-like",
                    "description": "Black honey processing leaves most of the mucilage intact, creating fruity sweetness similar to naturals. A moderate approach with slightly cooler water balances sweetness and clarity.",
                }
            )
        elif "red honey" in process:
            suggestions.update(
                {
                    "brew_ratio": "1:16",
                    "water_temp": "91-93°C (196-199°F)",
                    "water_quality": "140-160 ppm TDS",
                    "flavor_notes": "Stone fruit, caramel, moderate body, good sweetness",
                    "description": "Red honey processing leaves significant mucilage, creating good sweetness with moderate clarity. A balanced approach works well for this processing method.",
                }
            )
        elif "yellow honey" in process:
            suggestions.update(
                {
                    "brew_ratio": "1:16",
                    "water_temp": "92-94°C (198-201°F)",
                    "water_quality": "140-160 ppm TDS",
                    "flavor_notes": "Balanced acidity, mild fruit notes, honey sweetness",
                    "description": "Yellow honey processing removes more mucilage, resulting in a cleaner cup with subtle sweetness. A standard approach helps balance its characteristics.",
                }
            )
        elif "white honey" in process:
            suggestions.update(
                {
                    "brew_ratio": "1:16",
                    "water_temp": "92-95°C (198-203°F)",
                    "water_quality": "150-170 ppm TDS",
                    "flavor_notes": "Clean, bright acidity, subtle sweetness, tea-like",
                    "description": "White honey processing removes most of the mucilage, creating a profile closer to washed coffees. A standard approach with slightly higher temperature highlights its clean characteristics.",
                }
            )

    # Anaerobic fermentation
    elif "anaerobic" in process or "fermentation" in process:
        suggestions.update(
            {
                "brew_ratio": "1:17",
                "grind_size": "Medium-coarse (24-28 on Comandante)",
                "water_temp": "88-92°C (190-198°F)",
                "water_quality": "120-140 ppm TDS, softer water preferred",
                "technique": "Extended bloom (60s), very gentle pulse pours",
                "optimal_age": "14-28 days off roast",
                "filter_type": "Paper filter (preferably white, oxygen-bleached)",
                "flavor_notes": "Intense fruit, fermentation notes, wine-like acidity",
                "troubleshooting": "If ferment flavors are overwhelming, use cooler water and more dilute ratio",
                "description": "Anaerobic fermentation creates unique and often intense flavor profiles. A gentler extraction with cooler water helps control the ferment notes while highlighting the unique characteristics.",
            }
        )

    # Carbonic maceration
    elif "carbonic maceration" in process:
        suggestions.update(
            {
                "brew_ratio": "1:17",
                "grind_size": "Medium-coarse (24-28 on Comandante)",
                "water_temp": "88-91°C (190-196°F)",
                "water_quality": "120-140 ppm TDS, softer water preferred",
                "technique": "60s bloom, very gentle pulse pours with long intervals",
                "optimal_age": "14-28 days off roast",
                "filter_type": "Paper filter (preferably white, oxygen-bleached)",
                "flavor_notes": "Wine-like, red fruit, complex acidity, unique fermentation",
                "troubleshooting": "If wine-like notes are too intense, increase dilution to 1:17.5",
                "description": "Carbonic maceration creates intense fruit-forward profiles with wine-like characteristics. A gentler approach with cooler water helps balance the intense flavors while maintaining clarity.",
            }
        )

    # Wet hulled / Giling Basah
    elif "wet hulled" in process or "giling basah" in process:
        suggestions.update(
            {
                "brew_ratio": "1:15",
                "grind_size": "Medium-coarse (24-28 on Comandante)",
                "water_temp": "94-96°C (201-205°F)",
                "water_quality": "180-220 ppm TDS, higher mineral content",
                "technique": "30s bloom, then strong continuous pour",
                "optimal_age": "14-28 days off roast",
                "filter_type": "Paper or metal filter",
                "flavor_notes": "Earthy, herbal, cedar, spice, heavy body, low acidity",
                "troubleshooting": "If earthy notes are too intense, try slightly cooler water and finer grind",
                "description": "Wet hulled coffee (common in Indonesia) has distinctive earthy and spicy characteristics with full body. A stronger ratio and higher temperature helps balance these bold flavors.",
            }
        )

    # Extended fermentation
    elif "extended fermentation" in process:
        suggestions.update(
            {
                "brew_ratio": "1:16.5",
                "grind_size": "Medium-coarse (24-28 on Comandante)",
                "water_temp": "88-91°C (190-196°F)",
                "water_quality": "120-140 ppm TDS, softer water preferred",
                "technique": "60s bloom, very gentle pulse pouring",
                "optimal_age": "14-28 days off roast",
                "filter_type": "Paper filter (preferably white, oxygen-bleached)",
                "flavor_notes": "Tropical fruit, floral, complex acidity, distinctive ferment",
                "troubleshooting": "If ferment notes are too strong, try 1:17 ratio and slightly cooler water",
                "description": "Extended fermentation creates unique and complex flavor profiles with pronounced fruit notes. A gentler extraction with cooler water helps balance the fermentation characteristics.",
            }
        )

    # Lactic fermentation
    elif "lactic" in process:
        suggestions.update(
            {
                "brew_ratio": "1:17",
                "grind_size": "Medium-coarse (24-28 on Comandante)",
                "water_temp": "87-90°C (189-194°F)",
                "water_quality": "100-130 ppm TDS, very soft water preferred",
                "technique": "60s bloom, extremely gentle pulse pouring",
                "optimal_age": "14-28 days off roast",
                "filter_type": "Paper filter (preferably white, oxygen-bleached)",
                "flavor_notes": "Yogurt, cream, berries, unique dairy-like acidity",
                "troubleshooting": "If lactic notes are overwhelming, increase dilution to 1:18",
                "description": "Lactic fermentation produces unique dairy-like acidity and creamy textures. A very gentle extraction with cool water helps highlight these delicate characteristics while controlling fermentation notes.",
            }
        )

    # Acetic fermentation
    elif "acetic" in process:
        suggestions.update(
            {
                "brew_ratio": "1:17",
                "grind_size": "Medium-coarse (24-28 on Comandante)",
                "water_temp": "88-91°C (190-196°F)",
                "water_quality": "120-140 ppm TDS, softer water preferred",
                "technique": "60s bloom, gentle pulse pouring",
                "optimal_age": "14-28 days off roast",
                "filter_type": "Paper filter (preferably white, oxygen-bleached)",
                "flavor_notes": "Apple cider, vinegar-like brightness, fruit, complex",
                "troubleshooting": "If acetic notes are too strong, try 1:17.5 ratio and slightly cooler water",
                "description": "Acetic fermentation produces bright, vinegar-like acidity with unique fruit characteristics. A gentler extraction with cooler water helps balance the distinctive acidity.",
            }
        )

    # Thermal shock / Thermal shock natural
    elif "thermal shock" in process:
        suggestions.update(
            {
                "brew_ratio": "1:16.5",
                "grind_size": "Medium-coarse (24-28 on Comandante)",
                "water_temp": "89-92°C (192-198°F)",
                "water_quality": "130-150 ppm TDS",
                "technique": "45s bloom, gentle pulse pouring",
                "optimal_age": "14-28 days off roast",
                "filter_type": "Paper filter",
                "flavor_notes": "Enhanced sweetness, tropical fruit, reduced acidity",
                "description": "Thermal shock processing enhances sweetness while softening acidity. A balanced approach with moderate temperature helps highlight these characteristics.",
            }
        )

    # Experimental/Mixed fermentation
    elif "experimental" in process or "mixed fermentation" in process:
        suggestions.update(
            {
                "brew_ratio": "1:17",
                "grind_size": "Medium-coarse (24-28 on Comandante)",
                "water_temp": "87-91°C (189-196°F)",
                "water_quality": "120-140 ppm TDS, softer water preferred",
                "technique": "60s bloom, very gentle pulse pouring",
                "optimal_age": "14-28 days off roast",
                "filter_type": "Paper filter (preferably white, oxygen-bleached)",
                "flavor_notes": "Unique fermentation, complex fruit notes, varied acidity",
                "troubleshooting": "If fermentation notes are overwhelming, try cooler water and 1:17.5 ratio",
                "description": "Experimental processing methods create unique and unpredictable flavor profiles. A gentler extraction approach with cooler water helps balance these distinctive characteristics.",
            }
        )

    # Barrel aged/conditioned
    elif "barrel" in process or "aged" in process:
        suggestions.update(
            {
                "brew_ratio": "1:16.5",
                "grind_size": "Medium (20-24 on Comandante)",
                "water_temp": "90-93°C (194-199°F)",
                "water_quality": "140-160 ppm TDS",
                "technique": "45s bloom, gentle pulse pouring",
                "optimal_age": "14-28 days off roast",
                "filter_type": "Paper filter",
                "flavor_notes": "Oak, whiskey/wine notes, enhanced sweetness, unique complexity",
                "troubleshooting": "If boozy notes are too strong, try a 1:17 ratio and cooler water",
                "description": "Barrel aged or conditioned coffees absorb flavors from the barrel's previous contents. A balanced approach with moderate temperature highlights these unique characteristics without overwhelming the coffee's inherent flavors.",
            }
        )

    # Monsooned/Aged coffee
    elif "monsooned" in process or "monsoon" in process:
        suggestions.update(
            {
                "brew_ratio": "1:15",
                "grind_size": "Medium-coarse (24-28 on Comandante)",
                "water_temp": "94-96°C (201-205°F)",
                "water_quality": "180-220 ppm TDS, higher mineral content",
                "technique": "30s bloom, strong continuous pour",
                "optimal_age": "14-28 days off roast",
                "filter_type": "Paper or metal filter",
                "flavor_notes": "Musty, spicy, tobacco, low acidity, heavy body",
                "troubleshooting": "If mustiness is overwhelming, try slightly cooler water",
                "description": "Monsooned coffees are exposed to monsoon winds, creating a unique aged character with low acidity. A stronger ratio and higher temperature helps balance the distinctive flavor profile.",
            }
        )

    # Semi-washed / Wet-hulled / Giling Basah (Indonesia)
    elif "semi-washed" in process:
        suggestions.update(
            {
                "brew_ratio": "1:15.5",
                "grind_size": "Medium (22-26 on Comandante)",
                "water_temp": "93-95°C (199-203°F)",
                "water_quality": "160-180 ppm TDS",
                "technique": "30s bloom, then strong continuous pour",
                "optimal_age": "14-28 days off roast",
                "filter_type": "Paper or metal filter",
                "flavor_notes": "Earthy, woody, herbal, medium-high body",
                "description": "Semi-washed processing creates earthy characteristics with moderate body. A slightly stronger ratio and higher temperature helps balance these distinctive flavors.",
            }
        )

    # Sun-dried honey
    elif "sun-dried honey" in process:
        suggestions.update(
            {
                "brew_ratio": "1:16",
                "grind_size": "Medium (20-24 on Comandante)",
                "water_temp": "90-93°C (194-199°F)",
                "water_quality": "130-150 ppm TDS",
                "technique": "45s bloom, gentle pulse pouring",
                "optimal_age": "10-21 days off roast",
                "filter_type": "Paper filter",
                "flavor_notes": "Intense sweetness, dried fruit, caramelized sugar",
                "description": "Sun-dried honey process enhances sweetness and body. A balanced approach with moderate temperature highlights these distinctive characteristics.",
            }
        )

    # Wine yeast fermentation
    elif "wine yeast" in process:
        suggestions.update(
            {
                "brew_ratio": "1:16.5",
                "grind_size": "Medium-coarse (24-28 on Comandante)",
                "water_temp": "88-91°C (190-196°F)",
                "water_quality": "120-140 ppm TDS, softer water preferred",
                "technique": "60s bloom, gentle pulse pouring",
                "optimal_age": "14-28 days off roast",
                "filter_type": "Paper filter",
                "flavor_notes": "Wine-like, berry, complex acidity, unique fermentation",
                "description": "Wine yeast fermentation creates distinctive wine-like characteristics. A gentler extraction with cooler water helps highlight these nuanced flavors.",
            }
        )

    # Cold fermentation
    elif "cold fermentation" in process:
        suggestions.update(
            {
                "brew_ratio": "1:16.5",
                "grind_size": "Medium (20-24 on Comandante)",
                "water_temp": "90-93°C (194-199°F)",
                "water_quality": "130-150 ppm TDS",
                "technique": "45s bloom, gentle pulse pouring",
                "optimal_age": "10-21 days off roast",
                "filter_type": "Paper filter",
                "flavor_notes": "Clean, complex acidity, enhanced sweetness",
                "description": "Cold fermentation creates a cleaner profile with enhanced sweetness. A balanced approach with moderate temperature highlights these characteristics.",
            }
        )

    # Anaerobic washed
    elif "anaerobic washed" in process:
        suggestions.update(
            {
                "brew_ratio": "1:16.5",
                "grind_size": "Medium (20-24 on Comandante)",
                "water_temp": "90-93°C (194-199°F)",
                "water_quality": "130-150 ppm TDS",
                "technique": "45s bloom, gentle pulse pouring",
                "optimal_age": "10-21 days off roast",
                "filter_type": "Paper filter",
                "flavor_notes": "Clean, tropical fruit, complex acidity, balanced ferment",
                "description": "Anaerobic washed combines the clarity of washed process with unique fermentation notes. A balanced approach with moderate temperature helps highlight this complexity.",
            }
        )

    # Anaerobic natural
    elif "anaerobic natural" in process:
        suggestions.update(
            {
                "brew_ratio": "1:17",
                "grind_size": "Medium-coarse (24-28 on Comandante)",
                "water_temp": "87-90°C (189-194°F)",
                "water_quality": "120-140 ppm TDS, softer water preferred",
                "technique": "60s bloom, very gentle pulse pouring",
                "optimal_age": "14-28 days off roast",
                "filter_type": "Paper filter (preferably white, oxygen-bleached)",
                "flavor_notes": "Intense fruit, strong fermentation, boozy, syrupy",
                "troubleshooting": "If fermentation notes are overwhelming, try 1:17.5 ratio and cooler water",
                "description": "Anaerobic natural processing creates intense fruit and fermentation characteristics. A very gentle extraction with cooler water helps balance these powerful flavors.",
            }
        )

    # Anaerobic honey
    elif "anaerobic honey" in process:
        suggestions.update(
            {
                "brew_ratio": "1:16.5",
                "grind_size": "Medium-coarse (24-28 on Comandante)",
                "water_temp": "89-92°C (192-198°F)",
                "water_quality": "130-150 ppm TDS",
                "technique": "45s bloom, gentle pulse pouring",
                "optimal_age": "10-21 days off roast",
                "filter_type": "Paper filter",
                "flavor_notes": "Honey sweetness, tropical fruit, balanced fermentation",
                "description": "Anaerobic honey processing combines honey sweetness with controlled fermentation. A balanced approach with moderate temperature helps highlight these complex characteristics.",
            }
        )

    # # Combine varietal and process suggestions (existing combinations)
    # if varietal and process:
    #     # Special combinations
    #     if ("gesha" in varietal or "geisha" in varietal) and "natural" in process:
    #         suggestions.update({
    #             "brew_ratio": "1:17.5",
    #             "grind_size": "Medium (22-24 on Comandante)",
    #             "water_temp": "88-90°C (190-194°F)",
    #             "technique": "Very gentle pour with 60s bloom, then slow, deliberate pulse pours",
    #             "description": "Natural Gesha/Geisha combines intense florals with fruit-forward fermentation. Using cooler water and a more dilute ratio helps balance these intense flavors while maintaining clarity."
    #         })
    #     elif "bourbon" in varietal and "washed" in process:
    #         suggestions.update({
    #             "brew_ratio": "1:15.5",
    #             "water_temp": "94-96°C (201-205°F)",
    #             "technique": "Strong 45s bloom, then continuous pour",
    #             "description": "Washed Bourbon often has excellent sweetness and balanced acidity. A slightly higher temperature and stronger ratio can help extract its full sweetness potential."
    #         })

    #     # Added combinations
    #     elif ("sl28" in varietal or "sl-28" in varietal) and "washed" in process:
    #         suggestions.update({
    #             "brew_ratio": "1:16",
    #             "grind_size": "Medium-fine (18-22 on Comandante)",
    #             "water_temp": "93-95°C (199-203°F)",
    #             "technique": "45s bloom, slow continuous pour",
    #             "description": "Washed SL28 showcases vibrant blackcurrant and citrus notes with exceptional clarity. A medium-fine grind with slightly higher temperature helps extract its distinctive characteristics."
    #         })
    #     elif ("ethiopia heirloom" in varietal or "ethiopian heirloom" in varietal) and "natural" in process:
    #         suggestions.update({
    #             "brew_ratio": "1:17",
    #             "grind_size": "Medium-coarse (22-26 on Comandante)",
    #             "water_temp": "88-91°C (190-196°F)",
    #             "technique": "60s bloom, very gentle pulse pours",
    #             "description": "Natural Ethiopian heirloom varieties offer intense berry notes and wine-like fermentation. A gentler approach with cooler water helps balance these intense characteristics while maintaining clarity."
    #         })
    #     elif "pacamara" in varietal and "anaerobic" in process:
    #         suggestions.update({
    #             "brew_ratio": "1:17",
    #             "grind_size": "Medium-coarse (24-28 on Comandante)",
    #             "water_temp": "88-90°C (190-194°F)",
    #             "technique": "60s bloom, very gentle pulse pours with long intervals",
    #             "description": "Anaerobically processed Pacamara creates an extremely complex, intense flavor profile. A very gentle approach helps balance these powerful flavors while maintaining some clarity."
    #         })
    #     elif "caturra" in varietal and "honey" in process:
    #         suggestions.update({
    #             "brew_ratio": "1:16",
    #             "grind_size": "Medium (20-24 on Comandante)",
    #             "water_temp": "91-93°C (196-199°F)",
    #             "technique": "45s bloom, then two gentle pours",
    #             "description": "Honey processed Caturra balances the varietal's bright acidity with added sweetness from the processing. A balanced approach highlights both characteristics."
    #         })
    #     elif "yellow bourbon" in varietal and "natural" in process:
    #         suggestions.update({
    #             "brew_ratio": "1:16.5",
    #             "grind_size": "Medium-coarse (22-26 on Comandante)",
    #             "water_temp": "89-92°C (192-198°F)",
    #             "technique": "60s bloom, gentle pulse pouring",
    #             "description": "Natural Yellow Bourbon combines the inherent sweetness of the varietal with fruity fermentation notes. A gentler approach with cooler water balances these characteristics."
    #         })

    return suggestions
