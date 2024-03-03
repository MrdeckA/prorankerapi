description_intitule = [normaliser_chaine(
        chaine) for chaine in description_intitule]
    predictions = [normaliser_chaine(chaine) for chaine in predictions]

    # Initialiser la variable de score
    score = sum(any(chaine1 in chaine2 for chaine2 in predictions)
                for chaine1 in description_intitule)

    # language
    languages_count = len(languages)
    campagne_languages = [normaliser_chaine(
        chaine) for chaine in campagne.languages.split(',')]
    languages = [normaliser_chaine(chaine) for chaine in languages]
    score += sum(any(chaine1 in chaine2 for chaine2 in languages)
                 for chaine1 in campagne_languages)

    # skills
    campagne_skills = [normaliser_chaine(chaine)
                       for chaine in campagne.skills.split(',')]
    score += sum(any(chaine1 in chaine2 for chaine2 in predictions)
                 for chaine1 in campagne_skills)

    # autres critères
    experiences_count = len(experiences)
    awards_count = len(awards)
    certifications_count = len(certifications)

    score += awards_count > 0
    score += certifications_count > 0
    score += experiences_count >= campagne.minimum_number_of_experiences
    score += languages_count >= campagne.minimum_number_of_languages

    diplomes = {
        "Diplôme d'études primaires (DEP)": ["DEP", "Diplôme d'études primaires"],
        "Brevet d'études du premier cycle (BEPC)": ["BEPC", "Brevet d'études du premier cycle"],
        "Baccalauréat (BAC)": ["BAC", "Baccalauréat"],
        "Licence (L1, L2, L3)": ["Licence", "L1", "L2", "L3"],
        "Master (M1, M2)": ["Master", "M1", "M2"],
        "Doctorat (Ph.D.)": ["Doctorat", "Ph.D."],
        "Certificat d'aptitude professionnelle (CAP)": ["CAP", "Certificat d'aptitude professionnelle"],
        "Brevet de technicien supérieur (BTS)": ["BTS", "Brevet de technicien supérieur"],
        "Diplôme universitaire de technologie (DUT)": ["DUT", "Diplôme universitaire de technologie"],
        "Certificat universitaire (CU)": ["CU", "Certificat universitaire"],
        "Mastère spécialisé (MS)": ["MS", "Mastère spécialisé"],
        "Agrégation": ["Agrégation"]
    }
    degree = [normaliser_chaine(chaine) for chaine in degree]
    campagne_diplome = [normaliser_chaine(
        chaine) for chaine in diplomes[campagne.minimum_degree]]
    score += any(chaine1 in chaine2 for chaine1 in campagne_diplome for chaine2 in degree)

    if not is_valid_email(email):
        email = recuperer_premiere_email(text)
        print(fname, email)
    data = {
        "score": score,
        "description_intitule": description_intitule,
        "intitules": intitules,
        "predictions": predictions,
        "degree": degree,
        "experiences": experiences,
        "certifications": certifications,
        "awards": awards,
        "languages": languages,
        "email": email,
        "nom_complet": nom_complet,
        "texte_pdf": text
    }